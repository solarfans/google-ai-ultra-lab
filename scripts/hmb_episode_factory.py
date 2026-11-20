#!/usr/bin/env python3
"""
Reusable 100%-Free-Credit, Zero-Confirmation Production Factory for `How Markets Break`.

Subcommands:
  - prepare <episode_spec.json>:
      1) Enforces `ypp_pilot_gate.py` compliance on sibling `manifest.json` (`gcp_usd_budget == 0`).
      2) Fetches live Yahoo Finance daily closes (`market_snapshot.json`) + computes cross-asset stats.
      3) Renders headless-Chrome 1920x1080 static QA charts + 30fps progressive motion cards.
      4) Synthesizes 7 edge-tts narration beats + word-aligned cues (`voiceover_timeline.json`).
      5) Crossfades 4 tracks from local Flow Music library (`CATALOG.json`, `$0.00` GCP) into `flow_music_score.wav`.
      6) Writes `flow_prompts.json` for Zero-Confirmation `Omni 1.2 Flash` Text-to-Video.
  - master <episode_spec.json>:
      1) Verifies `renders/shot01_flow.mp4..shot05_flow.mp4` via `ffprobe`.
      2) Normalizes narration, sidechain-ducks local Flow Music bed, blends native Flow Foley,
         and renders overflow-proof PNG subtitles for 16:9 Clean, 16:9 Subtitled, and 9:16 Shorts.
      3) Mirrors all 3 masters to `downloads_dir` (`~/Downloads/...`).
"""
from __future__ import annotations

import argparse
import asyncio
import datetime
import html
import json
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = Path(__file__).resolve().parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from ypp_pilot_gate import validate_ypp_pilot_manifest  # noqa: E402

CHROME_BIN = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
FONT_PATHS = (
    "/System/Library/Fonts/HelveticaNeue.ttc",
    "/System/Library/Fonts/SFNS.ttf",
    "/Library/Fonts/Arial.ttf",
)

YAHOO_TICKERS: tuple[tuple[str, str, str], ...] = (
    ("ixic", "Nasdaq Composite (^IXIC)", "^IXIC"),
    ("gold", "Gold Futures (GC=F)", "GC=F"),
    ("btc", "Bitcoin (BTC-USD)", "BTC-USD"),
    ("hyg", "High Yield Corp Bond (HYG)", "HYG"),
    ("ief", "7-10Y Treasury ETF (IEF)", "IEF"),
    ("us10y", "US 10Y Yield (^TNX)", "^TNX"),
    ("dxy", "US Dollar Index (DXY)", "DX-Y.NYB"),
    ("vix", "CBOE Volatility (^VIX)", "^VIX"),
    ("vix3m", "CBOE 3M Volatility (^VIX3M)", "^VIX3M"),
)


def run_cmd(args: list[str], *, check_rc: bool = True) -> subprocess.CompletedProcess[str]:
    res = subprocess.run(args, capture_output=True, text=True, check=False)
    if check_rc and res.returncode != 0:
        raise RuntimeError(f"Command failed ({res.returncode}): {' '.join(args)}\n{res.stderr[:800]}")
    return res


def run_ffmpeg(args: list[str]) -> None:
    run_cmd(["ffmpeg", "-y", "-v", "error", *args], check_rc=True)


def ffprobe_info(path: Path) -> dict[str, Any]:
    out = run_cmd(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration,size:stream=codec_type,codec_name,width,height,sample_rate,channels",
            "-of",
            "json",
            str(path),
        ]
    ).stdout
    data = json.loads(out)
    streams = data.get("streams", [])
    v_stream = next((s for s in streams if s.get("codec_type") == "video"), {})
    a_stream = next((s for s in streams if s.get("codec_type") == "audio"), {})
    return {
        "duration": float(data["format"]["duration"]),
        "size": int(data["format"].get("size", path.stat().st_size)),
        "has_video": bool(v_stream),
        "has_audio": bool(a_stream),
        "width": int(v_stream.get("width", 0)),
        "height": int(v_stream.get("height", 0)),
        "sample_rate": int(a_stream.get("sample_rate", 0)) if a_stream.get("sample_rate") else 0,
        "channels": int(a_stream.get("channels", 0)) if a_stream.get("channels") else 0,
    }


def load_spec(spec_path: Path) -> tuple[dict[str, Any], Path]:
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    return spec, spec_path.resolve().parent


def enforce_manifest_gate(ep_dir: Path) -> dict[str, Any]:
    manifest_path = ep_dir / "manifest.json"
    if not manifest_path.is_file():
        raise FileNotFoundError(f"Missing manifest.json in {ep_dir}")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    verdict = validate_ypp_pilot_manifest(manifest)
    if not verdict["ok"]:
        raise RuntimeError(f"YPP Pilot compliance gate failed: {verdict['reasons']}")
    return verdict


def fetch_yahoo_daily(symbol: str, window_start: str) -> list[dict[str, Any]]:
    encoded = urllib.parse.quote(symbol, safe="")
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{encoded}?range=1mo&interval=1d"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        payload = json.load(resp)["chart"]["result"][0]
    ts = payload["timestamp"]
    closes = payload["indicators"]["quote"][0]["close"]
    by_date: dict[str, float] = {}
    for t, c in zip(ts, closes):
        if c is None:
            continue
        d = datetime.datetime.fromtimestamp(t, datetime.timezone.utc).strftime("%Y-%m-%d")
        if d >= window_start:
            by_date[d] = round(float(c), 2)
    return [{"date": d, "close": by_date[d]} for d in sorted(by_date)]


def summarize_series(points: list[dict[str, Any]]) -> dict[str, Any]:
    if not points:
        raise ValueError("Empty series returned from data source")
    hi = max(points, key=lambda x: x["close"])
    lo = min(points, key=lambda x: x["close"])
    first = points[0]
    last = points[-1]
    return {
        "first_date": first["date"],
        "first_close": first["close"],
        "last_date": last["date"],
        "last_close": last["close"],
        "high_date": hi["date"],
        "high_close": hi["close"],
        "low_date": lo["date"],
        "low_close": lo["close"],
        "pct_from_first": round((last["close"] - first["close"]) / first["close"] * 100.0, 2),
        "pct_from_high": round((last["close"] - hi["close"]) / hi["close"] * 100.0, 2),
        "pct_from_low": round((last["close"] - lo["close"]) / lo["close"] * 100.0, 2),
        "points": points,
    }


def compute_vix_ratio_series(vix_pts: list[dict[str, Any]], vix3m_pts: list[dict[str, Any]]) -> dict[str, Any]:
    """Compute VIX / VIX3M ratio on shared trading dates plus latest spot-over-3M ratio."""
    v3_map = {p["date"]: float(p["close"]) for p in vix3m_pts}
    aligned: list[dict[str, Any]] = []
    for p in vix_pts:
        if p["date"] in v3_map and v3_map[p["date"]] > 0:
            ratio = round(float(p["close"]) / v3_map[p["date"]], 3)
            aligned.append(
                {
                    "date": p["date"],
                    "vix": float(p["close"]),
                    "vix3m": v3_map[p["date"]],
                    "ratio": ratio,
                }
            )
    latest_vix = float(vix_pts[-1]["close"])
    latest_vix3m = float(vix3m_pts[-1]["close"])
    spot_ratio = round(latest_vix / latest_vix3m, 2) if latest_vix3m > 0 else 0.0
    return {
        "aligned_points": aligned,
        "latest_aligned_date": aligned[-1]["date"] if aligned else "",
        "latest_aligned_ratio": round(aligned[-1]["ratio"], 2) if aligned else 0.0,
        "latest_spot_vix": latest_vix,
        "latest_spot_vix_date": vix_pts[-1]["date"],
        "latest_vix3m": latest_vix3m,
        "latest_vix3m_date": vix3m_pts[-1]["date"],
        "spot_over_3m_ratio": spot_ratio,
    }


def fetch_market_snapshot(ep_dir: Path, window_start: str) -> dict[str, Any]:
    data_dir = ep_dir / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    series: dict[str, Any] = {}
    for key, label, sym in YAHOO_TICKERS:
        pts = fetch_yahoo_daily(sym, window_start)
        s = summarize_series(pts)
        s["label"] = label
        s["symbol"] = sym
        series[key] = s
    snapshot = {
        "fetched_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
        "window_start": window_start,
        "series": series,
        "derived": {
            "vix_term_structure": compute_vix_ratio_series(series["vix"]["points"], series["vix3m"]["points"]),
        },
    }
    (data_dir / "market_snapshot.json").write_text(json.dumps(snapshot, indent=2), encoding="utf-8")
    return snapshot


# ---------------------------------------------------------------------------
# Headless Chrome HTML -> PNG & FFmpeg Motion Graphics
# ---------------------------------------------------------------------------


def render_html_to_png(html_content: str, out_png: Path, w: int = 1920, h: int = 1080, transparent: bool = False) -> None:
    out_png.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as tf:
        tf.write(html_content)
        html_path = Path(tf.name)
    try:
        cmd = [
            CHROME_BIN,
            "--headless=new",
            "--disable-gpu",
            "--hide-scrollbars",
            f"--window-size={w},{h}",
            "--force-device-scale-factor=1",
        ]
        if transparent:
            cmd.append("--default-background-color=00000000")
        cmd.extend([f"--screenshot={out_png}", html_path.as_uri()])
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=30, check=False)
        if res.returncode != 0 or not out_png.is_file() or out_png.stat().st_size < 1_000:
            raise RuntimeError(f"Chrome screenshot failed for {out_png}: {res.stderr[:300]}")
    finally:
        html_path.unlink(missing_ok=True)


