import os, time, base64, requests
from google import genai
from google.genai import types
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

PROJECT = "project-665ac784-237e-4a71-ad0"
BASE = "/Users/kaykel/AI_PROJECTS/AI OS Backup_Mac/google-ai-ultra-lab/pipelines/warcraft_illidan_ep01"
ASSETS = f"{BASE}/assets"
OUT_DIR = f"{BASE}/renders"
os.makedirs(OUT_DIR, exist_ok=True)

def get_client():
    creds = Credentials.from_authorized_user_file(os.path.expanduser("~/.config/colab-cli/token.json"))
    creds.refresh(Request())
    return creds, genai.Client(
        vertexai=True,
        project=PROJECT,
        location="us-central1",
        credentials=creds,
        http_options=types.HttpOptions(headers={"x-goog-user-project": PROJECT})
    )

creds, client = get_client()

# Generate Climax Brass & Timpani Score Stem via Lyria-002
climax_wav = f"{OUT_DIR}/illidan_lyria_climax.wav"
if not os.path.exists(climax_wav):
    url = f"https://us-central1-aiplatform.googleapis.com/v1/projects/{PROJECT}/locations/us-central1/publishers/google/models/lyria-002:predict"
    r = requests.post(
        url,
        headers={"Authorization": f"Bearer {creds.token}", "x-goog-user-project": PROJECT, "Content-Type": "application/json"},
        json={
            "instances": [{
                "prompt": "Epic dark fantasy orchestral climax in D minor, powerful brass horns, dramatic staccato strings, thunderous cinematic war drums and timpani swells, dark heroic tragedy, monumental movie trailer finale score, 76 bpm",
                "negative_prompt": "cheerful, pop, electronic, guitar, fast dance"
            }],
            "parameters": {}
        },
        timeout=90
    )
    if r.status_code == 200 and r.json().get("predictions"):
        b64 = r.json()["predictions"][0].get("bytesBase64Encoded") or r.json()["predictions"][0].get("audioContent")
        with open(climax_wav, "wb") as f:
            f.write(base64.b64decode(b64))
        print("Saved climax score:", climax_wav)

shots = [
    {
        "name": "shot01_skull_macro",
        "mode": "i2v",
        "image_path": f"{ASSETS}/shot01_skull_macro.jpg",
        "duration": 4,
        "prompt": (
            "Photorealistic live-action dark-fantasy macro shot on ARRI Alexa 65 anamorphic lens in pouring night rain. "
            "Slow tense push-in as the dusky-violet clawed hand tightens violently around the ancient horned demon skull in the wet mud; "
            "blinding neon emerald-green fel lightning and green flames fracture outward through the skull's eye sockets and bone cracks, "
            "evaporating splashing raindrops into glowing green steam. Deep sub-bass arcane hum, bone cracking sound, heavy rain and thunder, no speech, no music, no text."
        )
    },
    {
        "name": "shot03_arrival",
        "mode": "i2v",
        "image_path": f"{ASSETS}/shot03_arrival.jpg",
        "duration": 4,
        "prompt": (
            "Photorealistic live-action dark-fantasy medium tracking shot on ARRI Alexa 65 in a misty rain-drenched forest at night. "
            "Antlered Archdruid Malfurion gripping his gnarled wooden staff and silver-haired High Priestess Tyrande step forward out of the swirling blue mist "
            "and halt abruptly in stunned horror as intense green fel light flares across their wet faces from off-screen right. "
            "Heavy footsteps splashing in forest mud, rustling wet raven-feather cloak, sharp intake of breath, pouring rain, no music, no text."
        )
    },
    {
        "name": "shot04_malfurion_cu",
        "mode": "i2v",
        "image_path": f"{ASSETS}/shot04_malfurion_cu.jpg",
        "duration": 6,
        "prompt": (
            "Photorealistic live-action dark-fantasy tight close-up on ARRI Alexa 65 in pouring night rain. "
            "Subtle handheld camera movement on Archdruid Malfurion with wooden stag antlers and wet dark-green beard, "
            "his glowing amber-gold eyes burning with horrified fury and betrayal as green fel reflections flicker on his face. "
            "He speaks in a deep, resonant, commanding ancient baritone voice with furious emotion and exact lip-sync: "
            "\"What have you done, Illidan?! You carry the Legion's taint within your soul!\" "
            "Authentic heavy rain sound, distant rumble of thunder, zero music, no subtitles, no text."
        )
    },
    {
        "name": "shot05_illidan_cu",
        "mode": "i2v",
        "image_path": f"{ASSETS}/shot05_illidan_cu.jpg",
        "duration": 6,
        "prompt": (
            "Photorealistic live-action dark-fantasy reverse-angle tight close-up on ARRI Alexa 65 in pouring night rain. "
            "Demon-transformed Illidan Stormrage with ridged obsidian horns and a rain-soaked black linen blindfold glowing fiercely with emerald fel fire "
            "turns slightly toward his brother, jaw trembling with heartbroken anguish and bitter defiance as rain streams down his scarred skin. "
            "He speaks in a deep, gravelly, resonant demonic baritone voice with raw emotion and exact lip-sync: "
            "\"Power was the only way to save our world... to save HER!\" "
            "Pouring rain, subtle crackle of green fel energy, zero music, no subtitles, no text."
        )
    },
    {
        "name": "shot06_tyrande_cu",
        "mode": "i2v",
        "image_path": f"{ASSETS}/shot06_tyrande_cu.jpg",
        "duration": 6,
        "prompt": (
            "Photorealistic live-action dark-fantasy tight emotional close-up on ARRI Alexa 65 in pouring night rain. "
            "High Priestess Tyrande with frost-silver braided hair and silver crescent circlet gazes with sorrowful luminous silver eyes as tears mix with rain on her cheek; "
            "she whispers in a heartbroken, ethereal female voice with exact lip-sync: "
            "\"Illidan... I cannot bear what you have become.\" "
            "Then she sorrowfully lowers her gaze and turns her face slightly away in grief. Soft rain pattering on silver armor, zero music, no subtitles, no text."
        )
    },
    {
        "name": "shot08_skyward_leap",
        "mode": "r2v",
        "ref_path": f"{ASSETS}/ref_illidan_front.jpg",
        "duration": 8,
        "prompt": (
            "Photorealistic live-action dark-fantasy wide low-angle cinema shot on ARRI Alexa 65 anamorphic lens at night in a storm-lashed ancient forest beneath a giant pale full moon. "
            "Demon-transformed Illidan Stormrage stands in the rain-soaked clearing with glowing emerald chest tattoos, black blindfold, curved horns, and twin curved blades glowing with pure emerald-green fel fire. "
            "He unfurls his massive tattered leathery demon wings wide, crouches powerfully, and launches himself violently skyward into the lightning-lit storm clouds, "
            "sending a shockwave ring of rain spray and emerald fel embers across the forest floor. "
            "Thunderous wingbeats, explosive arcane shockwave boom, roaring storm wind and rain, no speech, no music, no text."
        )
    }
]

