#!/usr/bin/env python3
import json
import os
import sys
from google_auth_oauthlib.flow import InstalledAppFlow

config_path = os.path.expanduser(
    "~/.local/share/uv/tools/google-colab-cli/lib/python3.12/site-packages/colab_cli/oauth_config.json"
)
with open(config_path) as f:
    config = json.load(f)

SCOPES = [
    "openid",
    "https://www.googleapis.com/auth/userinfo.profile",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/cloud-platform",
    "https://www.googleapis.com/auth/colaboratory",
    "https://www.googleapis.com/auth/drive.file",
]

flow = InstalledAppFlow.from_client_config(config, SCOPES)

# Print instructions and run local server on port 8085
print("Starting local OAuth listener on http://localhost:8085 ...", flush=True)
creds = flow.run_local_server(port=8085, open_browser=False)

token_path = os.path.expanduser("~/.config/colab-cli/token.json")
os.makedirs(os.path.dirname(token_path), exist_ok=True)
with open(token_path, "w") as f:
    f.write(creds.to_json())

print(f"SUCCESS: Authentication complete! Token saved to {token_path}", flush=True)
