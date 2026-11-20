#!/usr/bin/env python3
"""
Render broadcast-grade 30fps animated motion-graphic segments for How Markets Break Y0
in both 16:9 (1920x1080) and 9:16 (1080x1920), synced to voiceover_timeline.json durations.
"""
from __future__ import annotations

import datetime
import html
import json
import subprocess
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
SNAP_PATH = ROOT / "data" / "market_snapshot_20261120.json"
TIMELINE_PATH = ROOT / "audio" / "voiceover_timeline.json"
MOTION_DIR = ROOT / "motion_assets"
CHROME_BIN = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def render_html_to_png(html_content: str, out_png: Path, w: int, h: int, transparent: bool = False) -> None:
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
        if res.returncode != 0 or not out_png.is_file():
            raise RuntimeError(f"Chrome screenshot failed for {out_png}: {res.stderr[:250]}")
    finally:
        html_path.unlink(missing_ok=True)


def run_ffmpeg(args: list[str]) -> None:
    res = subprocess.run(["ffmpeg", "-y", "-v", "error", *args], capture_output=True, text=True, check=False)
    if res.returncode != 0:
        raise RuntimeError(f"ffmpeg failed:\n{' '.join(args)}\n{res.stderr}")


def fmt_date_short(iso: str) -> str:
    return datetime.date.fromisoformat(iso).strftime("%b %-d")


def svg_doc(w: int, h: int, body: str, bg: str | None = "#0B0E14") -> str:
    bg_css = bg if bg else "transparent"
    bg_rect = f'<rect width="{w}" height="{h}" fill="{bg}"/>' if bg else ""
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  html, body {{ width: {w}px; height: {h}px; overflow: hidden; background: {bg_css}; font-family: -apple-system, BlinkMacSystemFont, "Inter", sans-serif; }}
</style></head>
<body><svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">{bg_rect}{body}</svg></body></html>"""


def build_hook_card_16x9(snap: dict[str, Any], out_mp4: Path, dur: float) -> None:
    """Beat 1B: 3-asset shock ticker card + LIQUIDITY TRAP verdict."""
    s = snap["series"]
    cards = [
        ("NASDAQ COMPOSITE", f"{s['ixic']['last_close']:,.0f}", f"{s['ixic']['pct_from_high']:+.2f}%", "#38BDF8", 130),
        ("BITCOIN (BTC-USD)", f"${s['btc']['last_close']:,.0f}", f"{s['btc']['pct_from_high']:+.2f}%", "#E5484D", 706),
        ("GOLD FUTURES", f"${s['gold']['last_close']:,.0f}", f"{s['gold']['pct_from_high']:+.2f}%", "#E5A93B", 1282),
    ]
    base_png = MOTION_DIR / "hook_16x9_base.png"
    verdict_png = MOTION_DIR / "hook_16x9_verdict.png"

    card_svgs = []
    for title, price, pct, color, x in cards:
        card_svgs.append(f"""
        <rect x="{x}" y="220" width="508" height="330" rx="10" fill="#101521" stroke="{color}" stroke-width="2" stroke-opacity="0.7"/>
        <rect x="{x}" y="220" width="508" height="6" rx="2" fill="{color}"/>
        <text x="{x + 36}" y="286" fill="{color}" font-size="22" font-weight="700" letter-spacing="2" font-family="SF Mono, Menlo, monospace">{title}</text>
        <text x="{x + 36}" y="382" fill="#F8FAFC" font-size="56" font-weight="700" font-family="SF Mono, Menlo, monospace">{pct}</text>
        <text x="{x + 36}" y="446" fill="#94A3B8" font-size="24" font-family="SF Mono, Menlo, monospace">Close: {price}</text>
        <text x="{x + 36}" y="492" fill="#64748B" font-size="18" font-family="SF Mono, Menlo, monospace">Drawdown from Nov peak</text>
        """)
    base_body = f"""
      <text x="130" y="138" fill="#94A3B8" font-size="24" font-weight="600" letter-spacing="3" font-family="SF Mono, Menlo, monospace">NOVEMBER 4 – 20, 2026  ·  SYNCHRONIZED SELLOFF</text>
      {''.join(card_svgs)}
    """
    verdict_body = """
      <rect x="310" y="640" width="1300" height="176" rx="10" fill="#160D12" stroke="#E5484D" stroke-width="2.5"/>
      <text x="960" y="716" fill="#F8FAFC" font-size="48" font-weight="700" text-anchor="middle">IT ISN'T PANIC. IT'S A LIQUIDITY TRAP.</text>
      <text x="960" y="770" fill="#FCA5A5" font-size="22" font-weight="600" letter-spacing="3" font-family="SF Mono, Menlo, monospace" text-anchor="middle">RISK ASSETS &amp; SAFE HAVENS SOLD TOGETHER TO RAISE CASH</text>
    """
    render_html_to_png(svg_doc(1920, 1080, base_body, "#0B0E14"), base_png, 1920, 1080, transparent=False)
    render_html_to_png(svg_doc(1920, 1080, verdict_body, bg=None), verdict_png, 1920, 1080, transparent=True)

    # Fade in verdict at t=1.8s
    fc = (
        f"[1:v]format=rgba,fade=t=in:st=1.6:d=0.45:alpha=1[ov];"
        f"[0:v][ov]overlay=0:0:shortest=1,format=yuv420p"
    )
    run_ffmpeg([
        "-loop", "1", "-framerate", "30", "-t", f"{dur:.3f}", "-i", str(base_png),
        "-loop", "1", "-framerate", "30", "-t", f"{dur:.3f}", "-i", str(verdict_png),
        "-filter_complex", fc,
        "-c:v", "libx264", "-preset", "fast", "-crf", "18", str(out_mp4),
    ])