def svg_doc(w: int, h: int, body: str, bg: str | None = "#0B0E14") -> str:
    bg_css = bg if bg else "transparent"
    bg_rect = f'<rect width="{w}" height="{h}" fill="{bg}"/>' if bg else ""
    return (
        f'<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><style>'
        f"*{{box-sizing:border-box;margin:0;padding:0;}}"
        f"html,body{{width:{w}px;height:{h}px;overflow:hidden;background:{bg_css};"
        f'font-family:-apple-system,BlinkMacSystemFont,"Inter",sans-serif;}}'
        f"</style></head><body>"
        f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">'
        f"{bg_rect}{body}</svg></body></html>"
    )


def fmt_date_short(iso: str) -> str:
    return datetime.date.fromisoformat(iso).strftime("%b %-d")


def resolve_badge_positions(raw_ys: list[float], min_gap: float = 112.0, y_lo: float = 240.0, y_hi: float = 790.0) -> list[float]:
    order = sorted(range(len(raw_ys)), key=lambda idx: raw_ys[idx])
    placed = [0.0] * len(raw_ys)
    cursor = y_lo - min_gap
    for idx in order:
        y = max(y_lo, raw_ys[idx] - 46.0, cursor + min_gap)
        placed[idx] = y
        cursor = y
    if placed[order[-1]] > y_hi:
        shift = placed[order[-1]] - y_hi
        for idx in reversed(order):
            placed[idx] = max(y_lo, placed[idx] - shift)
    return placed


def render_wipe_overlay_mp4(
    base_png: Path,
    overlays: list[tuple[Path, float, float | None]],
    out_mp4: Path,
    dur: float,
    work_dir: Path,
) -> None:
    """Animate progressive horizontal wipe-in for curves/layers (when wipe_dur is set) or timed fade-in."""
    out_mp4.parent.mkdir(parents=True, exist_ok=True)
    # Build static PNG base with overlays composited sequentially
    inputs = ["-loop", "1", "-framerate", "30", "-t", f"{dur:.3f}", "-i", str(base_png)]
    filters: list[str] = []
    cur = "0:v"
    for i, (ov_png, st, wipe_dur) in enumerate(overlays, start=1):
        inputs.extend(["-loop", "1", "-framerate", "30", "-t", f"{dur:.3f}", "-i", str(ov_png)])
        if wipe_dur is not None and wipe_dur > 0.1:
            ov_lbl = f"w{i}"
            w_expr = f"if(lt(t,{st:.3f}),1,if(lt(t,{st+wipe_dur:.3f}),max(1,min(1920,1920*(t-{st:.3f})/{wipe_dur:.3f})),1920))"
            filters.append(f"[{i}:v]format=rgba,crop='{w_expr}':1080:0:0[{ov_lbl}]")
            nxt = f"o{i}"
            filters.append(f"[{cur}][{ov_lbl}]overlay=0:0:shortest=1[{nxt}]")
        else:
            ov_lbl = f"f{i}"
            filters.append(f"[{i}:v]format=rgba,fade=t=in:st={st:.3f}:d=0.35:alpha=1[{ov_lbl}]")
            nxt = f"o{i}"
            filters.append(f"[{cur}][{ov_lbl}]overlay=0:0:shortest=1[{nxt}]")
        cur = nxt
    filters.append(f"[{cur}]fps=30,format=yuv420p[outv]")
    run_ffmpeg(
        [
            *inputs,
            "-filter_complex",
            ";".join(filters),
            "-map",
            "[outv]",
            "-c:v",
            "libx264",
            "-preset",
            "fast",
            "-crf",
            "18",
            "-t",
            f"{dur:.3f}",
            str(out_mp4),
        ]
    )


def render_static_still_mp4(src_png: Path, out_mp4: Path, dur: float) -> None:
    out_mp4.parent.mkdir(parents=True, exist_ok=True)
    run_ffmpeg(
        [
            "-loop",
            "1",
            "-framerate",
            "30",
            "-t",
            f"{dur:.3f}",
            "-i",
            str(src_png),
            "-vf",
            "fps=30,format=yuv420p",
            "-c:v",
            "libx264",
            "-preset",
            "fast",
            "-crf",
            "18",
            str(out_mp4),
        ]
    )


