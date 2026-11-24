import http.server
import json
import subprocess
import sys
import tempfile
import threading
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MOTION_SCRIPT = ROOT / "scripts" / "motion_check.py"
SNAP_SCRIPT = ROOT / "scripts" / "snap_news.mjs"


class _QuietHandler(http.server.SimpleHTTPRequestHandler):
    html_payload = b""

    def do_GET(self) -> None:
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(self.html_payload)))
        self.end_headers()
        self.wfile.write(self.html_payload)

    def log_message(self, fmt: str, *args: object) -> None:
        return


class TestVideoQaTools(unittest.TestCase):
    def test_motion_check_detects_static_hold_and_outputs_json(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_dir = Path(tmp)
            static_mp4 = tmp_dir / "static.mp4"
            moving_mp4 = tmp_dir / "moving.mp4"
            joined_mp4 = tmp_dir / "joined.mp4"
            concat_txt = tmp_dir / "concat.txt"

            # 2.5s frozen noise pattern (textured so optical flow evaluates real pixels)
            subprocess.run(
                [
                    "ffmpeg",
                    "-y",
                    "-v",
                    "error",
                    "-f",
                    "lavfi",
                    "-i",
                    "mandelbrot=size=320x180:rate=30,trim=duration=0.05,loop=loop=74:size=1:start=0,setpts=N/FRAME_RATE/TB",
                    "-t",
                    "2.5",
                    "-pix_fmt",
                    "yuv420p",
                    str(static_mp4),
                ],
                check=True,
            )
            # 1.5s moving mandelbrot zoom
            subprocess.run(
                [
                    "ffmpeg",
                    "-y",
                    "-v",
                    "error",
                    "-f",
                    "lavfi",
                    "-i",
                    "mandelbrot=size=320x180:rate=30",
                    "-t",
                    "1.5",
                    "-pix_fmt",
                    "yuv420p",
                    str(moving_mp4),
                ],
                check=True,
            )
            concat_txt.write_text(f"file '{static_mp4}'\nfile '{moving_mp4}'\n", encoding="utf-8")
            subprocess.run(
                [
                    "ffmpeg",
                    "-y",
                    "-v",
                    "error",
                    "-f",
                    "concat",
                    "-safe",
                    "0",
                    "-i",
                    str(concat_txt),
                    "-c",
                    "copy",
                    str(joined_mp4),
                ],
                check=True,
            )

            res = subprocess.run(
                [sys.executable, str(MOTION_SCRIPT), str(joined_mp4), "--json"],
                capture_output=True,
                text=True,
                check=True,
            )
            data = json.loads(res.stdout)
            self.assertIn(str(joined_mp4), data)
            entry = data[str(joined_mp4)]
            for key in ("still", "hold2", "cam", "layer", "nonuni", "pushpull", "zoom", "p75", "cutmin"):
                self.assertIn(key, entry)
            self.assertTrue(any(h >= 2.0 for h in entry["_holds"]), f"Expected hold >= 2s, got {entry['_holds']}")

    def test_snap_news_strips_overlay_captures_png_and_locates_keyword(self) -> None:
        html = """<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><title>Test Market Report</title></head>
<body style="margin:0;padding:40px;font-family:sans-serif;height:2000px;">
  <div id="cookie-banner" style="position:fixed;top:0;left:0;right:0;height:80px;background:#111;color:#fff;z-index:999;">
    Cookie Consent Banner
  </div>
  <h1 style="margin-top:60px;">AI Infrastructure Spending Hits Record High</h1>
  <p style="font-size:20px;line-height:1.6;">
    Analysts estimate capital expenditures will reach $280 billion by 2030 across hyperscale clouds.
  </p>
</body>
</html>"""
        _QuietHandler.html_payload = html.encode("utf-8")
        server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), _QuietHandler)
        port = server.server_address[1]
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()

        try:
            with tempfile.TemporaryDirectory() as tmp:
                tmp_dir = Path(tmp)
                jobs_path = tmp_dir / "jobs.json"
                jobs_path.write_text(
                    json.dumps(
                        [
                            {
                                "id": "capex",
                                "url": f"http://127.0.0.1:{port}/article.html",
                                "find": ["$280 billion by 2030"],
                                "off": 80,
                                "waitMs": 200,
                            }
                        ]
                    ),
                    encoding="utf-8",
                )
                subprocess.run(
                    ["node", str(SNAP_SCRIPT), str(jobs_path)],
                    capture_output=True,
                    text=True,
                    check=True,
                    timeout=30,
                )
                png_path = tmp_dir / "docs" / "capex.png"
                meta_path = tmp_dir / "docs" / "news.json"
                self.assertTrue(png_path.exists() and png_path.stat().st_size > 1000)
                self.assertTrue(meta_path.exists())
                meta = json.loads(meta_path.read_text(encoding="utf-8"))
                self.assertIn("capex", meta)
                hits = meta["capex"]["hits"]
                self.assertEqual(len(hits), 1)
                self.assertEqual(hits[0]["k"], "$280 billion by 2030")
                self.assertTrue(len(hits[0]["rects"]) >= 1)
                self.assertEqual(len(hits[0]["rects"][0]), 4)
        finally:
            server.shutdown()
            server.server_close()


if __name__ == "__main__":
    unittest.main()
