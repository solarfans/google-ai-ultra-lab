#!/usr/bin/env python3
import sys
import subprocess
import torch

print("=== Colab G4 InsightFace Probe ===")
print("CUDA:", torch.cuda.is_available(), "GPU:", torch.cuda.get_device_name(0))

subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "insightface", "onnxruntime-gpu", "opencv-python"])

import insightface
from insightface.app import FaceAnalysis
print("InsightFace version:", insightface.__version__)

app = FaceAnalysis(name='buffalo_l')
app.prepare(ctx_id=0, det_size=(640, 640))
print("Buffalo_l prepared successfully on GPU!")