def build_ep01_visual_assets(snap: dict[str, Any], ep_dir: Path, dur_map: dict[str, float]) -> None:
    """Render static QA PNGs under charts/ and 30fps animated MP4 cards under motion_assets/."""
    charts_dir = ep_dir / "charts"
    motion_dir = ep_dir / "motion_assets"
    charts_dir.mkdir(parents=True, exist_ok=True)
    motion_dir.mkdir(parents=True, exist_ok=True)
    s = snap["series"]
    vix_ts = snap["derived"]["vix_term_structure"]

    # ---- Beat 1B: 3 Deep Signals Intro Hook Card ----
    hook_cards = [
        ("SIGNAL 01", "Corporate Junk Credit", "HYG ETF vs Risk Assets", "#22C55E", 130),
        ("SIGNAL 02", "VIX Term Structure", "Spot Fear vs 3-Month Fear", "#E5A93B", 706),
        ("SIGNAL 03", "Dollar & Gold Turn", "US10Y Yield + DXY Anchor", "#E5484D", 1282),
    ]
    hc_svg = []
    for tag, head, sub, color, x in hook_cards:
        hc_svg.append(
            f'<rect x="{x}" y="220" width="508" height="330" rx="10" fill="#101521" stroke="{color}" stroke-width="2" stroke-opacity="0.75"/>'
            f'<rect x="{x}" y="220" width="508" height="6" rx="2" fill="{color}"/>'
            f'<text x="{x+36}" y="290" fill="{color}" font-size="22" font-weight="700" letter-spacing="2" font-family="SF Mono, Menlo, monospace">{tag}</text>'
            f'<text x="{x+36}" y="378" fill="#F8FAFC" font-size="36" font-weight="700">{html.escape(head)}</text>'
            f'<text x="{x+36}" y="440" fill="#94A3B8" font-size="23">{html.escape(sub)}</text>'
            f'<text x="{x+36}" y="498" fill="#64748B" font-size="18" font-family="SF Mono, Menlo, monospace">Institutional Diagnostic Metric</text>'
        )
    hook_base = motion_dir / "hook_16x9_base.png"
    hook_verdict = motion_dir / "hook_16x9_verdict.png"
    render_html_to_png(
        svg_doc(
            1920,
            1080,
            '<text x="130" y="142" fill="#94A3B8" font-size="24" font-weight="600" letter-spacing="3" font-family="SF Mono, Menlo, monospace">HOW MARKETS BREAK  ·  EPISODE 01 DIAGNOSTIC FRAMEWORK</text>'
            + "".join(hc_svg),
        ),
        hook_base,
    )
    render_html_to_png(
        svg_doc(
            1920,
            1080,
            '<rect x="260" y="635" width="1400" height="170" rx="10" fill="#111726" stroke="#38BDF8" stroke-width="2.5"/>'
            '<text x="960" y="708" fill="#F8FAFC" font-size="42" font-weight="700" text-anchor="middle">FORCED FLUSH OR TRUE BEAR MARKET?</text>'
            '<text x="960" y="762" fill="#94A3B8" font-size="22" font-family="SF Mono, Menlo, monospace" text-anchor="middle">PRICE ALONE LIES — THESE 3 LIQUIDITY SIGNALS REVEAL THE REGIME</text>',
            bg=None,
        ),
        hook_verdict,
        transparent=True,
    )
    render_wipe_overlay_mp4(hook_base, [(hook_verdict, 2.8, None)], motion_dir / "beat01b_hook_card.mp4", dur_map["beat01b"], motion_dir)

    # ---- Chart 01 (Beat 2): Credit Market Held (HYG vs Gold vs Bitcoin drawdown from Nov high) ----
    c01_cfg = [
        ("hyg", "High-Yield Credit (HYG)", "#22C55E", "HYG"),
        ("gold", "Gold Futures", "#E5A93B", "GC=F"),
        ("btc", "Bitcoin", "#E5484D", "BTC-USD"),
    ]
    all_dates = sorted({pt["date"] for k, *_ in c01_cfg for pt in s[k]["points"]})
    d_idx = {d: i for i, d in enumerate(all_dates)}
    W, H = 1920, 1080
    PL, PR, PT, PB = 130, 440, 230, 145
    PW, PH = W - PL - PR, H - PT - PB
    y_min, y_max = -28.0, 2.0
    x_px = lambda d: PL + (d_idx[d] / max(1, len(all_dates) - 1)) * PW
    y_px = lambda v: PT + ((y_max - v) / (y_max - y_min)) * PH

    grid = []
    for tick in [0, -5, -10, -15, -20, -25]:
        yy = y_px(float(tick))
        stroke = "#334155" if tick == 0 else "#1B2230"
        sw = "2" if tick == 0 else "1"
        dash = "" if tick == 0 else 'stroke-dasharray="4 6"'
        grid.append(f'<line x1="{PL}" y1="{yy:.1f}" x2="{PL+PW}" y2="{yy:.1f}" stroke="{stroke}" stroke-width="{sw}" {dash}/>')
        grid.append(f'<text x="{PL-22}" y="{yy+7:.1f}" fill="#8B96A8" font-size="22" font-family="SF Mono, Menlo, monospace" text-anchor="end">{tick}%</text>')
    shown = {i for i in range(0, len(all_dates), 4) if i < len(all_dates) - 2} | {len(all_dates) - 1}
    for idx in sorted(shown):
        d = all_dates[idx]
        xx = x_px(d)
        grid.append(f'<line x1="{xx:.1f}" y1="{PT}" x2="{xx:.1f}" y2="{PT+PH}" stroke="#161C27" stroke-width="1"/>')
        grid.append(f'<text x="{xx:.1f}" y="{PT+PH+42}" fill="#8B96A8" font-size="21" font-family="SF Mono, Menlo, monospace" text-anchor="middle">{html.escape(fmt_date_short(d))}</text>')

    c01_base_svg = (
        '<text x="130" y="96" fill="#22C55E" font-size="22" font-weight="700" letter-spacing="3" font-family="SF Mono, Menlo, monospace">HOW MARKETS BREAK  |  SIGNAL 01: CORPORATE JUNK CREDIT</text>'
        '<text x="130" y="148" fill="#F8FAFC" font-size="44" font-weight="700">Credit Isn’t Panicking — High-Yield Bonds Barely Budged</text>'
        '<text x="130" y="188" fill="#94A3B8" font-size="22">Normalized drawdown (%) from November 2026 peak close — true systemic bears crack junk credit first</text>'
        + "".join(grid)
        + f'<text x="130" y="1028" fill="#64748B" font-size="18" font-family="SF Mono, Menlo, monospace">Source: Yahoo Finance daily closes (HYG, GC=F, BTC-USD) · Educational market mechanics, not financial advice</text>'
    )
    c01_base_png = motion_dir / "c01_base.png"
    render_html_to_png(svg_doc(W, H, c01_base_svg), c01_base_png)

    c01_raw_ys = []
    c01_series_data = []
    for key, label, color, ticker in c01_cfg:
        ser = s[key]
        hi = ser["high_close"]
        pts_xy = [(x_px(pt["date"]), y_px((pt["close"] - hi) / hi * 100.0)) for pt in ser["points"]]
        c01_raw_ys.append(pts_xy[-1][1])
        c01_series_data.append((key, label, color, ticker, ser, pts_xy))
    badge_ys = resolve_badge_positions(c01_raw_ys, min_gap=118.0, y_lo=260.0, y_hi=780.0)

    c01_curves_pngs = []
    c01_badges_pngs = []
    full_svg_layers = []
    for idx, (key, label, color, ticker, ser, pts_xy) in enumerate(c01_series_data):
        d_attr = " ".join(("M" if i == 0 else "L") + f"{x:.1f},{y:.1f}" for i, (x, y) in enumerate(pts_xy))
        lx, ly = pts_xy[-1]
        c_svg = (
            f'<path d="{d_attr}" fill="none" stroke="{color}" stroke-width="5.5" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<circle cx="{lx:.1f}" cy="{ly:.1f}" r="9" fill="{color}" stroke="#0B0E14" stroke-width="3"/>'
        )
        by = badge_ys[idx]
        bx = PL + PW + 26
        b_svg = (
            f'<line x1="{lx:.1f}" y1="{ly:.1f}" x2="{bx}" y2="{by+48:.1f}" stroke="{color}" stroke-width="1.5" stroke-opacity="0.55" stroke-dasharray="3 3"/>'
            f'<rect x="{bx}" y="{by:.1f}" width="388" height="96" rx="8" fill="#101521" stroke="{color}" stroke-width="1.8"/>'
            f'<text x="{bx+18}" y="{by+34:.1f}" fill="{color}" font-size="21" font-weight="700">{html.escape(label)}</text>'
            f'<text x="{bx+370}" y="{by+35:.1f}" fill="#F8FAFC" font-size="26" font-weight="700" font-family="SF Mono, Menlo, monospace" text-anchor="end">{ser["pct_from_high"]:+.2f}%</text>'
            f'<text x="{bx+18}" y="{by+66:.1f}" fill="#94A3B8" font-size="17" font-family="SF Mono, Menlo, monospace">Peak ${ser["high_close"]:,.2f} -> ${ser["last_close"]:,.2f}</text>'
        )
        cp = motion_dir / f"c01_curve_{key}.png"
        bp = motion_dir / f"c01_badge_{key}.png"
        render_html_to_png(svg_doc(W, H, c_svg, bg=None), cp, transparent=True)
        render_html_to_png(svg_doc(W, H, b_svg, bg=None), bp, transparent=True)
        c01_curves_pngs.append((key, cp))
        c01_badges_pngs.append((key, bp))
        full_svg_layers.append(c_svg + b_svg)

    render_html_to_png(svg_doc(W, H, c01_base_svg + "".join(full_svg_layers)), charts_dir / "chart01_credit.png")
    c01_overlays = [
        (c01_curves_pngs[2][1], 0.2, 5.0),   # BTC curve
        (c01_badges_pngs[2][1], 4.8, None),  # BTC badge
        (c01_curves_pngs[1][1], 5.2, 4.0),   # Gold curve
        (c01_badges_pngs[1][1], 8.6, None),  # Gold badge
        (c01_curves_pngs[0][1], 9.0, 4.0),   # HYG Credit curve
        (c01_badges_pngs[0][1], 11.8, None), # HYG badge
    ]
    render_wipe_overlay_mp4(c01_base_png, c01_overlays, motion_dir / "beat02_chart01_credit.mp4", dur_map["beat02"], motion_dir)

    # ---- Chart 02 (Beat 4): VIX Term Structure Inversion ----
    v_dates = [p["date"] for p in vix_ts["aligned_points"]]
    vix_vals = [p["vix"] for p in vix_ts["aligned_points"]]
    vix3m_vals = [p["vix3m"] for p in vix_ts["aligned_points"]]
    ratio_vals = [p["ratio"] for p in vix_ts["aligned_points"]]
    PL2, PR2, PT2, PB2 = 130, 740, 250, 145
    PW2, PH2 = W - PL2 - PR2, H - PT2 - PB2
    vy_min = min(min(vix_vals), min(vix3m_vals)) - 2.0
    vy_max = max(max(vix_vals), max(vix3m_vals)) + 2.5
    vx_px = lambda i: PL2 + (i / max(1, len(v_dates) - 1)) * PW2
    vy_px = lambda v: PT2 + ((vy_max - v) / (vy_max - vy_min)) * PH2

    v_grid = []
    for tick in [16, 20, 24, 28, 32]:
        if vy_min <= tick <= vy_max:
            yy = vy_px(float(tick))
            v_grid.append(f'<line x1="{PL2}" y1="{yy:.1f}" x2="{PL2+PW2}" y2="{yy:.1f}" stroke="#1B2230" stroke-width="1" stroke-dasharray="4 6"/>')
            v_grid.append(f'<text x="{PL2-18}" y="{yy+7:.1f}" fill="#8B96A8" font-size="21" font-family="SF Mono, Menlo, monospace" text-anchor="end">{tick}</text>')
    v_shown = {i for i in range(0, len(v_dates), 4) if i < len(v_dates) - 2} | {len(v_dates) - 1}
    for idx in sorted(v_shown):
        xx = vx_px(idx)
        v_grid.append(f'<text x="{xx:.1f}" y="{PT2+PH2+42}" fill="#8B96A8" font-size="20" font-family="SF Mono, Menlo, monospace" text-anchor="middle">{html.escape(fmt_date_short(v_dates[idx]))}</text>')

    c02_base_svg = (
        '<text x="130" y="96" fill="#E5A93B" font-size="22" font-weight="700" letter-spacing="3" font-family="SF Mono, Menlo, monospace">HOW MARKETS BREAK  |  SIGNAL 02: VIX TERM STRUCTURE</text>'
        '<text x="130" y="148" fill="#F8FAFC" font-size="44" font-weight="700">Term Inversion: Near-Term Fear Spiked Above 3-Month Fear</text>'
        '<text x="130" y="188" fill="#94A3B8" font-size="22">Spot CBOE ^VIX vs 3-Month ^VIX3M — ratio above 1.00 signals acute hedging near liquidation stress</text>'
        + "".join(v_grid)
        + f'<text x="130" y="1028" fill="#64748B" font-size="18" font-family="SF Mono, Menlo, monospace">Source: Yahoo Finance (^VIX, ^VIX3M) aligned {html.escape(vix_ts["latest_aligned_date"])} (Spot ^VIX {vix_ts["latest_spot_vix"]:.2f} / 3M {vix_ts["latest_vix3m"]:.2f})</text>'
    )
    c02_base_png = motion_dir / "c02_base.png"
    render_html_to_png(svg_doc(W, H, c02_base_svg), c02_base_png)

    d_v3m = " ".join(("M" if i == 0 else "L") + f"{vx_px(i):.1f},{vy_px(v):.1f}" for i, v in enumerate(vix3m_vals))
    d_vix = " ".join(("M" if i == 0 else "L") + f"{vx_px(i):.1f},{vy_px(v):.1f}" for i, v in enumerate(vix_vals))
    v3m_svg = (
        f'<path d="{d_v3m}" fill="none" stroke="#38BDF8" stroke-width="5" stroke-linecap="round"/>'
        f'<circle cx="{vx_px(len(v_dates)-1):.1f}" cy="{vy_px(vix3m_vals[-1]):.1f}" r="8" fill="#38BDF8" stroke="#0B0E14" stroke-width="3"/>'
        f'<rect x="{PL2+20}" y="{PT2+18}" width="265" height="44" rx="6" fill="#101521" stroke="#38BDF8" stroke-opacity="0.6"/>'
        f'<text x="{PL2+38}" y="{PT2+47}" fill="#38BDF8" font-size="20" font-weight="700" font-family="SF Mono, Menlo, monospace">3M ^VIX3M: {vix3m_vals[-1]:.2f}</text>'
    )
    vix_svg = (
        f'<path d="{d_vix}" fill="none" stroke="#E5484D" stroke-width="5.5" stroke-linecap="round"/>'
        f'<circle cx="{vx_px(len(v_dates)-1):.1f}" cy="{vy_px(vix_vals[-1]):.1f}" r="9" fill="#E5484D" stroke="#0B0E14" stroke-width="3"/>'
        f'<rect x="{PL2+302}" y="{PT2+18}" width="446" height="44" rx="6" fill="#160D12" stroke="#E5484D" stroke-opacity="0.8"/>'
        f'<text x="{PL2+320}" y="{PT2+47}" fill="#E5484D" font-size="20" font-weight="700" font-family="SF Mono, Menlo, monospace">SPOT ^VIX: {vix_vals[-1]:.2f} (Last {vix_ts["latest_spot_vix"]:.2f})</text>'
    )
    rx, ry, rw, rh = 1230, 250, 560, 685
    r_lo, r_hi = 0.85, max(1.18, max(ratio_vals) + 0.04)
    r_x = lambda i: (rx + 40) + (i / max(1, len(v_dates) - 1)) * (rw - 80)
    r_y = lambda r: (ry + 590) - ((r - r_lo) / (r_hi - r_lo)) * 310
    y_100 = r_y(1.0)
    d_rat = " ".join(("M" if i == 0 else "L") + f"{r_x(i):.1f},{r_y(r):.1f}" for i, r in enumerate(ratio_vals))
    ratio_panel_svg = (
        f'<rect x="{rx}" y="{ry}" width="{rw}" height="{rh}" rx="10" fill="#101521" stroke="#E5A93B" stroke-width="2"/>'
        f'<rect x="{rx}" y="{ry}" width="{rw}" height="6" rx="2" fill="#E5A93B"/>'
        f'<text x="{rx+34}" y="{ry+58}" fill="#E5A93B" font-size="21" font-weight="700" letter-spacing="2" font-family="SF Mono, Menlo, monospace">VIX / VIX3M INVERSION RATIO</text>'
        f'<text x="{rx+34}" y="{ry+148}" fill="#F8FAFC" font-size="76" font-weight="700" font-family="SF Mono, Menlo, monospace">{vix_ts["spot_over_3m_ratio"]:.2f}x</text>'
        f'<text x="{rx+34}" y="{ry+196}" fill="#94A3B8" font-size="18" font-family="SF Mono, Menlo, monospace">Aligned: {vix_ts["latest_aligned_ratio"]:.2f}x  ·  Threshold: &gt;1.00x</text>'
        f'<line x1="{rx+34}" y1="{y_100:.1f}" x2="{rx+rw-34}" y2="{y_100:.1f}" stroke="#E5484D" stroke-width="2" stroke-dasharray="6 4"/>'
        f'<text x="{rx+rw-36}" y="{y_100+24:.1f}" fill="#E5484D" font-size="15" font-weight="700" font-family="SF Mono, Menlo, monospace" text-anchor="end">1.00 INVERSION LINE</text>'
        f'<path d="{d_rat}" fill="none" stroke="#E5A93B" stroke-width="5" stroke-linecap="round"/>'
        f'<circle cx="{r_x(len(v_dates)-1):.1f}" cy="{r_y(ratio_vals[-1]):.1f}" r="8" fill="#E5A93B" stroke="#0B0E14" stroke-width="3"/>'
        f'<text x="{rx+34}" y="{ry+644}" fill="#94A3B8" font-size="19">Status: AMBER — acute stress hedging active</text>'
    )
    c02_v3m_png = motion_dir / "c02_v3m.png"
    c02_vix_png = motion_dir / "c02_vix.png"
    c02_rat_png = motion_dir / "c02_ratio.png"
    render_html_to_png(svg_doc(W, H, v3m_svg, bg=None), c02_v3m_png, transparent=True)
    render_html_to_png(svg_doc(W, H, vix_svg, bg=None), c02_vix_png, transparent=True)
    render_html_to_png(svg_doc(W, H, ratio_panel_svg, bg=None), c02_rat_png, transparent=True)
    render_html_to_png(svg_doc(W, H, c02_base_svg + v3m_svg + vix_svg + ratio_panel_svg), charts_dir / "chart02_vix.png")
    render_wipe_overlay_mp4(
        c02_base_png,
        [(c02_v3m_png, 0.2, 4.0), (c02_vix_png, 4.2, 4.5), (c02_rat_png, 7.8, None)],
        motion_dir / "beat04_chart02_vix.mp4",
        dur_map["beat04"],
        motion_dir,
    )

    # ---- Chart 03 (Beat 5B): Missing Green Light — US10Y Yield, Dollar Index & Gold ----
    c03_base_svg = (
        '<text x="110" y="96" fill="#E5484D" font-size="22" font-weight="700" letter-spacing="3" font-family="SF Mono, Menlo, monospace">HOW MARKETS BREAK  |  SIGNAL 03: THE MISSING GREEN LIGHT</text>'
        '<text x="110" y="148" fill="#F8FAFC" font-size="44" font-weight="700">Yields Eased Off 5.15% Peak — But Dollar Near 104 Still Crushes Gold</text>'
        '<text x="110" y="188" fill="#94A3B8" font-size="22">Daily closes across US 10-Year Yield (^TNX), U.S. Dollar Index (DXY), and Gold Futures (GC=F)</text>'
        '<text x="110" y="1028" fill="#64748B" font-size="18" font-family="SF Mono, Menlo, monospace">Source: Yahoo Finance daily closes · Watch Signal 3: DXY rollover below 102 + Gold decoupling higher</text>'
    )
    c03_base_png = motion_dir / "c03_base.png"
    render_html_to_png(svg_doc(W, H, c03_base_svg), c03_base_png)

    p_specs = [
        ("us10y", "10Y US TREASURY YIELD", "Eased off 5.15% peak to 5.05%", f"{s['us10y']['last_close']:.2f}%", f"Low {s['us10y']['low_close']:.2f}% -> Peak {s['us10y']['high_close']:.2f}%", "#38BDF8", True),
        ("dxy", "US DOLLAR INDEX (DXY)", "Pinned near 104 resistance ceiling", f"{s['dxy']['last_close']:.2f}", f"{s['dxy']['first_close']:.2f} ({fmt_date_short(s['dxy']['first_date'])}) -> {s['dxy']['last_close']:.2f}", "#E5484D", False),
        ("gold", "GOLD FUTURES (GC=F)", "Still pressured by strong Dollar", f"${s['gold']['last_close']:,.0f}", f"{s['gold']['pct_from_high']:+.2f}% from peak ${s['gold']['high_close']:,.0f}", "#E5A93B", False),
    ]
    c03_panels_pngs = []
    c03_panels_all_svg = []
    pw, ph, py0, gap = 540, 720, 235, 40
    for idx, (key, ttl, sub, big_val, delta_txt, color, draw_peak_line) in enumerate(p_specs):
        px0 = 110 + idx * (pw + gap)
        pts = s[key]["points"]
        vals = [p["close"] for p in pts]
        vmin, vmax = min(vals), max(vals)
        pad = max(0.05, (vmax - vmin) * 0.18)
        lo, hi = vmin - pad, vmax + pad
        x0, x1, y0, y1 = px0 + 68, px0 + pw - 28, py0 + 215, py0 + ph - 72
        px_fn = lambda j: x0 + (j / max(1, len(pts) - 1)) * (x1 - x0)
        py_fn = lambda v: y0 + ((hi - v) / max(1e-6, hi - lo)) * (y1 - y0)

        p_grid = []
        for frac in (0.0, 0.5, 1.0):
            gv = lo + frac * (hi - lo)
            gy = py_fn(gv)
            glbl = f"{gv:.2f}%" if key == "us10y" else (f"{gv:,.0f}" if key == "gold" else f"{gv:.1f}")
            p_grid.append(f'<line x1="{x0}" y1="{gy:.1f}" x2="{x1}" y2="{gy:.1f}" stroke="#1B2230" stroke-width="1"/>')
            p_grid.append(f'<text x="{x0-10}" y="{gy+5:.1f}" fill="#64748B" font-size="16" font-family="SF Mono, Menlo, monospace" text-anchor="end">{glbl}</text>')
        if draw_peak_line:
            y5 = py_fn(5.0)
            p_grid.append(f'<line x1="{x0}" y1="{y5:.1f}" x2="{x1}" y2="{y5:.1f}" stroke="#E5A93B" stroke-width="1.5" stroke-dasharray="5 4"/>')
            p_grid.append(f'<text x="{x1}" y="{y5-8:.1f}" fill="#E5A93B" font-size="15" font-weight="700" font-family="SF Mono, Menlo, monospace" text-anchor="end">5.00% HURDLE</text>')
        d_line = " ".join(("M" if j == 0 else "L") + f"{px_fn(j):.1f},{py_fn(v):.1f}" for j, v in enumerate(vals))
        d_area = f"{d_line} L{px_fn(len(pts)-1):.1f},{y1:.1f} L{px_fn(0):.1f},{y1:.1f} Z"
        p_svg = (
            f'<rect x="{px0}" y="{py0}" width="{pw}" height="{ph}" rx="10" fill="#101521" stroke="#1E293B" stroke-width="1.5"/>'
            f'<rect x="{px0}" y="{py0}" width="{pw}" height="5" rx="2" fill="{color}"/>'
            f'<text x="{px0+28}" y="{py0+46}" fill="{color}" font-size="20" font-weight="700" letter-spacing="1.5" font-family="SF Mono, Menlo, monospace">{ttl}</text>'
            f'<text x="{px0+28}" y="{py0+76}" fill="#94A3B8" font-size="18">{html.escape(sub)}</text>'
            f'<text x="{px0+28}" y="{py0+136}" fill="#F8FAFC" font-size="52" font-weight="700" font-family="SF Mono, Menlo, monospace">{html.escape(big_val)}</text>'
            f'<text x="{px0+28}" y="{py0+170}" fill="#94A3B8" font-size="18" font-family="SF Mono, Menlo, monospace">{html.escape(delta_txt)}</text>'
            + "".join(p_grid)
            + f'<path d="{d_area}" fill="{color}" fill-opacity="0.12"/>'
            f'<path d="{d_line}" fill="none" stroke="{color}" stroke-width="4" stroke-linecap="round"/>'
            f'<circle cx="{px_fn(len(pts)-1):.1f}" cy="{py_fn(vals[-1]):.1f}" r="7" fill="{color}" stroke="#0B0E14" stroke-width="2.5"/>'
            f'<text x="{x0}" y="{y1+34}" fill="#64748B" font-size="16" font-family="SF Mono, Menlo, monospace">{html.escape(fmt_date_short(pts[0]["date"]))}</text>'
            f'<text x="{x1}" y="{y1+34}" fill="#64748B" font-size="16" font-family="SF Mono, Menlo, monospace" text-anchor="end">{html.escape(fmt_date_short(pts[-1]["date"]))}</text>'
        )
        pp = motion_dir / f"c03_panel_{idx}.png"
        render_html_to_png(svg_doc(W, H, p_svg, bg=None), pp, transparent=True)
        c03_panels_pngs.append(pp)
        c03_panels_all_svg.append(p_svg)

    render_html_to_png(svg_doc(W, H, c03_base_svg + "".join(c03_panels_all_svg)), charts_dir / "chart03_dxy_gold.png")
    render_wipe_overlay_mp4(
        c03_base_png,
        [(c03_panels_pngs[0], 0.2, None), (c03_panels_pngs[1], 3.2, None), (c03_panels_pngs[2], 6.0, None)],
        motion_dir / "beat05b_chart03_dxy_gold.mp4",
        dur_map["beat05b"],
        motion_dir,
    )

    # ---- Beat 6B: Diagnostic Scoreboard (GREEN / AMBER / RED -> Verdict) ----
    sb_base_svg = (
        '<text x="130" y="96" fill="#38BDF8" font-size="22" font-weight="700" letter-spacing="3" font-family="SF Mono, Menlo, monospace">HOW MARKETS BREAK  |  REGIME DIAGNOSTIC SCOREBOARD</text>'
        '<text x="130" y="148" fill="#F8FAFC" font-size="44" font-weight="700">Credit Is Green, Volatility Is Amber, Dollar Is Red</text>'
    )
    sb_cols = [
        ("SIGNAL 01 · JUNK CREDIT", "GREEN", "#22C55E", "#0C1D14", f"HYG {s['hyg']['pct_from_high']:+.2f}% from peak", "No systemic corporate default wave", 130),
        ("SIGNAL 02 · VIX / VIX3M", "AMBER", "#E5A93B", "#1A140B", f"Ratio {vix_ts['spot_over_3m_ratio']:.2f}x (>1.00 inverted)", "Acute hedging near liquidation stress", 706),
        ("SIGNAL 03 · DOLLAR & GOLD", "RED", "#E5484D", "#1A0E12", f"DXY {s['dxy']['last_close']:.2f} · Gold {s['gold']['pct_from_high']:+.2f}%", "Dollar ceiling hasn't rolled over yet", 1282),
    ]
    sb_pngs = []
    sb_all = []
    for i, (kicker, badge, color, fillbg, stat, note, x) in enumerate(sb_cols):
        card_svg = (
            f'<rect x="{x}" y="220" width="508" height="390" rx="10" fill="{fillbg}" stroke="{color}" stroke-width="2.2"/>'
            f'<rect x="{x}" y="220" width="508" height="6" rx="2" fill="{color}"/>'
            f'<text x="{x+34}" y="284" fill="#94A3B8" font-size="20" font-weight="700" letter-spacing="1.5" font-family="SF Mono, Menlo, monospace">{kicker}</text>'
            f'<text x="{x+34}" y="388" fill="{color}" font-size="68" font-weight="700" font-family="SF Mono, Menlo, monospace">{badge}</text>'
            f'<text x="{x+34}" y="466" fill="#F8FAFC" font-size="26" font-weight="700">{html.escape(stat)}</text>'
            f'<text x="{x+34}" y="522" fill="#94A3B8" font-size="22">{html.escape(note)}</text>'
        )
        sp = motion_dir / f"sb_card_{i}.png"
        render_html_to_png(svg_doc(W, H, card_svg, bg=None), sp, transparent=True)
        sb_pngs.append(sp)
        sb_all.append(card_svg)
    verdict_svg = (
        '<rect x="130" y="670" width="1660" height="175" rx="10" fill="#101521" stroke="#38BDF8" stroke-width="2"/>'
        '<text x="960" y="742" fill="#F8FAFC" font-size="40" font-weight="700" text-anchor="middle">VERDICT: LIQUIDITY FLUSH — NOT A STRUCTURAL BEAR MARKET YET</text>'
        '<text x="960" y="796" fill="#94A3B8" font-size="22" font-family="SF Mono, Menlo, monospace" text-anchor="middle">Next Green Light Required: DXY Rolling Below 102 + Gold Reclaiming Safe-Haven Bid</text>'
    )
    sb_v_png = motion_dir / "sb_verdict.png"
    render_html_to_png(svg_doc(W, H, verdict_svg, bg=None), sb_v_png, transparent=True)
    render_html_to_png(svg_doc(W, H, sb_base_svg + "".join(sb_all) + verdict_svg), charts_dir / "card_scoreboard.png")
    sb_base_png = motion_dir / "sb_base.png"
    render_html_to_png(svg_doc(W, H, sb_base_svg), sb_base_png)
    render_wipe_overlay_mp4(
        sb_base_png,
        [(sb_pngs[0], 0.2, None), (sb_pngs[1], 1.8, None), (sb_pngs[2], 3.4, None), (sb_v_png, 5.2, None)],
        motion_dir / "beat06b_scoreboard.mp4",
        dur_map["beat06b"],
        motion_dir,
    )

    # ---- Beat 7B: End Slate ----
    end_png = motion_dir / "end_slate_16x9.png"
    render_html_to_png(
        svg_doc(
            W,
            H,
            '<rect x="260" y="210" width="1400" height="660" rx="14" fill="#101521" stroke="#1E293B" stroke-width="2"/>'
            '<text x="960" y="340" fill="#E5A93B" font-size="24" font-weight="700" letter-spacing="4" font-family="SF Mono, Menlo, monospace" text-anchor="middle">NEXT IN EPISODE 02</text>'
            '<text x="960" y="438" fill="#F8FAFC" font-size="68" font-weight="700" text-anchor="middle">HOW MARKETS BREAK</text>'
            '<line x1="620" y1="484" x2="1300" y2="484" stroke="#E5A93B" stroke-width="3"/>'
            '<text x="960" y="556" fill="#CBD5E1" font-size="30" text-anchor="middle">How Margin Calls Cascade Across Portfolios in Real Time</text>'
            '<rect x="740" y="628" width="440" height="72" rx="8" fill="#172033" stroke="#38BDF8" stroke-width="2"/>'
            '<text x="960" y="673" fill="#38BDF8" font-size="24" font-weight="700" letter-spacing="2" font-family="SF Mono, Menlo, monospace" text-anchor="middle">SUBSCRIBE FOR EPISODE 02</text>'
            '<text x="960" y="818" fill="#64748B" font-size="19" font-family="SF Mono, Menlo, monospace" text-anchor="middle">Educational market mechanics &amp; public data breakdown · Not financial advice · Contains AI-assisted visuals &amp; narration</text>',
        ),
        end_png,
    )
    render_static_still_mp4(end_png, motion_dir / "beat07b_end_slate.mp4", dur_map["beat07b"])