def build_chart01_animated_16x9(snap: dict[str, Any], out_mp4: Path, dur: float) -> None:
    """Beat 2: Animated left-to-right sweep for Nasdaq -> Bitcoin -> Gold."""
    series_cfg = [
        ("ixic", "Nasdaq Composite", "#38BDF8", "^IXIC"),
        ("gold", "Gold Futures", "#E5A93B", "GC=F"),
        ("btc", "Bitcoin", "#E5484D", "BTC-USD"),
    ]
    all_dates = sorted({pt["date"] for key, *_ in series_cfg for pt in snap["series"][key]["points"]})
    date_idx = {d: i for i, d in enumerate(all_dates)}
    W, H = 1920, 1080
    PL, PR, PT, PB = 130, 420, 230, 145
    PW = W - PL - PR
    PH = H - PT - PB
    y_min, y_max = -26.5, 2.0

    def x_px(d: str) -> float:
        return PL + (date_idx[d] / max(1, len(all_dates) - 1)) * PW

    def y_px(pct: float) -> float:
        return PT + ((y_max - pct) / (y_max - y_min)) * PH

    grid_lines = []
    for tick in [0, -5, -10, -15, -20, -25]:
        yy = y_px(float(tick))
        stroke = "#334155" if tick == 0 else "#1B2230"
        sw = "2" if tick == 0 else "1"
        dash = "" if tick == 0 else 'stroke-dasharray="4 6"'
        grid_lines.append(f'<line x1="{PL}" y1="{yy:.1f}" x2="{PL + PW}" y2="{yy:.1f}" stroke="{stroke}" stroke-width="{sw}" {dash}/>')
        grid_lines.append(f'<text x="{PL - 22}" y="{yy + 7:.1f}" fill="#8B96A8" font-size="22" font-family="SF Mono, Menlo, monospace" text-anchor="end">{tick}%</text>')

    x_ticks = []
    shown = {i for i in range(0, len(all_dates), 3) if i < len(all_dates) - 2} | {len(all_dates) - 1}
    for idx in sorted(shown):
        d = all_dates[idx]
        xx = x_px(d)
        x_ticks.append(f'<line x1="{xx:.1f}" y1="{PT}" x2="{xx:.1f}" y2="{PT + PH}" stroke="#161C27" stroke-width="1"/>')
        x_ticks.append(f'<text x="{xx:.1f}" y="{PT + PH + 42}" fill="#8B96A8" font-size="21" font-family="SF Mono, Menlo, monospace" text-anchor="middle">{html.escape(fmt_date_short(d))}</text>')

    base_png = MOTION_DIR / "c01_base.png"
    base_body = f"""
      <rect x="64" y="54" width="1792" height="972" fill="#0E121B" stroke="#1E2532" stroke-width="1.5" rx="8"/>
      <text x="130" y="106" fill="#E5A93B" font-size="18" font-weight="700" letter-spacing="3" font-family="SF Mono, Menlo, monospace">HOW MARKETS BREAK  |  THE BROKEN SAFE-HAVEN PARADOX (NOV 4–20, 2026)</text>
      <text x="130" y="156" fill="#F8FAFC" font-size="42" font-weight="700">Everything Fell Together — Even Gold Dropped Nearly 2x Harder Than Tech</text>
      <text x="130" y="196" fill="#94A3B8" font-size="22">Normalized drawdown (%) from each asset's November 2026 peak daily close</text>
      {''.join(x_ticks)}{''.join(grid_lines)}
      <line x1="{PL}" y1="{PT}" x2="{PL}" y2="{PT + PH}" stroke="#2A3447" stroke-width="1.5"/>
      <line x1="{PL}" y1="{PT + PH}" x2="{PL + PW}" y2="{PT + PH}" stroke="#2A3447" stroke-width="1.5"/>
      <text x="130" y="998" fill="#64748B" font-size="18" font-family="SF Mono, Menlo, monospace">Source: Yahoo Finance daily closes (^IXIC, GC=F, BTC-USD) as of Nov 20, 2026 · Educational market mechanics, not financial advice</text>
    """
    render_html_to_png(svg_doc(1920, 1080, base_body, "#0B0E14"), base_png, 1920, 1080, transparent=False)

    # Precompute badge Y positions identically to static chart
    badges_meta = []
    curve_pngs: dict[str, Path] = {}
    badge_pngs: dict[str, Path] = {}
    for key, label, color, ticker in series_cfg:
        s = snap["series"][key]
        hi = s["high_close"]
        pts_xy = [(x_px(pt["date"]), y_px((pt["close"] - hi) / hi * 100.0), pt) for pt in s["points"]]
        d_attr = " ".join(("M" if i == 0 else "L") + f"{x:.1f},{y:.1f}" for i, (x, y, _) in enumerate(pts_xy))
        lx, ly, lpt = pts_xy[-1]
        curve_svg = f'<path d="{d_attr}" fill="none" stroke="{color}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round" opacity="0.96"/><circle cx="{lx:.1f}" cy="{ly:.1f}" r="9" fill="{color}" stroke="#0B0E14" stroke-width="3"/>'
        cp = MOTION_DIR / f"c01_curve_{key}.png"
        render_html_to_png(svg_doc(1920, 1080, curve_svg, bg=None), cp, 1920, 1080, transparent=True)
        curve_pngs[key] = cp
        badges_meta.append({
            "key": key, "raw_y": ly, "color": color, "label": label, "ticker": ticker,
            "dd": (lpt["close"] - hi) / hi * 100.0, "hi": hi, "last": lpt["close"],
            "hi_date": fmt_date_short(s["high_date"]), "last_date": fmt_date_short(lpt["date"]),
        })

    badges_meta.sort(key=lambda b: b["raw_y"])
    for i in range(1, len(badges_meta)):
        if badges_meta[i]["raw_y"] - badges_meta[i - 1]["raw_y"] < 128.0:
            badges_meta[i]["raw_y"] = badges_meta[i - 1]["raw_y"] + 128.0

    bx, bw, bh = PL + PW + 28, 360, 108
    for b in badges_meta:
        by = min(max(PT, b["raw_y"] - bh / 2), PT + PH - bh)
        range_str = f"{b['hi']:,.0f} ({b['hi_date']}) → {b['last']:,.0f}" if b["ticker"] == "^IXIC" else f"${b['hi']:,.0f} ({b['hi_date']}) → ${b['last']:,.0f}"
        bsvg = f"""
          <rect x="{bx}" y="{by:.1f}" width="{bw}" height="{bh}" rx="6" fill="#121722" stroke="{b['color']}" stroke-width="2" stroke-opacity="0.8"/>
          <rect x="{bx}" y="{by:.1f}" width="6" height="{bh}" rx="2" fill="{b['color']}"/>
          <text x="{bx + 20}" y="{by + 33:.1f}" fill="#E6ECF5" font-size="22" font-weight="600">{html.escape(b['label'])}</text>
          <text x="{bx + bw - 18}" y="{by + 36:.1f}" fill="{b['color']}" font-size="28" font-weight="700" font-family="SF Mono, Menlo, monospace" text-anchor="end">{b['dd']:+.2f}%</text>
          <text x="{bx + 20}" y="{by + 68:.1f}" fill="#8B96A8" font-size="18" font-family="SF Mono, Menlo, monospace">{html.escape(range_str)}</text>
          <text x="{bx + 20}" y="{by + 92:.1f}" fill="#5F6B7E" font-size="16" font-family="SF Mono, Menlo, monospace">Latest close: {html.escape(b['last_date'])}</text>
        """
        bp = MOTION_DIR / f"c01_badge_{b['key']}.png"
        render_html_to_png(svg_doc(1920, 1080, bsvg, bg=None), bp, 1920, 1080, transparent=True)
        badge_pngs[b["key"]] = bp

    # Timing synced to beat02 voiceover: Nasdaq ~2.0s, Bitcoin ~6.0s, Gold ~9.8s
    timings = [("ixic", 1.8, 3.0), ("btc", 5.8, 2.8), ("gold", 9.6, 2.8)]
    inputs = ["-loop", "1", "-framerate", "30", "-t", f"{dur:.3f}", "-i", str(base_png)]
    filters = []
    last_v = "0:v"
    idx = 1
    for key, t_start, sweep_d in timings:
        inputs.extend(["-loop", "1", "-framerate", "30", "-t", f"{dur:.3f}", "-i", str(curve_pngs[key])])
        c_idx = idx
        idx += 1
        inputs.extend(["-loop", "1", "-framerate", "30", "-t", f"{dur:.3f}", "-i", str(badge_pngs[key])])
        b_idx = idx
        idx += 1
        # Progressive left-to-right wipe across plot width [PL, PL+PW+20]
        w_expr = f"if(lt(t,{t_start}),1,if(lt(t,{t_start+sweep_d}),max(1,min({PL+PW+25},{PL}+({PW+25})*(t-{t_start})/{sweep_d})),{PL+PW+25}))"
        filters.append(f"[{c_idx}:v]format=rgba,crop='{w_expr}':1080:0:0[cw{c_idx}]")
        filters.append(f"[{last_v}][cw{c_idx}]overlay=0:0:shortest=1[v{c_idx}]")
        b_fade = round(t_start + sweep_d * 0.55, 2)
        filters.append(f"[{b_idx}:v]format=rgba,fade=t=in:st={b_fade}:d=0.35:alpha=1[bf{b_idx}]")
        filters.append(f"[v{c_idx}][bf{b_idx}]overlay=0:0:shortest=1[v{b_idx}]")
        last_v = f"v{b_idx}"

    filters.append(f"[{last_v}]format=yuv420p[outv]")
    run_ffmpeg([*inputs, "-filter_complex", ";".join(filters), "-map", "[outv]", "-c:v", "libx264", "-preset", "fast", "-crf", "18", str(out_mp4)])


