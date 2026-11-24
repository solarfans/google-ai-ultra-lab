#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Optical-flow video pacing & motion QA (adapted from HeyChengC/wallstreet-explainer, MIT).

Usage:
  .venv/bin/python scripts/motion_check.py video1.mp4 [video2.mp4 ...] [--top 0.8] [--from 0] [--to 999] [--json]

Measures frame-to-frame Farneback optical flow over the upper `--top` fraction of each
frame (default 0.80, avoiding bottom captions), decomposes global camera pan/zoom from
non-uniform parallax/subject residual, and flags static holds > 2s or low-motion pacing.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

import cv2
import numpy as np

REF = {
    "still": (0.149, 0.287, "Static frame ratio"),
    "hold2": (0.64, 1.0, "Holds > 2s (per min)"),
    "cam": (0.213, 0.271, "Camera-motion ratio"),
    "layer": (0.09, 0.123, "Parallax/layered motion"),
    "nonuni": (0.52, 0.62, "Non-uniformity ratio"),
    "pushpull": (1.3, 2.9, "Zoom-in : zoom-out"),
    "zoom": (2.8, 3.6, "Drift speed (%/s)"),
    "p75": (2.37, 3.03, "Shot dur p75 (s)"),
    "cutmin": (25.6, 32.3, "Cuts per min"),
}

SAMPLE_FPS = 30
WIDTH, HEIGHT = 320, 180