# ---------------------------------------------------------------------------
# Voiceover Synthesis & Local Flow Music Library Mixer ($0.00 GCP)
# ---------------------------------------------------------------------------


def split_caption_phrases(text: str, max_chars: int = 58) -> list[str]:
    raw_clauses = re.split(r"(?<=[.?!—])\s+", text.strip())
    phrases: list[str] = []
    for clause in raw_clauses:
        clause = clause.strip()
        if not clause:
            continue
        if len(clause) <= max_chars:
            phrases.append(clause)
            continue
        cur = ""
        for w in clause.split(" "):
            cand = f"{cur} {w}".strip() if cur else w
            if len(cand) <= max_chars:
                cur = cand
            else:
                if cur:
                    phrases.append(cur)
                cur = w
        if cur:
            phrases.append(cur)
    return phrases


def align_phrases_to_words(phrases: list[str], word_events: list[dict[str, Any]], total_dur: float) -> list[dict[str, Any]]:
    if not word_events:
        total_chars = sum(max(1, len(p)) for p in phrases)
        cues = []
        t = 0.0
        for p in phrases:
            dt = total_dur * (max(1, len(p)) / total_chars)
            cues.append({"start": round(t, 3), "end": round(min(total_dur, t + dt), 3), "text": p})
            t += dt
        if cues:
            cues[-1]["end"] = round(total_dur, 3)
        return cues

    cues: list[dict[str, Any]] = []
    w_idx = 0
    n_words = len(word_events)
    for i, phrase in enumerate(phrases):
        tokens = re.findall(r"[A-Za-z0-9']+", phrase)
        take = max(1, len(tokens))
        start_idx = min(w_idx, n_words - 1)
        end_idx = min(n_words - 1, start_idx + take - 1)
        start_s = 0.0 if i == 0 else float(word_events[start_idx]["start"])
        if i == len(phrases) - 1:
            end_s = total_dur
        else:
            next_start = float(word_events[min(n_words - 1, end_idx + 1)]["start"])
            own_end = float(word_events[end_idx]["end"])
            end_s = max(own_end, (own_end + next_start) / 2.0)
        cues.append({"start": round(start_s, 3), "end": round(min(total_dur, max(start_s + 0.2, end_s)), 3), "text": phrase})
        w_idx = min(n_words - 1, end_idx + 1)
    return cues


