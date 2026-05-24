import os

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def build_output_name(input_file, codec, ext):
    name = os.path.splitext(os.path.basename(input_file))[0]
    return f"{name}_{codec}.{ext}"