def build_chart02_animated_16x9(snap: dict[str, Any], out_mp4: Path, dur: float) -> None:
    """Beat 4: Sequential 3-panel macro dashboard reveal synced to beat04 narration."""
    base_png = MOTION_DIR / "c02_base.png"
    base_body = """
      <text x="110" y="102" fill="#E5A93B" font-size="18" font-weight="700" letter-spacing="3" font-family="SF Mono, Menlo, monospace">HOW MARKETS BREAK  |  MACRO PRESSURE GAUGES (NOV 4–20, 2026)</text>
      <text x="110" y="156" fill="#F8FAFC" font-size="44" font-weight="700">The Real Culprit: Cash-Is-King Liquidity Squeeze</text>
      <text x="110" y="198" fill="#94A3B8" font-size="22">Rising yields, a surging dollar, and spiking volatility force indiscriminate margin liquidation</text>
      <text x="110" y="998" fill="#64748B" font-size="18" font-family="SF Mono, Menlo, monospace">Source: Yahoo Finance daily closes (^TNX, DX-Y.NYB, ^VIX) as of Nov 20, 2026 · Educational market mechanics, not financial advice</text>
    """
    render_html_to_png(svg_doc(1920, 1080, base_body, "#0B0E14"), base_png, 1920, 1080, transparent=False)

    panels_cfg = [
        {"key": "us10y", "title": "10Y US TREASURY YIELD", "subtitle": "Risk-free hurdle breached 5.00%", "color": "#E5484D", "unit": "%", "threshold": 5.00, "threshold_label": "5.00% DANGER LINE", "y_min": 4.70, "y_max": 5.25, "delta_label": lambda s: f"{s['first_close']:.2f}% → {s['last_close']:.2f}% (Peak {s['high_close']:.2f}%)"},
        {"key": "dxy", "title": "US DOLLAR INDEX (DXY)", "subtitle": "Global USD scramble tightens liquidity", "color": "#38BDF8", "unit": "", "threshold": None, "threshold_label": "", "y_min": 101.0, "y_max": 104.5, "delta_label": lambda s: f"{s['low_close']:.2f} ({fmt_date_short(s['low_date'])}) → {s['last_close']:.2f} ({s['pct_from_low']:+.2f}%)"},
        {"key": "vix", "title": "CBOE VOLATILITY (^VIX)", "subtitle": "Fear gauge surging past 30 stress line", "color": "#E5A93B", "unit": "", "threshold": 30.0, "threshold_label": "30.0 STRESS LINE", "y_min": 14.0, "y_max": 33.0, "delta_label": lambda s: f"{s['low_close']:.2f} ({fmt_date_short(s['low_date'])}) → {s['last_close']:.2f} ({s['pct_from_low']:+.1f}%)"},
    ]
    px0, gap, pw_total, py0, ph_total = 110, 46, 536, 240, 690
    panel_pngs: list[Path] = []
    for idx, cfg in enumerate(panels_cfg):
        s = snap["series"][cfg["key"]]
        pts = s["points"]
        x_box = px0 + idx * (pw_total + gap)
        ipl, ipr, ipt, ipb = x_box + 56, x_box + pw_total - 28, py0 + 188, py0 + ph_total - 70
        ipw, iph = ipr - ipl, ipb - ipt
        ymin, ymax = cfg["y_min"], cfg["y_max"]

        def px(i: int, n: int = len(pts)) -> float:
            return ipl + (i / max(1, n - 1)) * ipw

        def py(v: float) -> float:
            return ipt + ((ymax - v) / (ymax - ymin)) * iph

        p_lines = []
        for k in range(4):
            val = ymin + (ymax - ymin) * k / 3.0
            yy = py(val)
            p_lines.append(f'<line x1="{ipl}" y1="{yy:.1f}" x2="{ipr}" y2="{yy:.1f}" stroke="#1B2230" stroke-width="1"/>')
            p_lines.append(f'<text x="{ipl - 8}" y="{yy + 5:.1f}" fill="#64748B" font-size="16" font-family="SF Mono, Menlo, monospace" text-anchor="end">{val:.1f}{cfg["unit"]}</text>')
        if cfg["threshold"] is not None:
            ty = py(cfg["threshold"])
            p_lines.append(f'<line x1="{ipl}" y1="{ty:.1f}" x2="{ipr}" y2="{ty:.1f}" stroke="#F87171" stroke-width="2" stroke-dasharray="6 6" opacity="0.85"/>')
            p_lines.append(f'<text x="{ipr}" y="{ty - 10:.1f}" fill="#F87171" font-size="15" font-weight="700" font-family="SF Mono, Menlo, monospace" text-anchor="end">{cfg["threshold_label"]}</text>')

        coords = [(px(i), py(pt["close"])) for i, pt in enumerate(pts)]
        d_path = " ".join(("M" if i == 0 else "L") + f"{x:.1f},{y:.1f}" for i, (x, y) in enumerate(coords))
        area_path = f"{d_path} L{coords[-1][0]:.1f},{ipb:.1f} L{coords[0][0]:.1f},{ipb:.1f} Z"
        p_lines.append(f'<path d="{area_path}" fill="{cfg["color"]}" fill-opacity="0.12"/>')
        p_lines.append(f'<path d="{d_path}" fill="none" stroke="{cfg["color"]}" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"/>')
        p_lines.append(f'<circle cx="{coords[-1][0]:.1f}" cy="{coords[-1][1]:.1f}" r="8" fill="{cfg["color"]}" stroke="#0B0E14" stroke-width="2.5"/>')
        p_lines.append(f'<text x="{ipl}" y="{ipb + 36}" fill="#8B96A8" font-size="17" font-family="SF Mono, Menlo, monospace">{html.escape(fmt_date_short(pts[0]["date"]))}</text>')
        p_lines.append(f'<text x="{ipr}" y="{ipb + 36}" fill="#8B96A8" font-size="17" font-family="SF Mono, Menlo, monospace" text-anchor="end">{html.escape(fmt_date_short(pts[-1]["date"]))}</text>')

        psvg = f"""
          <rect x="{x_box}" y="{py0}" width="{pw_total}" height="{ph_total}" rx="8" fill="#0E121B" stroke="#1E2532" stroke-width="1.5"/>
          <rect x="{x_box}" y="{py0}" width="{pw_total}" height="5" rx="2" fill="{cfg['color']}"/>
          <text x="{x_box + 32}" y="{py0 + 44}" fill="{cfg['color']}" font-size="19" font-weight="700" letter-spacing="1.5" font-family="SF Mono, Menlo, monospace">{html.escape(cfg['title'])}</text>
          <text x="{x_box + 32}" y="{py0 + 74}" fill="#94A3B8" font-size="18">{html.escape(cfg['subtitle'])}</text>
          <text x="{x_box + 32}" y="{py0 + 124}" fill="#F8FAFC" font-size="40" font-weight="700" font-family="SF Mono, Menlo, monospace">{html.escape(f"{s['last_close']:.2f}{cfg['unit']}")}</text>
          <text x="{x_box + 32}" y="{py0 + 154}" fill="#CBD5E1" font-size="17" font-family="SF Mono, Menlo, monospace">{html.escape(cfg['delta_label'](s))}</text>
          {''.join(p_lines)}
        """
        pp = MOTION_DIR / f"c02_panel_{idx}.png"
        render_html_to_png(svg_doc(1920, 1080, psvg, bg=None), pp, 1920, 1080, transparent=True)
        panel_pngs.append(pp)

    # Reveal panels synced to beat04: 1.4s (Yields), 5.4s (Dollar), 8.6s (VIX)
    reveals = [1.4, 5.4, 8.6]
    inputs = ["-loop", "1", "-framerate", "30", "-t", f"{dur:.3f}", "-i", str(base_png)]
    filters = []
    last_v = "0:v"
    for idx, (pp, t_st) in enumerate(zip(panel_pngs, reveals), start=1):
        inputs.extend(["-loop", "1", "-framerate", "30", "-t", f"{dur:.3f}", "-i", str(pp)])
        filters.append(f"[{idx}:v]format=rgba,fade=t=in:st={t_st}:d=0.45:alpha=1[pf{idx}]")
        filters.append(f"[{last_v}][pf{idx}]overlay=0:0:shortest=1[v{idx}]")
        last_v = f"v{idx}"
    filters.append(f"[{last_v}]format=yuv420p[outv]")
    run_ffmpeg([*inputs, "-filter_complex", ";".join(filters), "-map", "[outv]", "-c:v", "libx264", "-preset", "fast", "-crf", "18", str(out_mp4)])