def measure(src: str, top: float = 0.8, t0: float = 0.0, t1: float = 1e9) -> dict[str, Any]:
    """Compute optical-flow pacing metrics for a single video file."""
    h = max(16, int(HEIGHT * top))
    cmd = ["ffmpeg", "-v", "error", "-ss", str(t0), "-i", src]
    if t1 < 1e8:
        cmd += ["-t", str(max(0.1, t1 - t0))]
    cmd += [
        "-vf",
        f"fps={SAMPLE_FPS},scale={WIDTH}:{HEIGHT},format=gray",
        "-f",
        "rawvideo",
        "-",
    ]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    assert proc.stdout is not None

    ys, xs = np.mgrid[6 : h - 6 : 8, 6 : WIDTH - 6 : 8]
    x_flat = (xs - WIDTH / 2).ravel().astype(np.float32)
    y_flat = (ys - h / 2).ravel().astype(np.float32)
    basis = np.zeros((2 * len(x_flat), 4), np.float32)
    basis[0::2, 0] = x_flat
    basis[0::2, 1] = -y_flat
    basis[0::2, 2] = 1
    basis[1::2, 0] = y_flat
    basis[1::2, 1] = x_flat
    basis[1::2, 3] = 1

    rows: list[tuple[float, float, float, float, float, float]] = []
    prev = None
    frame_bytes = WIDTH * HEIGHT
    try:
        while True:
            buf = proc.stdout.read(frame_bytes)
            if len(buf) < frame_bytes:
                break
            gray = np.frombuffer(buf, np.uint8).reshape(HEIGHT, WIDTH)[:h]
            if prev is not None:
                diff = float(np.abs(gray.astype(np.int16) - prev).mean())
                flow = cv2.calcOpticalFlowFarneback(
                    prev, gray, None, 0.5, 3, 15, 3, 5, 1.2, 0
                )
                u = flow[ys, xs, 0].ravel()
                v = flow[ys, xs, 1].ravel()
                grad = np.hypot(
                    cv2.Sobel(prev, cv2.CV_32F, 1, 0),
                    cv2.Sobel(prev, cv2.CV_32F, 0, 1),
                )
                tex = grad[ys, xs].ravel() > 20
                mag = float(np.hypot(u, v)[tex].mean()) if tex.sum() > 20 else 0.0
                if tex.sum() > 30:
                    idx = np.where(tex)[0]
                    ai = basis.reshape(-1, 2, 4)[idx].reshape(-1, 4)
                    bi = np.stack([u[idx], v[idx]], 1).ravel()
                    af, bf = ai, bi
                    sol = np.zeros(4, np.float32)
                    for _ in range(3):
                        sol, *_ = np.linalg.lstsq(ai, bi, rcond=None)
                        rn = np.hypot(*(ai @ sol - bi).reshape(-1, 2).T)
                        keep = rn < max(0.3, float(np.percentile(rn, 70)) * 2)
                        if keep.all() or keep.sum() < 8:
                            break
                        ai = ai.reshape(-1, 2, 4)[keep].reshape(-1, 4)
                        bi = bi.reshape(-1, 2)[keep].ravel()
                    rn = np.hypot(*(af @ sol - bf).reshape(-1, 2).T)
                    res = float(rn.mean())
                    fit = float((rn < 0.5).mean())
                    zoom_val, _, tx, ty = sol
                else:
                    zoom_val = tx = ty = res = 0.0
                    fit = 1.0
                rows.append((diff, float(zoom_val), float(np.hypot(tx, ty)) * 6.0, mag, res, fit))
            prev = gray.copy()
    finally:
        proc.stdout.close()
        stderr_bytes = proc.stderr.read() if proc.stderr else b""
        if proc.stderr:
            proc.stderr.close()
        rc = proc.wait()

    if rc != 0:
        raise RuntimeError(f"ffmpeg failed ({rc}): {stderr_bytes.decode(errors='replace').strip()}")
    if len(rows) < 2:
        raise RuntimeError(f"Video too short or unreadable for optical flow: {src}")

    arr = np.array(rows)
    n = len(arr)
    diff, zoom, tr, mag, res, fit = arr.T
    cut = np.zeros(n, bool)
    last = -9
    for i in range(n):
        nb_arr = np.r_[diff[max(0, i - 6) : i], diff[i + 1 : i + 7]]
        nb = float(np.median(nb_arr)) if len(nb_arr) else 0.0
        if diff[i] > 6 and diff[i] > 3 * nb + 2 and fit[i] < 0.7 and i - last > 4:
            cut[i] = True
            last = i

    cam = (fit > 0.5) & ~cut & ((np.abs(zoom) > 0.0007) | (tr > 1.2))
    still = (mag < 0.04) & ~cut

    def runs(mask: np.ndarray) -> np.ndarray:
        out: list[float] = []
        start = None
        for i, val in enumerate(np.r_[mask, False]):
            if val and start is None:
                start = i
            if not val and start is not None:
                out.append((i - start) / SAMPLE_FPS)
                start = None
        return np.array(out)

    bounds = np.r_[0, np.where(cut)[0], n]
    seg = np.diff(bounds) / SAMPLE_FPS
    seg = seg[seg > 0.1]
    if not len(seg):
        seg = np.array([n / SAMPLE_FPS])

    holds = runs(still)
    mins = max(1e-6, n / SAMPLE_FPS / 60.0)
    zin = int(((zoom > 0.0007) & cam).sum())
    zout = int(((zoom < -0.0007) & cam).sum())

    metrics = {
        "still": round(float(still.mean()), 4),
        "hold2": round(float((holds > 2.0).sum() / mins), 4),
        "cam": round(float(cam.mean()), 4),
        "layer": round(float((cam & (res > 0.25)).mean()), 4),
        "nonuni": round(float(np.median(res[cam] / np.maximum(mag[cam], 1e-3))) if cam.any() else 0.0, 4),
        "pushpull": round(float(zin / max(1, zout)), 4),
        "zoom": round(float(np.median(np.abs(zoom[cam]))) * SAMPLE_FPS * 100.0 if cam.any() else 0.0, 4),
        "p75": round(float(np.percentile(seg, 75)), 4),
        "cutmin": round(float(cut.sum() / mins), 4),
        "duration_s": round(float(n / SAMPLE_FPS), 2),
        "_holds": sorted([round(float(x), 2) for x in holds if x > 2.0]),
    }
    flagged = []
    for k, (lo, hi, _) in REF.items():
        val = metrics[k]
        if (k in ("still", "hold2", "p75") and val > hi * 1.15) or (
            k in ("cam", "layer", "nonuni", "pushpull") and val < lo * 0.85
        ):
            flagged.append(k)
    metrics["flagged"] = flagged
    return metrics


def main() -> int:
    parser = argparse.ArgumentParser(description="Optical-flow video pacing QA.")
    parser.add_argument("videos", nargs="+", help="Input MP4/video files")
    parser.add_argument("--top", type=float, default=0.8, help="Upper frame fraction to analyze")
    parser.add_argument("--from", dest="t_from", type=float, default=0.0, help="Start time (s)")
    parser.add_argument("--to", dest="t_to", type=float, default=1e9, help="End time (s)")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    args = parser.parse_args()

    results = {}
    for v in args.videos:
        if not Path(v).exists():
            print(f"ERROR: file not found: {v}", file=sys.stderr)
            return 2
        results[v] = measure(v, top=args.top, t0=args.t_from, t1=args.t_to)

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
        return 0

    print("Metric".ljust(24), "Ref Range".rjust(12), *[(Path(v).name[-24:]).rjust(26) for v in args.videos])
    for k, (lo, hi, name) in REF.items():
        cells = []
        for v in args.videos:
            val = results[v][k]
            mark = " !" if k in results[v]["flagged"] else "  "
            cells.append(f"{val:.3f}{mark}".rjust(26))
        print(name.ljust(24), f"{lo:g}-{hi:g}".rjust(12), *cells)
    for v in args.videos:
        if results[v]["_holds"]:
            print(f"{Path(v).name} holds > 2s (s): {results[v]['_holds']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