# Run in batches of 2 to respect Vertex AI concurrent RPM smoothly
for i in range(0, len(shots), 2):
    batch = shots[i:i+2]
    creds, client = get_client()
    active_ops = []
    for s in batch:
        out_path = f"{OUT_DIR}/{s['name']}.mp4"
        if os.path.exists(out_path) and os.path.getsize(out_path) > 500_000:
            print(f"Skipping already rendered {s['name']}")
            continue
        for attempt in range(4):
            try:
                print(f"Submitting {s['name']} (attempt {attempt+1})...")
                if s["mode"] == "i2v":
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
                            negative_prompt="cartoon, anime, 3d game render, plastic skin, subtitles, captions, text, watermark, logo, deformed"
                        )
                    )
                else:
                    ref_img = types.Image.from_file(location=s["ref_path"])
                    op = client.models.generate_videos(
                        model="veo-3.1-generate-001",
                        prompt=s["prompt"],
                        config=types.GenerateVideosConfig(
                            aspect_ratio="16:9",
                            resolution="1080p",
                            duration_seconds=8,
                            generate_audio=True,
                            person_generation="allow_adult",
                            reference_images=[
                                types.VideoGenerationReferenceImage(
                                    image=ref_img,
                                    reference_type=types.VideoGenerationReferenceType.ASSET
                                )
                            ],
                            negative_prompt="cartoon, anime, 3d game render, plastic skin, subtitles, captions, text, watermark, logo, split screen"
                        )
                    )
                print(f"  -> Started {s['name']}: {op.name}")
                active_ops.append((s["name"], op))
                break
            except Exception as e:
                print(f"  [WARN] {s['name']} submit error: {e}")
                time.sleep(20)
    for name, op in active_ops:
        while not op.done:
            time.sleep(8)
            creds, client = get_client()
            op = client.operations.get(op)
        if op.error:
            print(f"  [{name}] ERROR: {op.error}")
        elif op.response and op.response.generated_videos:
            vid_bytes = op.response.generated_videos[0].video.video_bytes
            out_path = f"{OUT_DIR}/{name}.mp4"
            with open(out_path, "wb") as f:
                f.write(vid_bytes)
            print(f"  [{name}] SAVED {out_path} ({len(vid_bytes):,} bytes)")
print("ALL BATCHES COMPLETE!")