def build_margin_cascade_16x9(snap: dict[str, Any], out_mp4: Path, dur: float) -> None:
    """Beat 5B: 3-step animated forced liquidation chain."""
    s = snap["series"]
    base_png = MOTION_DIR / "cascade_base.png"
    s2_png = MOTION_DIR / "cascade_s2.png"
    s3_png = MOTION_DIR / "cascade_s3.png"

    n1 = f"""
      <text x="130" y="106" fill="#E5A93B" font-size="18" font-weight="700" letter-spacing="3" font-family="SF Mono, Menlo, monospace">HOW MARKETS BREAK  |  FORCED LIQUIDATION MECHANISM</text>
      <text x="130" y="158" fill="#F8FAFC" font-size="42" font-weight="700">Why Funds Dump Everything Liquid at the Same Time</text>
      <rect x="130" y="290" width="460" height="400" rx="10" fill="#101521" stroke="#38BDF8" stroke-width="2"/>
      <text x="170" y="348" fill="#38BDF8" font-size="19" font-weight="700" letter-spacing="2" font-family="SF Mono, Menlo, monospace">01 · CASH TIGHTENS</text>
      <text x="170" y="425" fill="#F8FAFC" font-size="44" font-weight="700" font-family="SF Mono, Menlo, monospace">{s['us10y']['last_close']:.2f}%</text>
      <text x="170" y="466" fill="#94A3B8" font-size="22">Risk-free 10Y yield + DXY {s['dxy']['last_close']:.2f}</text>
      <text x="170" y="535" fill="#CBD5E1" font-size="22">Capital flees leverage into</text>
      <text x="170" y="568" fill="#CBD5E1" font-size="22">risk-free T-Bills and USD cash.</text>
    """
    n2 = """
      <line x1="590" y1="490" x2="710" y2="490" stroke="#E5A93B" stroke-width="4"/>
      <polygon points="710,480 730,490 710,500" fill="#E5A93B"/>
      <rect x="730" y="290" width="460" height="400" rx="10" fill="#16121A" stroke="#E5A93B" stroke-width="2"/>
      <text x="770" y="348" fill="#E5A93B" font-size="19" font-weight="700" letter-spacing="2" font-family="SF Mono, Menlo, monospace">02 · MARGIN CALLS</text>
      <text x="770" y="425" fill="#F8FAFC" font-size="38" font-weight="700">Leverage Unwinds</text>
      <text x="770" y="500" fill="#CBD5E1" font-size="22">Funds don't sell what they hate —</text>
      <text x="770" y="536" fill="#CBD5E1" font-size="22">they sell whatever is liquid</text>
      <text x="770" y="572" fill="#CBD5E1" font-size="22">to post collateral before close.</text>
    """
    n3 = f"""
      <line x1="1190" y1="490" x2="1310" y2="490" stroke="#E5484D" stroke-width="4"/>
      <polygon points="1310,480 1330,490 1310,500" fill="#E5484D"/>
      <rect x="1330" y="290" width="460" height="400" rx="10" fill="#180F14" stroke="#E5484D" stroke-width="2"/>
      <text x="1370" y="348" fill="#E5484D" font-size="19" font-weight="700" letter-spacing="2" font-family="SF Mono, Menlo, monospace">03 · ALL SOLD TOGETHER</text>
      <text x="1370" y="430" fill="#38BDF8" font-size="30" font-weight="700" font-family="SF Mono, Menlo, monospace">Tech (Nasdaq)  {s['ixic']['pct_from_high']:+.2f}%</text>
      <text x="1370" y="495" fill="#E5484D" font-size="30" font-weight="700" font-family="SF Mono, Menlo, monospace">Crypto (BTC)   {s['btc']['pct_from_high']:+.2f}%</text>
      <text x="1370" y="560" fill="#E5A93B" font-size="30" font-weight="700" font-family="SF Mono, Menlo, monospace">Gold (Profit)  {s['gold']['pct_from_high']:+.2f}%</text>
      <text x="1370" y="632" fill="#FCA5A5" font-size="20">Even winning gold bars are sold for cash.</text>
    """
    render_html_to_png(svg_doc(1920, 1080, n1, "#0B0E14"), base_png, 1920, 1080, transparent=False)
    render_html_to_png(svg_doc(1920, 1080, n2, bg=None), s2_png, 1920, 1080, transparent=True)
    render_html_to_png(svg_doc(1920, 1080, n3, bg=None), s3_png, 1920, 1080, transparent=True)

    fc = (
        "[1:v]format=rgba,fade=t=in:st=1.6:d=0.45:alpha=1[v1f];"
        "[2:v]format=rgba,fade=t=in:st=4.4:d=0.45:alpha=1[v2f];"
        "[0:v][v1f]overlay=0:0:shortest=1[m1];"
        "[m1][v2f]overlay=0:0:shortest=1,format=yuv420p"
    )
    run_ffmpeg([
        "-loop", "1", "-framerate", "30", "-t", f"{dur:.3f}", "-i", str(base_png),
        "-loop", "1", "-framerate", "30", "-t", f"{dur:.3f}", "-i", str(s2_png),
        "-loop", "1", "-framerate", "30", "-t", f"{dur:.3f}", "-i", str(s3_png),
        "-filter_complex", fc, "-c:v", "libx264", "-preset", "fast", "-crf", "18", str(out_mp4),
    ])


