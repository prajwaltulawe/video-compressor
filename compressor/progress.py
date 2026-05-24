import re

def parse_progress(line):
    result = {}

    patterns = {
        "frame": r"frame=\s*(\d+)",
        "fps": r"fps=\s*([\d\.]+)",
        "bitrate": r"bitrate=\s*([\d\.kmgbits\/s]+)",
        "speed": r"speed=\s*([\d\.x]+)"
    }

    for key, pattern in patterns.items():
        match = re.search(pattern, line)
        if match:
            result[key] = match.group(1)

    return result