import subprocess
import platform

def detect_gpu():
    system = platform.system()

    # NVIDIA
    try:
        subprocess.check_output(["nvidia-smi"])
        return "nvidia"
    except:
        pass

    # Intel Quick Sync
    try:
        output = subprocess.check_output(
            ["ffmpeg", "-hide_banner", "-encoders"],
            stderr=subprocess.STDOUT
        ).decode()

        if "qsv" in output:
            return "intel"
    except:
        pass

    # AMD
    try:
        output = subprocess.check_output(
            ["ffmpeg", "-hide_banner", "-encoders"],
            stderr=subprocess.STDOUT
        ).decode()

        if "amf" in output:
            return "amd"
    except:
        pass

    # macOS VideoToolbox
    if system == "Darwin":
        return "mac"

    return "cpu"