import os, time, sys
from google import genai
from google.genai import types
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

PROJECT = "project-665ac784-237e-4a71-ad0"
BASE = "/Users/kaykel/AI_PROJECTS/AI OS Backup_Mac/google-ai-ultra-lab/pipelines/warcraft_illidan_ep01"
OUT_DIR = f"{BASE}/renders"
os.makedirs(OUT_DIR, exist_ok=True)

creds = Credentials.from_authorized_user_file(os.path.expanduser("~/.config/colab-cli/token.json"))
creds.refresh(Request())

client = genai.Client(
    vertexai=True,
    project=PROJECT,
    location="us-central1",
    credentials=creds,
    http_options=types.HttpOptions(headers={"x-goog-user-project": PROJECT})
)

shots = [
    {
        "name": "shot02_skull_absorb",
        "image_path": f"{BASE}/assets/illidan_keyframe_skull_16x9.jpg",
        "duration": 6,
        "prompt": (
            "Photorealistic live-action dark-fantasy Hollywood cinema shot on ARRI Alexa 65 anamorphic lens, heavy rain at night. "
            "Slow dramatic camera push-in as Illidan Stormrage crushes the glowing green horned demon skull in his left hand, "
            "unleashing a surge of emerald fel fire and green lightning that courses through his glowing chest tattoos while his "
            "tattered leathery demon wings spread wide behind him. Looking forward beneath his glowing green-lit black blindfold, "
            "he speaks in a deep, gravelly, resonant demonic baritone voice with exact lip-sync: "
            "\"The Legion's shadow... ends tonight.\" "
            "Authentic heavy rain sound, distant thunder crack, crackling fel fire, zero music, no subtitles, no text."
        )
    },
    {
        "name": "shot07_banishment_blades",
        "image_path": f"{BASE}/assets/illidan_keyframe_banishment_16x9.jpg",
        "duration": 6,
        "prompt": (
            "Photorealistic live-action dark-fantasy Hollywood cinema over-the-shoulder shot in pouring night rain. "
            "Subtle handheld cinema camera push past the foreground silhouettes of antlered Malfurion and silver-haired Tyrande "
            "toward demon-transformed Illidan Stormrage standing in the rain-soaked forest puddles. "
            "Illidan clenches his jaw, swings both curved Twin Blades of Azzinoth outward as roaring emerald-green fel flames "
            "erupt brighter along the blades, illuminating the rain, and speaks in a cold, heartbroken yet defiant deep gravelly baritone "
            "with exact lip-sync: \"Call me Betrayer, brother... You are NOT prepared.\" "
            "Sound of pouring rain, metallic warglaive ignition whoosh, crackling fel fire, zero background music, no subtitles, no text."
        )
    }
]

ops = []
for s in shots:
    print(f"Submitting {s['name']} to veo-3.1-generate-001...")
    img = types.Image.from_file(location=s["image_path"])
    op = client.models.generate_videos(
        model="veo-3.1-generate-001",
        prompt=s["prompt"],
        image=img,
        config=types.GenerateVideosConfig(
            aspect_ratio="16:9",
            resolution="1080p",
            duration_seconds=s["duration"],
            generate_audio=True,
            person_generation="allow_adult",
            negative_prompt="cartoon, anime, 3d game render, plastic skin, subtitles, captions, text, watermark, logo, blurry, deformed face"
        )
    )
    print(f"  -> Operation started: {op.name}")
    ops.append((s["name"], op))

for name, op in ops:
    while not op.done:
        time.sleep(8)
        op = client.operations.get(op)
        print(f"  [{name}] done={op.done}")
    if op.error:
        print(f"  [{name}] ERROR: {op.error}")
    elif op.response and op.response.generated_videos:
        vid_bytes = op.response.generated_videos[0].video.video_bytes
        out_path = f"{OUT_DIR}/{name}.mp4"
        with open(out_path, "wb") as f:
            f.write(vid_bytes)
        print(f"  [{name}] SAVED {out_path} ({len(vid_bytes):,} bytes)")
    else:
        print(f"  [{name}] Unexpected response: {op}")