def build_liquidity_vs_bear_16x9(out_mp4: Path, dur: float) -> None:
    """Beat 6B: Liquidity Squeeze vs True Bear Market split diagnostic."""
    base_png = MOTION_DIR / "lvb_base.png"
    right_png = MOTION_DIR / "lvb_right.png"
    left_svg = """
      <text x="130" y="106" fill="#E5A93B" font-size="18" font-weight="700" letter-spacing="3" font-family="SF Mono, Menlo, monospace">HOW MARKETS BREAK  |  BEAR MARKET DIAGNOSTIC</text>
      <text x="130" y="158" fill="#F8FAFC" font-size="42" font-weight="700">Violent Flush vs. True Bear Market</text>
      <rect x="130" y="250" width="790" height="580" rx="10" fill="#101724" stroke="#E5A93B" stroke-width="2"/>
      <rect x="130" y="250" width="790" height="6" rx="2" fill="#E5A93B"/>
      <text x="180" y="320" fill="#E5A93B" font-size="22" font-weight="700" letter-spacing="2" font-family="SF Mono, Menlo, monospace">A · FORCED LIQUIDITY SQUEEZE</text>
      <text x="180" y="395" fill="#F8FAFC" font-size="34" font-weight="700">Sharp Cross-Asset Drop</text>
      <text x="180" y="468" fill="#CBD5E1" font-size="25">• Driven by rising yields &amp; USD margin calls</text>
      <text x="180" y="520" fill="#CBD5E1" font-size="25">• Gold, Bitcoin &amp; Nasdaq fall together</text>
      <text x="180" y="572" fill="#CBD5E1" font-size="25">• Rebounds once yields peak &amp; forced</text>
      <text x="198" y="610" fill="#CBD5E1" font-size="25">selling exhausts leverage</text>
    """
    right_svg = """
      <rect x="1000" y="250" width="790" height="580" rx="10" fill="#171016" stroke="#E5484D" stroke-width="2"/>
      <rect x="1000" y="250" width="790" height="6" rx="2" fill="#E5484D"/>
      <text x="1050" y="320" fill="#E5484D" font-size="22" font-weight="700" letter-spacing="2" font-family="SF Mono, Menlo, monospace">B · STRUCTURAL BEAR MARKET</text>
      <text x="1050" y="395" fill="#F8FAFC" font-size="34" font-weight="700">Multi-Quarter Earnings Decay</text>
      <text x="1050" y="468" fill="#CBD5E1" font-size="25">• Persistent corporate credit &amp; margin erosion</text>
      <text x="1050" y="520" fill="#CBD5E1" font-size="25">• Safe havens eventually decouple upward</text>
      <text x="1050" y="572" fill="#CBD5E1" font-size="25">• Failed relief rallies make lower highs</text>
      <text x="1050" y="640" fill="#FCA5A5" font-size="23" font-weight="600">Look identical at Week 2 — until yields turn.</text>
    """
    render_html_to_png(svg_doc(1920, 1080, left_svg, "#0B0E14"), base_png, 1920, 1080, transparent=False)
    render_html_to_png(svg_doc(1920, 1080, right_svg, bg=None), right_png, 1920, 1080, transparent=True)
    fc = "[1:v]format=rgba,fade=t=in:st=1.4:d=0.45:alpha=1[rf];[0:v][rf]overlay=0:0:shortest=1,format=yuv420p"
    run_ffmpeg([
        "-loop", "1", "-framerate", "30", "-t", f"{dur:.3f}", "-i", str(base_png),
        "-loop", "1", "-framerate", "30", "-t", f"{dur:.3f}", "-i", str(right_png),
        "-filter_complex", fc, "-c:v", "libx264", "-preset", "fast", "-crf", "18", str(out_mp4),
    ])


