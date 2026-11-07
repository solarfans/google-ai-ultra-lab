import subprocess
import sys

print("=== Colab VM Hardware Probe ===", flush=True)
print("Python version:", sys.version, flush=True)

# Run nvidia-smi
try:
    smi = subprocess.check_output(["nvidia-smi"], text=True)
    print("\n=== nvidia-smi ===\n" + smi, flush=True)
except Exception as e:
    print("nvidia-smi check:", e, flush=True)

# Check host RAM and Disk
try:
    meminfo = subprocess.check_output(["free", "-h"], text=True)
    print("=== System RAM ===\n" + meminfo, flush=True)
    df = subprocess.check_output(["df", "-h", "/"], text=True)
    print("=== Root Disk ===\n" + df, flush=True)
except Exception as e:
    print("host info check:", e, flush=True)
