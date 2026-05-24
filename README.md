# Video Compressor

A small Python GUI to compress videos using FFmpeg.

## Requirements

- Python 3.8+
- Install dependencies:

```
pip install -r requirements.txt
```

## Usage for non-developers

Download and Run the GUI file : https://www.mediafire.com/file/msee89pi8q02l2p/gui.exe/file


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
a gui file will be generated in dist/

## Project Layout

- `compressor/` - core encoding modules
- `assets/` - bundled ffmpeg and resources
- `output/` - generated output files

## Note
This is just an another vide coded app. The libraries installed looked verified but do not blind trust!

It worked on my pc! 