def build_end_slate_16x9(out_mp4: Path, dur: float) -> None:
    """Beat 7B: Clean channel end slate + compliance disclosure."""
    slate_png = MOTION_DIR / "end_slate_16x9.png"
    svg = """
      <rect x="130" y="110" width="1660" height="860" rx="12" fill="#0E121B" stroke="#1E2532" stroke-width="1.5"/>
      <text x="960" y="340" fill="#E5A93B" font-size="24" font-weight="700" letter-spacing="5" font-family="SF Mono, Menlo, monospace" text-anchor="middle">NEXT IN EPISODE 01</text>
      <text x="960" y="445" fill="#F8FAFC" font-size="68" font-weight="700" text-anchor="middle">HOW MARKETS BREAK</text>
      <line x1="760" y1="495" x2="1160" y2="495" stroke="#E5A93B" stroke-width="3"/>
      <text x="960" y="565" fill="#CBD5E1" font-size="30" text-anchor="middle">Three Liquidity Signals That Separate a Violent Flush from a True Bear Market</text>
      <rect x="740" y="635" width="440" height="66" rx="6" fill="#182030" stroke="#38BDF8" stroke-width="2"/>
      <text x="960" y="677" fill="#38BDF8" font-size="24" font-weight="700" letter-spacing="2" font-family="SF Mono, Menlo, monospace" text-anchor="middle">SUBSCRIBE FOR EPISODE 01</text>
      <text x="960" y="905" fill="#64748B" font-size="18" font-family="SF Mono, Menlo, monospace" text-anchor="middle">Educational market mechanics &amp; public data breakdown · Not financial advice · Contains AI-assisted visuals &amp; narration</text>
    """
    render_html_to_png(svg_doc(1920, 1080, svg, "#0B0E14"), slate_png, 1920, 1080, transparent=False)
    run_ffmpeg([
        "-loop", "1", "-framerate", "30", "-t", f"{dur:.3f}", "-i", str(slate_png),
        "-vf", "fade=t=in:st=0:d=0.45,format=yuv420p",
        "-c:v", "libx264", "-preset", "fast", "-crf", "18", str(out_mp4),
    ])