async def synth_beats_async(spec: dict[str, Any], ep_dir: Path) -> dict[str, Any]:
    import edge_tts

    voice_cfg = spec["voice"]
    beats_dir = ep_dir / "audio" / "beats"
    beats_dir.mkdir(parents=True, exist_ok=True)
    out_beats: list[dict[str, Any]] = []

    for beat in spec["beats"]:
        bid = beat["beat_id"]
        text = beat["text"]
        mp3_path = beats_dir / f"{bid}.mp3"
        wav_path = beats_dir / f"{bid}.wav"
        meta_path = beats_dir / f"{bid}.json"

        if meta_path.is_file() and wav_path.is_file() and wav_path.stat().st_size > 10_000:
            cached = json.loads(meta_path.read_text(encoding="utf-8"))
            if cached.get("text") == text:
                out_beats.append(cached)
                continue

        audio_chunks: list[bytes] = []
        word_events: list[dict[str, Any]] = []
        last_err: Exception | None = None
        prosody_tiers = (
            (voice_cfg["rate"], voice_cfg["pitch"], "WordBoundary"),
            (voice_cfg["rate"], "+0Hz", "WordBoundary"),
            ("+0%", "+0Hz", "WordBoundary"),
            ("+0%", "+0Hz", "SentenceBoundary"),
        )
        for attempt, (try_rate, try_pitch, try_boundary) in enumerate(prosody_tiers):
            try:
                audio_chunks = []
                word_events = []
                tts_text = text.replace(" — ", ", ").replace("—", ", ")
                comm = edge_tts.Communicate(
                    tts_text,
                    voice_cfg["name"],
                    rate=try_rate,
                    pitch=try_pitch,
                    boundary=try_boundary,
                )

                async def _collect() -> None:
                    async for chunk in comm.stream():
                        ctype = chunk.get("type")
                        if ctype == "audio":
                            audio_chunks.append(chunk["data"])
                        elif ctype == "WordBoundary":
                            st = float(chunk["offset"]) / 10_000_000.0
                            du = float(chunk["duration"]) / 10_000_000.0
                            word_events.append({"text": chunk["text"], "start": st, "end": st + du})

                await asyncio.wait_for(_collect(), timeout=20.0)
                if audio_chunks:
                    break
            except Exception as exc:
                last_err = exc
                await asyncio.sleep(1.5 * (attempt + 1))
        else:
            raise RuntimeError(f"edge-tts failed for {bid}: {last_err}")

        mp3_path.write_bytes(b"".join(audio_chunks))
        run_ffmpeg(["-i", str(mp3_path), "-ar", "48000", "-ac", "1", "-c:a", "pcm_s16le", str(wav_path)])
        dur = ffprobe_info(wav_path)["duration"]
        cues = align_phrases_to_words(split_caption_phrases(text), word_events, dur)
        meta = {
            "beat_id": bid,
            "wav": str(wav_path),
            "mp3": str(mp3_path),
            "duration_sec": round(dur, 3),
            "text": text,
            "word_count": len(word_events),
            "cues": cues,
        }
        meta_path.write_text(json.dumps(meta, indent=2), encoding="utf-8")
        print(f"VOICEOVER_BEAT_OK: {bid} ({dur:.2f}s)", flush=True)
        out_beats.append(meta)
        await asyncio.sleep(0.8)

    timeline = {
        "voice": voice_cfg["name"],
        "rate": voice_cfg["rate"],
        "pitch": voice_cfg["pitch"],
        "pause_between_beats_sec": float(voice_cfg.get("pause_between_beats_sec", 0.45)),
        "beats": out_beats,
    }
    (ep_dir / "audio" / "voiceover_timeline.json").write_text(json.dumps(timeline, indent=2), encoding="utf-8")
    return timeline


