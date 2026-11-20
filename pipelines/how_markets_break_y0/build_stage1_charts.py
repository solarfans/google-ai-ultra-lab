#!/usr/bin/env python3
"""
Stage-1 Live Market Snapshot Fetcher & Broadcast Dark-Terminal Chart Renderer (0 Flow / $0 GCP).
Fetches daily closes from Yahoo Finance (Nov 2026 window), persists auditable JSON, and renders
two 1920x1080 institutional Matte Carbon SVG/HTML charts via headless Google Chrome.
"""
from __future__ import annotations

import datetime
import html
import json
import subprocess
import tempfile
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
CHARTS_DIR = ROOT / "charts"
KEYFRAMES_DIR = ROOT / "keyframes"
CHROME_BIN = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

SYMBOLS = [
    ("ixic", "Nasdaq Composite (^IXIC)", "^IXIC"),
    ("ndx", "Nasdaq 100 (^NDX)", "^NDX"),
    ("gold", "Gold Futures (GC=F)", "GC=F"),
    ("btc", "Bitcoin (BTC-USD)", "BTC-USD"),
    ("us10y", "US 10Y Yield (^TNX)", "^TNX"),
    ("dxy", "US Dollar Index (DXY)", "DX-Y.NYB"),
    ("vix", "CBOE Volatility (^VIX)", "^VIX"),
]


def fetch_yahoo_daily(symbol: str, window_start: str = "2026-11-04") -> list[dict[str, Any]]:
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


def render_html_to_png(html_content: str, out_png: Path) -> None:
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
            "--window-size=1920,1080",
            "--force-device-scale-factor=1",
            f"--screenshot={out_png}",
            html_path.as_uri(),
        ]
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=30, check=False)
        if res.returncode != 0 or not out_png.is_file() or out_png.stat().st_size < 10_000:
            raise RuntimeError(f"Chrome screenshot failed for {out_png}: {res.stderr[:300]}")
    finally:
        html_path.unlink(missing_ok=True)


def fmt_date_short(iso: str) -> str:
    dt = datetime.date.fromisoformat(iso)
    return dt.strftime("%b %-d")