def main() -> None:
    MOTION_DIR.mkdir(parents=True, exist_ok=True)
    snap = json.loads(SNAP_PATH.read_text(encoding="utf-8"))
    tl = json.loads(TIMELINE_PATH.read_text(encoding="utf-8"))
    pause = float(tl.get("pause_between_beats_sec", 0.45))
    durs = {b["beat_id"]: float(b["duration_sec"]) for b in tl["beats"]}

    # Planned visual segment durations synced to narration beats
    # Beat 1 (11.78+0.45 = 12.23s): Shot 01 (6.0s) + Hook Card (6.23s)
    build_hook_card_16x9(snap, MOTION_DIR / "beat01b_hook_card.mp4", round(durs["beat01"] + pause - 6.0, 3))
    # Beat 2 (13.87+0.45 = 14.32s): Animated Chart 01
    build_chart01_animated_16x9(snap, MOTION_DIR / "beat02_chart01.mp4", round(durs["beat02"] + pause, 3))
    # Beat 4 (11.57+0.45 = 12.02s): Animated Chart 02
    build_chart02_animated_16x9(snap, MOTION_DIR / "beat04_chart02.mp4", round(durs["beat04"] + pause, 3))
    # Beat 5 (15.19+0.45 = 15.64s): Shot 03 (6.0s) + Margin Cascade (9.64s)
    build_margin_cascade_16x9(snap, MOTION_DIR / "beat05b_cascade.mp4", round(durs["beat05"] + pause - 6.0, 3))
    # Beat 6 (13.39+0.45 = 13.84s): Shot 04 (6.0s) + Liquidity vs Bear (7.84s)
    build_liquidity_vs_bear_16x9(MOTION_DIR / "beat06b_lvb.mp4", round(durs["beat06"] + pause - 6.0, 3))
    # Beat 7 (10.90+2.50 = 13.40s): Shot 05 (6.5s) + End Slate (6.90s)
    build_end_slate_16x9(MOTION_DIR / "beat07b_end_slate.mp4", round(durs["beat07"] + 2.50 - 6.5, 3))
    print("MOTION_CARDS_READY")


if __name__ == "__main__":
    main()