def resolve_music_segments(spec: dict[str, Any], repo_root: Path = REPO_ROOT) -> list[dict[str, Any]]:
    """Resolve Flow Music local library tracks from CATALOG.json strictly ($0.00 GCP)."""
    cat_rel = spec.get("music_library_catalog")
    if not cat_rel:
        raise ValueError("episode_spec missing music_library_catalog")
    cat_path = Path(cat_rel) if Path(cat_rel).is_absolute() else (repo_root / cat_rel)
    if not cat_path.is_file():
        raise FileNotFoundError(f"Music library catalog not found: {cat_path}")
    catalog = json.loads(cat_path.read_text(encoding="utf-8"))
    if float(catalog.get("gcp_spend_usd", 0.0)) != 0.0:
        raise ValueError("Music catalog gcp_spend_usd must be 0.0")
    by_id = {t["id"]: t for t in catalog.get("tracks", [])}
    lib_dir = cat_path.parent

    resolved: list[dict[str, Any]] = []
    for seg in spec.get("music_segments", []):
        tid = seg["track_id"]
        if tid not in by_id:
            raise KeyError(f"Track '{tid}' not in catalog {cat_path}")
        wav_path = lib_dir / by_id[tid]["file"]
        if not wav_path.is_file():
            raise FileNotFoundError(f"Missing local Flow Music WAV file: {wav_path}")
        resolved.append(
            {
                "track_id": tid,
                "wav_path": wav_path,
                "start_sec": float(seg.get("start_sec", 0.0)),
                "duration_sec": float(seg.get("duration_sec", 25.0)),
            }
        )
    if not resolved:
        raise ValueError("No music_segments configured in episode_spec")
    return resolved


def build_flow_music_score(spec: dict[str, Any], ep_dir: Path) -> Path:
    """Build multi-track Flow Music score via smooth acrossfade transitions ($0.00 GCP)."""
    segs = resolve_music_segments(spec)
    xfade = float(spec.get("crossfade_sec", 2.0))
    out_wav = ep_dir / "audio" / "flow_music_score.wav"
    out_wav.parent.mkdir(parents=True, exist_ok=True)

    inputs: list[str] = []
    fc: list[str] = []
    for idx, seg in enumerate(segs):
        inputs.extend(["-ss", f"{seg['start_sec']:.3f}", "-t", f"{seg['duration_sec']:.3f}", "-i", str(seg["wav_path"])])
        fc.append(f"[{idx}:a]aformat=sample_rates=48000:channel_layouts=stereo[s{idx}]")

    if len(segs) == 1:
        fc.append("[s0]anull[outa]")
    else:
        cur = "s0"
        for idx in range(1, len(segs)):
            nxt = f"xf{idx}" if idx < len(segs) - 1 else "outa"
            fc.append(f"[{cur}][s{idx}]acrossfade=d={xfade:.2f}:c1=tri:c2=tri[{nxt}]")
            cur = nxt

    run_ffmpeg([*inputs, "-filter_complex", ";".join(fc), "-map", "[outa]", "-c:a", "pcm_s16le", str(out_wav)])
    return out_wav


# ---------------------------------------------------------------------------
# Overflow-Proof Subtitle Rendering & Final Mastering
# ---------------------------------------------------------------------------