def build_chart01_html(snapshot: dict[str, Any]) -> str:
    series_cfg = [
        ("ixic", "Nasdaq Composite", "#38BDF8", "^IXIC"),
        ("gold", "Gold Futures", "#E5A93B", "GC=F"),
        ("btc", "Bitcoin", "#E5484D", "BTC-USD"),
    ]
    all_dates = sorted({pt["date"] for key, *_ in series_cfg for pt in snapshot["series"][key]["points"]})
    date_idx = {d: i for i, d in enumerate(all_dates)}

    # SVG plot bounds inside 1920x1080 canvas
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
        grid_lines.append(
            f'<line x1="{PL}" y1="{yy:.1f}" x2="{PL + PW}" y2="{yy:.1f}" stroke="{stroke}" stroke-width="{sw}" {dash}/>'
        )
        grid_lines.append(
            f'<text x="{PL - 22}" y="{yy + 7:.1f}" fill="#8B96A8" font-size="22" font-family="SF Mono, Menlo, monospace" text-anchor="end">{tick}%</text>'
        )

    # X axis date labels every 3 steps, always including last, dropping adjacent penultimate to prevent overlap
    x_ticks = []
    shown = {i for i in range(0, len(all_dates), 3) if i < len(all_dates) - 2} | {len(all_dates) - 1}
    for idx in sorted(shown):
        d = all_dates[idx]
        xx = x_px(d)
        x_ticks.append(f'<line x1="{xx:.1f}" y1="{PT}" x2="{xx:.1f}" y2="{PT + PH}" stroke="#161C27" stroke-width="1"/>')
        x_ticks.append(
            f'<text x="{xx:.1f}" y="{PT + PH + 42}" fill="#8B96A8" font-size="21" font-family="SF Mono, Menlo, monospace" text-anchor="middle">{html.escape(fmt_date_short(d))}</text>'
        )

    paths_svg = []
    badges = []
    for key, label, color, ticker in series_cfg:
        s = snapshot["series"][key]
        hi = s["high_close"]
        pts_xy = []
        peak_xy = None
        for pt in s["points"]:
            dd = (pt["close"] - hi) / hi * 100.0
            xx, yy = x_px(pt["date"]), y_px(dd)
            pts_xy.append((xx, yy, dd, pt["date"], pt["close"]))
            if pt["date"] == s["high_date"]:
                peak_xy = (xx, yy)

        d_attr = " ".join(("M" if i == 0 else "L") + f"{x:.1f},{y:.1f}" for i, (x, y, *_) in enumerate(pts_xy))
        paths_svg.append(
            f'<path d="{d_attr}" fill="none" stroke="{color}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round" opacity="0.96"/>'
        )
        if peak_xy:
            paths_svg.append(
                f'<circle cx="{peak_xy[0]:.1f}" cy="{peak_xy[1]:.1f}" r="6" fill="#0B0E14" stroke="{color}" stroke-width="3"/>'
            )
        lx, ly, ldd, ldate, lval = pts_xy[-1]
        paths_svg.append(
            f'<circle cx="{lx:.1f}" cy="{ly:.1f}" r="9" fill="{color}" stroke="#0B0E14" stroke-width="3"/>'
        )
        badges.append({
            "raw_y": ly,
            "color": color,
            "label": label,
            "ticker": ticker,
            "dd": ldd,
            "hi": hi,
            "last": lval,
            "hi_date": fmt_date_short(s["high_date"]),
            "last_date": fmt_date_short(ldate),
        })

    # Enforce vertical spacing for right-hand callout badges
    badges.sort(key=lambda b: b["raw_y"])
    min_gap = 128.0
    for i in range(1, len(badges)):
        if badges[i]["raw_y"] - badges[i - 1]["raw_y"] < min_gap:
            badges[i]["raw_y"] = badges[i - 1]["raw_y"] + min_gap

    badges_svg = []
    bx = PL + PW + 28
    bw = 360
    bh = 108
    for b in badges:
        by = min(max(PT, b["raw_y"] - bh / 2), PT + PH - bh)
        if b["ticker"] == "^IXIC":
            range_str = f"{b['hi']:,.0f} ({b['hi_date']}) → {b['last']:,.0f}"
        else:
            range_str = f"${b['hi']:,.0f} ({b['hi_date']}) → ${b['last']:,.0f}"
        badges_svg.append(f"""
        <g>
          <rect x="{bx}" y="{by:.1f}" width="{bw}" height="{bh}" rx="6" fill="#121722" stroke="{b['color']}" stroke-width="2" stroke-opacity="0.75"/>
          <rect x="{bx}" y="{by:.1f}" width="6" height="{bh}" rx="2" fill="{b['color']}"/>
          <text x="{bx + 20}" y="{by + 33:.1f}" fill="#E6ECF5" font-size="22" font-weight="600" font-family="-apple-system, BlinkMacSystemFont, Inter, sans-serif">{html.escape(b['label'])}</text>
          <text x="{bx + bw - 18}" y="{by + 36:.1f}" fill="{b['color']}" font-size="28" font-weight="700" font-family="SF Mono, Menlo, monospace" text-anchor="end">{b['dd']:+.2f}%</text>
          <text x="{bx + 20}" y="{by + 68:.1f}" fill="#8B96A8" font-size="18" font-family="SF Mono, Menlo, monospace">{html.escape(range_str)}</text>
          <text x="{bx + 20}" y="{by + 92:.1f}" fill="#5F6B7E" font-size="16" font-family="SF Mono, Menlo, monospace">Latest close: {html.escape(b['last_date'])}</text>
        </g>
        """)

    return f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="utf-8"><style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  html, body {{ width: 1920px; height: 1080px; overflow: hidden; background: #0B0E14; font-family: -apple-system, BlinkMacSystemFont, "Inter", sans-serif; color: #F1F5F9; }}
</style></head>
<body>
<svg width="1920" height="1080" viewBox="0 0 1920 1080" xmlns="http://www.w3.org/2000/svg">
  <rect width="1920" height="1080" fill="#0B0E14"/>
  <rect x="64" y="54" width="1792" height="972" fill="#0E121B" stroke="#1E2532" stroke-width="1.5" rx="8"/>
  <text x="130" y="106" fill="#E5A93B" font-size="18" font-weight="700" letter-spacing="3" font-family="SF Mono, Menlo, monospace">HOW MARKETS BREAK  |  THE BROKEN SAFE-HAVEN PARADOX (NOV 4–20, 2026)</text>
  <text x="130" y="156" fill="#F8FAFC" font-size="42" font-weight="700">Everything Fell Together — Even Gold Dropped Nearly 2x Harder Than Tech</text>
  <text x="130" y="196" fill="#94A3B8" font-size="22">Normalized drawdown (%) from each asset's November 2026 peak daily close</text>
  {''.join(x_ticks)}
  {''.join(grid_lines)}
  <line x1="{PL}" y1="{PT}" x2="{PL}" y2="{PT + PH}" stroke="#2A3447" stroke-width="1.5"/>
  <line x1="{PL}" y1="{PT + PH}" x2="{PL + PW}" y2="{PT + PH}" stroke="#2A3447" stroke-width="1.5"/>
  {''.join(paths_svg)}
  {''.join(badges_svg)}
  <text x="130" y="998" fill="#64748B" font-size="18" font-family="SF Mono, Menlo, monospace">Source: Yahoo Finance daily closes (^IXIC, GC=F, BTC-USD) as of Nov 20, 2026 · Educational market mechanics, not financial advice</text>
</svg>
</body>
</html>"""


def build_chart02_html(snapshot: dict[str, Any]) -> str:
    panels_cfg = [
        {
            "key": "us10y",
            "title": "10Y US TREASURY YIELD",
            "subtitle": "Risk-free hurdle breached 5.00%",
            "color": "#E5484D",
            "unit": "%",
            "threshold": 5.00,
            "threshold_label": "5.00% DANGER LINE",
            "y_min": 4.70,
            "y_max": 5.25,
            "delta_label": lambda s: f"{s['first_close']:.2f}% → {s['last_close']:.2f}% (Peak {s['high_close']:.2f}%)",
        },
        {
            "key": "dxy",
            "title": "US DOLLAR INDEX (DXY)",
            "subtitle": "Global USD scramble tightens liquidity",
            "color": "#38BDF8",
            "unit": "",
            "threshold": None,
            "threshold_label": "",
            "y_min": 101.0,
            "y_max": 104.5,
            "delta_label": lambda s: f"{s['low_close']:.2f} ({fmt_date_short(s['low_date'])}) → {s['last_close']:.2f} ({s['pct_from_low']:+.2f}%)",
        },
        {
            "key": "vix",
            "title": "CBOE VOLATILITY (^VIX)",
            "subtitle": "Fear gauge surging toward 30 panic line",
            "color": "#E5A93B",
            "unit": "",
            "threshold": 30.0,
            "threshold_label": "30.0 STRESS LINE",
            "y_min": 14.0,
            "y_max": 33.0,
            "delta_label": lambda s: f"{s['low_close']:.2f} ({fmt_date_short(s['low_date'])}) → {s['last_close']:.2f} ({s['pct_from_low']:+.1f}%)",
        },
    ]

    panel_svgs = []
    px0 = 110
    gap = 46
    pw_total = 536
    py0 = 240
    ph_total = 690

    for idx, cfg in enumerate(panels_cfg):
        s = snapshot["series"][cfg["key"]]
        pts = s["points"]
        x_box = px0 + idx * (pw_total + gap)
        # Inner plot area
        ipl, ipr, ipt, ipb = x_box + 56, x_box + pw_total - 28, py0 + 188, py0 + ph_total - 70
        ipw = ipr - ipl
        iph = ipb - ipt
        ymin, ymax = cfg["y_min"], cfg["y_max"]

        def px(i: int, n: int = len(pts)) -> float:
            return ipl + (i / max(1, n - 1)) * ipw

        def py(v: float) -> float:
            return ipt + ((ymax - v) / (ymax - ymin)) * iph

        p_lines = []
        # 4 horizontal guides
        for k in range(4):
            val = ymin + (ymax - ymin) * k / 3.0
            yy = py(val)
            p_lines.append(f'<line x1="{ipl}" y1="{yy:.1f}" x2="{ipr}" y2="{yy:.1f}" stroke="#1B2230" stroke-width="1"/>')
            p_lines.append(
                f'<text x="{ipl - 8}" y="{yy + 5:.1f}" fill="#64748B" font-size="16" font-family="SF Mono, Menlo, monospace" text-anchor="end">{val:.1f}{cfg["unit"]}</text>'
            )

        if cfg["threshold"] is not None:
            ty = py(cfg["threshold"])
            p_lines.append(f'<line x1="{ipl}" y1="{ty:.1f}" x2="{ipr}" y2="{ty:.1f}" stroke="#F87171" stroke-width="2" stroke-dasharray="6 6" opacity="0.85"/>')
            p_lines.append(f'<text x="{ipr}" y="{ty - 10:.1f}" fill="#F87171" font-size="15" font-weight="700" font-family="SF Mono, Menlo, monospace" text-anchor="end">{cfg["threshold_label"]}</text>')

        coords = [(px(i), py(pt["close"]), pt) for i, pt in enumerate(pts)]
        d_path = " ".join(("M" if i == 0 else "L") + f"{x:.1f},{y:.1f}" for i, (x, y, _) in enumerate(coords))
        area_path = f"{d_path} L{coords[-1][0]:.1f},{ipb:.1f} L{coords[0][0]:.1f},{ipb:.1f} Z"
        p_lines.append(f'<path d="{area_path}" fill="{cfg["color"]}" fill-opacity="0.10"/>')
        p_lines.append(f'<path d="{d_path}" fill="none" stroke="{cfg["color"]}" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"/>')
        lx, ly, lpt = coords[-1]
        p_lines.append(f'<circle cx="{lx:.1f}" cy="{ly:.1f}" r="8" fill="{cfg["color"]}" stroke="#0B0E14" stroke-width="2.5"/>')

        p_lines.append(
            f'<text x="{ipl}" y="{ipb + 36}" fill="#8B96A8" font-size="17" font-family="SF Mono, Menlo, monospace">{html.escape(fmt_date_short(pts[0]["date"]))}</text>'
        )
        p_lines.append(
            f'<text x="{ipr}" y="{ipb + 36}" fill="#8B96A8" font-size="17" font-family="SF Mono, Menlo, monospace" text-anchor="end">{html.escape(fmt_date_short(pts[-1]["date"]))}</text>'
        )

        big_val = f"{s['last_close']:.2f}{cfg['unit']}"
        delta_txt = cfg["delta_label"](s)
        panel_svgs.append(f"""
        <g>
          <rect x="{x_box}" y="{py0}" width="{pw_total}" height="{ph_total}" rx="8" fill="#0E121B" stroke="#1E2532" stroke-width="1.5"/>
          <rect x="{x_box}" y="{py0}" width="{pw_total}" height="5" rx="2" fill="{cfg['color']}"/>
          <text x="{x_box + 32}" y="{py0 + 44}" fill="{cfg['color']}" font-size="19" font-weight="700" letter-spacing="1.5" font-family="SF Mono, Menlo, monospace">{html.escape(cfg['title'])}</text>
          <text x="{x_box + 32}" y="{py0 + 74}" fill="#94A3B8" font-size="18">{html.escape(cfg['subtitle'])}</text>
          <text x="{x_box + 32}" y="{py0 + 124}" fill="#F8FAFC" font-size="40" font-weight="700" font-family="SF Mono, Menlo, monospace">{html.escape(big_val)}</text>
          <text x="{x_box + 32}" y="{py0 + 154}" fill="#CBD5E1" font-size="17" font-family="SF Mono, Menlo, monospace">{html.escape(delta_txt)}</text>
          {''.join(p_lines)}
        </g>
        """)

    return f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="utf-8"><style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  html, body {{ width: 1920px; height: 1080px; overflow: hidden; background: #0B0E14; font-family: -apple-system, BlinkMacSystemFont, "Inter", sans-serif; color: #F1F5F9; }}
</style></head>
<body>
<svg width="1920" height="1080" viewBox="0 0 1920 1080" xmlns="http://www.w3.org/2000/svg">
  <rect width="1920" height="1080" fill="#0B0E14"/>
  <text x="110" y="102" fill="#E5A93B" font-size="18" font-weight="700" letter-spacing="3" font-family="SF Mono, Menlo, monospace">HOW MARKETS BREAK  |  MACRO PRESSURE GAUGES (NOV 4–20, 2026)</text>
  <text x="110" y="156" fill="#F8FAFC" font-size="44" font-weight="700">The Real Culprit: Cash-Is-King Liquidity Squeeze</text>
  <text x="110" y="198" fill="#94A3B8" font-size="22">Rising yields, a surging dollar, and spiking volatility force indiscriminate margin liquidation</text>
  {''.join(panel_svgs)}
  <text x="110" y="998" fill="#64748B" font-size="18" font-family="SF Mono, Menlo, monospace">Source: Yahoo Finance daily closes (^TNX, DX-Y.NYB, ^VIX) as of Nov 20, 2026 · Educational market mechanics, not financial advice</text>
</svg>
</body>
</html>"""


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    CHARTS_DIR.mkdir(parents=True, exist_ok=True)
    KEYFRAMES_DIR.mkdir(parents=True, exist_ok=True)

    snapshot: dict[str, Any] = {
        "fetched_at_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "window_start": "2026-11-04",
        "series": {},
    }
    for key, label, symbol in SYMBOLS:
        pts = fetch_yahoo_daily(symbol, window_start="2026-11-04")
        summary = summarize_series(pts)
        summary["label"] = label
        summary["symbol"] = symbol
        snapshot["series"][key] = summary

    snap_path = DATA_DIR / "market_snapshot_20261120.json"
    snap_path.write_text(json.dumps(snapshot, indent=2, ensure_ascii=False), encoding="utf-8")

    c1 = CHARTS_DIR / "chart01_cross_asset_crash.png"
    c2 = CHARTS_DIR / "chart02_liquidity_culprits.png"
    render_html_to_png(build_chart01_html(snapshot), c1)
    render_html_to_png(build_chart02_html(snapshot), c2)
    print(json.dumps({"ok": True, "snapshot": str(snap_path), "charts": [str(c1), str(c2)]}, indent=2))


if __name__ == "__main__":
    main()
