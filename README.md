# Video Compressor

A small Python GUI to compress videos using FFmpeg.

## Requirements

- Python 3.8+
- Install dependencies:

```
pip install -r requirements.txt
```

## Usage for non-developers

Run the GUI: dist\gui.exe


## Usage for developers

Customize application as per your need

Run :
```
python gui.py
```
for local running.

Build a one-file executable:

```
pyinstaller --onefile --windowed --add-data "assets;assets" gui.py
```

## Project Layout

- `compressor/` - core encoding modules
- `assets/` - bundled ffmpeg and resources
- `output/` - generated output files

# Video Compressor
This is just an another vide coded app. The libraries installed looked verified but do not blind trust!
It worked on my pc, 