def normalize_cues(raw_cues: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Merge awkward 'U.S.' splits and short orphan words while never chaining across sentence endings."""
    merged: list[dict[str, Any]] = []
    for cue in raw_cues:
        txt = str(cue["text"]).strip()
        if not merged:
            merged.append({"start": float(cue["start"]), "end": float(cue["end"]), "text": txt})
            continue
        prev = merged[-1]["text"]
        combined_len = len(prev) + 1 + len(txt)
        is_us_abbr = prev == "U.S." or prev.endswith(" U.S.")
        sentence_ended = prev.endswith((".", "?", "!")) and not is_us_abbr
        should_merge = is_us_abbr or (not sentence_ended and combined_len <= 72 and (len(txt) < 14 or combined_len <= 52))
        if should_merge:
            merged[-1]["text"] = f"{prev} {txt}"
            merged[-1]["end"] = float(cue["end"])
        else:
            merged.append({"start": float(cue["start"]), "end": float(cue["end"]), "text": txt})
    return merged


def wrap_lines(text: str, max_line: int = 44) -> list[str]:
    if len(text) <= max_line:
        return [text]
    words = text.split(" ")
    if len(words) <= 1:
        return [text]
    if len(text) <= max_line * 2 + 10:
        best_split = len(words) // 2
        best_diff = 999
        for k in range(1, len(words)):
            l1, l2 = " ".join(words[:k]), " ".join(words[k:])
            if max(len(l1), len(l2)) <= max_line + 8:
                diff = abs(len(l1) - len(l2))
                if diff < best_diff:
                    best_diff = diff
                    best_split = k
        return [" ".join(words[:best_split]), " ".join(words[best_split:])]
    lines: list[str] = []
    cur = words[0]
    for w_tok in words[1:]:
        if len(cur) + 1 + len(w_tok) <= max_line:
            cur = f"{cur} {w_tok}"
        else:
            lines.append(cur)
            cur = w_tok
    lines.append(cur)
    return lines


def load_pil_font(size: int, bold: bool = False) -> Any:
    from PIL import ImageFont

    for fp in FONT_PATHS:
        if Path(fp).is_file():
            try:
                idx = 1 if (bold and fp.endswith("HelveticaNeue.ttc")) else 0
                return ImageFont.truetype(fp, size=size, index=idx)
            except Exception:
                try:
                    return ImageFont.truetype(fp, size=size)
                except Exception:
                    continue
    return ImageFont.load_default()


def make_subtitle_png(text: str, out_png: Path, w: int, h: int, bottom_margin: int, font_size: int) -> None:
    from PIL import Image, ImageDraw

    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    pad_x, pad_y, line_gap = 28, 16, 10
    max_box_w = w - 96

    cur_size = font_size
    lines = wrap_lines(text, max_line=44 if w == 1920 else 28)
    while True:
        font = load_pil_font(cur_size, bold=True)
        line_boxes = [draw.textbbox((0, 0), ln, font=font) for ln in lines]
        line_widths = [b[2] - b[0] for b in line_boxes]
        box_w = max(line_widths) + pad_x * 2
        if box_w <= max_box_w or cur_size <= 26:
            break
        cur_size -= 2

    line_heights = [b[3] - b[1] for b in line_boxes]
    box_h = sum(line_heights) + line_gap * (len(lines) - 1) + pad_y * 2
    bx0, by0 = (w - box_w) // 2, h - bottom_margin - box_h
    draw.rounded_rectangle(
        [bx0, by0, bx0 + box_w, by0 + box_h],
        radius=10,
        fill=(11, 14, 20, 215),
        outline=(56, 72, 98, 170),
        width=2,
    )
    cy = by0 + pad_y
    for ln, lw, lh, bbox in zip(lines, line_widths, line_heights, line_boxes):
        draw.text(((w - lw) // 2 - bbox[0], cy - bbox[1]), ln, font=font, fill=(248, 250, 252, 255))
        cy += lh + line_gap
    img.save(out_png)


def make_vertical_header_png(out_png: Path, title: str, kicker: str) -> None:
    from PIL import Image, ImageDraw

    img = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.text((72, 230), kicker, font=load_pil_font(28, bold=True), fill=(229, 169, 59, 255))
    y = 284
    for ln in wrap_lines(title, max_line=26):
        draw.text((72, y), ln, font=load_pil_font(54, bold=True), fill=(248, 250, 252, 255))
        y += 66
    img.save(out_png)


def compute_segment_durations(timeline: dict[str, Any]) -> dict[str, float]:
    """Derive deterministic beat + card durations from voiceover timeline before Flow renders exist."""
    pause = float(timeline.get("pause_between_beats_sec", 0.45))
    b = {x["beat_id"]: float(x["duration_sec"]) for x in timeline["beats"]}
    return {
        "beat01a": 6.0,
        "beat01b": max(4.0, b["beat01"] + pause - 6.0),
        "beat02": b["beat02"] + pause,
        "beat03": b["beat03"] + pause,
        "beat04": b["beat04"] + pause,
        "beat05a": 6.0,
        "beat05b": max(4.5, b["beat05"] + pause - 6.0),
        "beat06a": 6.0,
        "beat06b": max(4.5, b["beat06"] + pause - 6.0),
        "beat07a": 6.5,
        "beat07b": max(4.5, b["beat07"] + 2.5 - 6.5),
    }


def prepare_flow_clip(src_mp4: Path, dst_mp4: Path, target_dur: float, foley_wav: Path, mode: str) -> None:
    info = ffprobe_info(src_mp4)
    start_ss = 0.25 if info["duration"] - 0.25 >= target_dur * 0.85 else 0.0
    avail = max(0.5, info["duration"] - start_ss)
    scale_crop = (
        "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,setsar=1"
        if mode == "16x9"
        else "scale=-1:1920:force_original_aspect_ratio=increase,crop=1080:1920:(iw-1080)/2:0,setsar=1"
    )
    pad_s = max(0.0, target_dur - avail)
    vf = f"{scale_crop},eq=contrast=1.06:brightness=-0.02:gamma=0.94:saturation=1.02,fps=30"
    if pad_s > 0.02:
        vf += f",tpad=stop_mode=clone:stop_duration={pad_s:.3f}"
    vf += f",trim=duration={target_dur:.3f},setpts=PTS-STARTPTS,format=yuv420p"
    run_ffmpeg(["-ss", f"{start_ss:.3f}", "-i", str(src_mp4), "-an", "-vf", vf, "-c:v", "libx264", "-preset", "fast", "-crf", "18", str(dst_mp4)])
    if info["has_audio"]:
        af = (
            f"aformat=sample_rates=48000:channel_layouts=stereo,apad=whole_dur={target_dur:.3f},"
            f"atrim=duration={target_dur:.3f},afade=t=in:st=0:d=0.15,afade=t=out:st={max(0.0, target_dur-0.2):.3f}:d=0.2"
        )
        run_ffmpeg(["-ss", f"{start_ss:.3f}", "-i", str(src_mp4), "-vn", "-af", af, "-c:a", "pcm_s16le", str(foley_wav)])
    else:
        run_ffmpeg(["-f", "lavfi", "-i", f"anullsrc=r=48000:cl=stereo:d={target_dur:.3f}", "-c:a", "pcm_s16le", str(foley_wav)])


def adjust_motion_clip(src_mp4: Path, dst_mp4: Path, target_dur: float, mode: str, header_png: Path | None) -> None:
    info = ffprobe_info(src_mp4)
    pad_s = max(0.0, target_dur - info["duration"])
    if mode == "16x9":
        vf = "fps=30"
        if pad_s > 0.02:
            vf += f",tpad=stop_mode=clone:stop_duration={pad_s:.3f}"
        vf += f",trim=duration={target_dur:.3f},setpts=PTS-STARTPTS,format=yuv420p"
        run_ffmpeg(["-i", str(src_mp4), "-an", "-vf", vf, "-c:v", "libx264", "-preset", "fast", "-crf", "18", str(dst_mp4)])
    else:
        vf_base = "scale=1080:608:flags=lanczos,fps=30"
        if pad_s > 0.02:
            vf_base += f",tpad=stop_mode=clone:stop_duration={pad_s:.3f}"
        vf_base += f",trim=duration={target_dur:.3f},setpts=PTS-STARTPTS,pad=1080:1920:0:656:color=0x0B0E14"
        if header_png is not None:
            run_ffmpeg(
                [
                    "-i", str(src_mp4),
                    "-loop", "1", "-framerate", "30", "-t", f"{target_dur:.3f}", "-i", str(header_png),
                    "-an", "-filter_complex", f"[0:v]{vf_base}[bg];[bg][1:v]overlay=0:0:shortest=1,format=yuv420p",
                    "-c:v", "libx264", "-preset", "fast", "-crf", "18", str(dst_mp4),
                ]
            )
        else:
            run_ffmpeg(["-i", str(src_mp4), "-an", "-vf", f"{vf_base},format=yuv420p", "-c:v", "libx264", "-preset", "fast", "-crf", "18", str(dst_mp4)])


def cmd_prepare(spec_path: Path) -> None:
    spec, ep_dir = load_spec(spec_path)
    gate = enforce_manifest_gate(ep_dir)
    print(f"COMPLIANCE_GATE_PASS: {gate}")

    snap = fetch_market_snapshot(ep_dir, spec.get("window_start", "2026-11-02"))
    print(f"MARKET_SNAPSHOT_OK: {len(snap['series'])} series fetched")

    timeline = asyncio.run(synth_beats_async(spec, ep_dir))
    dur_map = compute_segment_durations(timeline)
    print(f"VOICEOVER_OK: {len(timeline['beats'])} beats synthesized")

    build_ep01_visual_assets(snap, ep_dir, dur_map)
    print("VISUAL_ASSETS_OK: charts + 6 motion cards rendered")

    score_wav = build_flow_music_score(spec, ep_dir)
    s_info = ffprobe_info(score_wav)
    print(f"FLOW_MUSIC_SCORE_OK: {score_wav} ({s_info['duration']:.2f}s, {s_info['sample_rate']}Hz, {s_info['channels']}ch, $0.00 GCP)")

    prompts_doc = {
        "episode_id": spec["episode_id"],
        "project_name": f"{spec['channel']} {spec['episode_id']}",
        "flow_settings": {
            "mode": "Video",
            "video_type": "Ingredients",
            "aspect_ratio": "16:9",
            "model": "Omni 1.2 Flash",
            "resolution": "720p",
            "duration_sec": 8,
            "outputs_per_prompt": "x1",
        },
        "zero_confirmation_mode": True,
        "shots": spec["flow_shots"],
    }
    (ep_dir / "flow_prompts.json").write_text(json.dumps(prompts_doc, indent=2), encoding="utf-8")
    print(f"PREPARE_COMPLETE: ready for zero-upload Flow Cinema generation ({ep_dir / 'flow_prompts.json'})")


def build_track_for_mode(spec: dict[str, Any], ep_dir: Path, mode: str, work_dir: Path, timeline: dict[str, Any], score_wav: Path) -> Path:
    dur_map = compute_segment_durations(timeline)
    beats_by_id = {b["beat_id"]: b for b in timeline["beats"]}
    renders_dir = ep_dir / "renders"
    motion_dir = ep_dir / "motion_assets"
    out_dir = ep_dir / "output"
    out_dir.mkdir(parents=True, exist_ok=True)

    flow_paths = {i: renders_dir / f"shot0{i}_flow.mp4" for i in range(1, 6)}
    for i, p in flow_paths.items():
        if not p.is_file():
            raise FileNotFoundError(f"Missing Flow render: {p}")
        info = ffprobe_info(p)
        if not info["has_video"] or info["duration"] < 4.0 or info["width"] < 640:
            raise RuntimeError(f"Invalid Flow render {p}: {info}")

    hdrs: dict[str, Path] = {}
    if mode == "9x16":
        for key, meta in spec.get("vertical_headers", {}).items():
            hp = work_dir / f"hdr_{key}.png"
            make_vertical_header_png(hp, meta["title"], meta["kicker"])
            hdrs[key] = hp

    segs = [
        ("flow", flow_paths[1], dur_map["beat01a"], "seg01a", None),
        ("motion", motion_dir / "beat01b_hook_card.mp4", dur_map["beat01b"], "seg01b", hdrs.get("beat01b")),
        ("motion", motion_dir / "beat02_chart01_credit.mp4", dur_map["beat02"], "seg02", hdrs.get("beat02")),
        ("flow", flow_paths[2], dur_map["beat03"], "seg03", None),
        ("motion", motion_dir / "beat04_chart02_vix.mp4", dur_map["beat04"], "seg04", hdrs.get("beat04")),
        ("flow", flow_paths[3], dur_map["beat05a"], "seg05a", None),
        ("motion", motion_dir / "beat05b_chart03_dxy_gold.mp4", dur_map["beat05b"], "seg05b", hdrs.get("beat05b")),
        ("flow", flow_paths[4], dur_map["beat06a"], "seg06a", None),
        ("motion", motion_dir / "beat06b_scoreboard.mp4", dur_map["beat06b"], "seg06b", hdrs.get("beat06b")),
        ("flow", flow_paths[5], dur_map["beat07a"], "seg07a", None),
        ("motion", motion_dir / "beat07b_end_slate.mp4", dur_map["beat07b"], "seg07b", None),
    ]

    beat_starts = {"beat01": 0.0}
    beat_starts["beat02"] = dur_map["beat01a"] + dur_map["beat01b"]
    beat_starts["beat03"] = beat_starts["beat02"] + dur_map["beat02"]
    beat_starts["beat04"] = beat_starts["beat03"] + dur_map["beat03"]
    beat_starts["beat05"] = beat_starts["beat04"] + dur_map["beat04"]
    beat_starts["beat06"] = beat_starts["beat05"] + dur_map["beat05a"] + dur_map["beat05b"]
    beat_starts["beat07"] = beat_starts["beat06"] + dur_map["beat06a"] + dur_map["beat06b"]
    total_dur = beat_starts["beat07"] + dur_map["beat07a"] + dur_map["beat07b"]

    video_parts: list[Path] = []
    foley_parts: list[tuple[float, Path]] = []
    t_cursor = 0.0
    for kind, src, dur, name, hdr in segs:
        vp = work_dir / f"{mode}_{name}.mp4"
        if kind == "flow":
            fp = work_dir / f"{mode}_{name}_foley.wav"
            prepare_flow_clip(src, vp, dur, fp, mode=mode)
            foley_parts.append((t_cursor, fp))
        else:
            adjust_motion_clip(src, vp, dur, mode=mode, header_png=hdr)
        video_parts.append(vp)
        t_cursor += dur

    concat_list = work_dir / f"{mode}_concat.txt"
    concat_list.write_text("\n".join(f"file '{p}'" for p in video_parts), encoding="utf-8")
    raw_video = work_dir / f"{mode}_video_raw.mp4"
    run_ffmpeg(["-f", "concat", "-safe", "0", "-i", str(concat_list), "-c", "copy", str(raw_video)])

    v_in, v_fc = [], []
    for i, bid in enumerate([f"beat0{k}" for k in range(1, 8)]):
        v_in.extend(["-i", beats_by_id[bid]["wav"]])
        dms = int(round(beat_starts[bid] * 1000))
        v_fc.append(f"[{i}:a]aformat=sample_rates=48000:channel_layouts=stereo,adelay={dms}|{dms}[v{i}]")
    v_fc.append(f"{''.join(f'[v{i}]' for i in range(7))}amix=inputs=7:duration=longest:normalize=0,apad=whole_dur={total_dur:.3f},atrim=duration={total_dur:.3f},loudnorm=I=-14:TP=-1.5:LRA=9[vnorm]")
    narration_wav = work_dir / f"{mode}_narration.wav"
    run_ffmpeg([*v_in, "-filter_complex", ";".join(v_fc), "-map", "[vnorm]", "-c:a", "pcm_s16le", str(narration_wav)])

    f_in, f_fc = [], []
    for i, (st, fp) in enumerate(foley_parts):
        f_in.extend(["-i", str(fp)])
        dms = int(round(st * 1000))
        f_fc.append(f"[{i}:a]volume=0.11,adelay={dms}|{dms}[f{i}]")
    f_fc.append(f"{''.join(f'[f{i}]' for i in range(len(foley_parts)))}amix=inputs={len(foley_parts)}:duration=longest:normalize=0,apad=whole_dur={total_dur:.3f},atrim=duration={total_dur:.3f}[fout]")
    foley_wav = work_dir / f"{mode}_foley.wav"
    run_ffmpeg([*f_in, "-filter_complex", ";".join(f_fc), "-map", "[fout]", "-c:a", "pcm_s16le", str(foley_wav)])

    score_bed = work_dir / f"{mode}_score.wav"
    run_ffmpeg(
        [
            "-stream_loop", "-1", "-i", str(score_wav), "-t", f"{total_dur:.3f}",
            "-af", f"aformat=sample_rates=48000:channel_layouts=stereo,volume=0.22,afade=t=in:st=0:d=1.0,afade=t=out:st={max(0.0, total_dur-2.2):.3f}:d=2.2",
            "-c:a", "pcm_s16le", str(score_bed),
        ]
    )

    mixed_wav = work_dir / f"{mode}_mix.wav"
    run_ffmpeg(
        [
            "-i", str(narration_wav), "-i", str(score_bed), "-i", str(foley_wav),
            "-filter_complex",
            "[0:a]asplit=2[vo_m][vo_sc];[1:a][vo_sc]sidechaincompress=threshold=0.03:ratio=4.5:attack=40:release=320[m_duck];[vo_m][m_duck][2:a]amix=inputs=3:duration=first:normalize=0,alimiter=limit=0.92[mix]",
            "-map", "[mix]", "-c:a", "pcm_s16le", str(mixed_wav),
        ]
    )

    prefix = spec["output_prefix"]
    if mode == "16x9":
        clean_out = out_dir / f"{prefix}_16x9_1080p_Clean.mp4"
        run_ffmpeg(["-i", str(raw_video), "-i", str(mixed_wav), "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(clean_out)])

    w, h = (1920, 1080) if mode == "16x9" else (1080, 1920)
    b_margin = 52 if mode == "16x9" else 310
    f_size = 38 if mode == "16x9" else 42
    ov_in = ["-i", str(raw_video), "-i", str(mixed_wav)]
    ov_fc = []
    cur_v = "0:v"
    sub_idx = 0
    for bid in [f"beat0{k}" for k in range(1, 8)]:
        bst = beat_starts[bid]
        for cue in normalize_cues(beats_by_id[bid]["cues"]):
            st_abs, en_abs = round(bst + float(cue["start"]), 3), round(bst + float(cue["end"]), 3)
            if en_abs <= st_abs:
                continue
            spng = work_dir / f"{mode}_sub_{sub_idx:03d}.png"
            make_subtitle_png(cue["text"], spng, w, h, bottom_margin=b_margin, font_size=f_size)
            in_i = sub_idx + 2
            ov_in.extend(["-i", str(spng)])
            nxt = f"ov{in_i}"
            ov_fc.append(f"[{cur_v}][{in_i}:v]overlay=0:0:enable='between(t,{st_abs:.3f},{en_abs:.3f})'[{nxt}]")
            cur_v = nxt
            sub_idx += 1

    final_name = f"{prefix}_16x9_1080p_Subtitled.mp4" if mode == "16x9" else f"{prefix}_9x16_Shorts.mp4"
    final_out = out_dir / final_name
    ov_fc.append(f"[{cur_v}]format=yuv420p[outv]")
    run_ffmpeg([*ov_in, "-filter_complex", ";".join(ov_fc), "-map", "[outv]", "-map", "1:a", "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(final_out)])
    return final_out


def cmd_master(spec_path: Path) -> None:
    spec, ep_dir = load_spec(spec_path)
    enforce_manifest_gate(ep_dir)
    timeline_path = ep_dir / "audio" / "voiceover_timeline.json"
    score_wav = ep_dir / "audio" / "flow_music_score.wav"
    if not timeline_path.is_file():
        raise FileNotFoundError(f"Run `prepare` first; missing {timeline_path}")
    if not score_wav.is_file():
        score_wav = build_flow_music_score(spec, ep_dir)
    timeline = json.loads(timeline_path.read_text(encoding="utf-8"))

    dl_dir = Path(spec["downloads_dir"]).expanduser()
    dl_dir.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="hmb_ep_master_") as tmp:
        wdir = Path(tmp)
        out_16 = build_track_for_mode(spec, ep_dir, "16x9", wdir, timeline, score_wav)
        out_916 = build_track_for_mode(spec, ep_dir, "9x16", wdir, timeline, score_wav)

    clean_16 = ep_dir / "output" / f"{spec['output_prefix']}_16x9_1080p_Clean.mp4"
    for p in (clean_16, out_16, out_916):
        shutil.copy2(p, dl_dir / p.name)
        info = ffprobe_info(dl_dir / p.name)
        print(f"DELIVERED: {dl_dir / p.name} ({info['size']/1e6:.2f} MB, {info['duration']:.2f}s, {info['width']}x{info['height']}, audio={info['has_audio']}, {info['sample_rate']}Hz/{info['channels']}ch, GCP=$0.00)")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="How Markets Break Zero-Confirm Free-Credit Episode Factory")
    sub = parser.add_subparsers(dest="cmd", required=True)
    p_prep = sub.add_parser("prepare", help="Run YPP gate, fetch live data, synthesize voiceover/music, render charts")
    p_prep.add_argument("spec_json", help="Path to episode_spec.json")
    p_mast = sub.add_parser("master", help="Assemble 16:9 Clean/Subtitled + 9:16 Shorts from Flow renders")
    p_mast.add_argument("spec_json", help="Path to episode_spec.json")
    args = parser.parse_args(argv)
    if args.cmd == "prepare":
        cmd_prepare(Path(args.spec_json))
    elif args.cmd == "master":
        cmd_master(Path(args.spec_json))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
