import subprocess
import os
import sys

from compressor.hardware import detect_gpu
from compressor.formats import CODECS
from compressor.presets import PRESETS
from compressor.utils import build_output_name

class VideoEncoder:

    def __init__(
        self,
        input_file,
        output_dir,
        codec="h264",
        container="mp4",
        resolution=None,
        bitrate=None,
        fps=None,
        audio_codec="aac",
        preset="balanced",
        hw_accel=True,
        preserve_metadata=True,
        preserve_subtitles=True
    ):

        self.input_file = input_file
        self.output_dir = output_dir
        self.codec = codec
        self.container = container
        self.resolution = resolution
        self.bitrate = bitrate
        self.fps = fps
        self.audio_codec = audio_codec
        self.preset = preset

        self.hw_accel = hw_accel
        self.preserve_metadata = preserve_metadata
        self.preserve_subtitles = preserve_subtitles

    def resource_path(relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)
    
    FFMPEG_PATH = resource_path(
       "assets/ffmpeg/ffmpeg.exe"
    )

    def get_encoder(self):

        if not self.hw_accel:
            return CODECS[self.codec]["cpu"]

        gpu = detect_gpu()

        return CODECS[self.codec].get(
            gpu,
            CODECS[self.codec]["cpu"]
        )

    def build_command(self):

        encoder = self.get_encoder()

        preset_data = PRESETS[self.preset]

        output_file = os.path.join(
            self.output_dir,
            build_output_name(
                self.input_file,
                self.codec,
                self.container
            )
        )

        cmd = [
            self.FFMPEG_PATH,
            "-y",
            "-i",
            self.input_file
        ]

        if self.preserve_metadata:
            cmd += ["-map_metadata", "0"]

        if self.preserve_subtitles:
            cmd += ["-map", "0:s?"]

        if self.resolution:
            cmd += [
                "-vf",
                f"scale={self.resolution}"
            ]

        if self.fps:
            cmd += ["-r", str(self.fps)]

        cmd += [
            "-c:v",
            encoder
        ]

        # CPU codecs
        if "libx" in encoder or "svt" in encoder:
            cmd += [
                "-preset",
                preset_data["preset"],
                "-crf",
                str(preset_data["crf"])
            ]

        # GPU codecs
        elif "nvenc" in encoder:
            cmd += [
                "-preset",
                "p5"
            ]

        if self.bitrate:
            cmd += [
                "-b:v",
                self.bitrate
            ]

        cmd += [
            "-c:a",
            self.audio_codec,
            output_file
        ]

        return cmd, output_file

    def encode(self, progress_callback=None):

        cmd, output_file = self.build_command()

        process = subprocess.Popen(
            cmd,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )

        duration = None

        while True:

            line = process.stderr.readline()

            if not line:
                break

            if "Duration" in line:

                import re

                match = re.search(
                    r"Duration: (\d+):(\d+):(\d+\.\d+)",
                    line
                )

                if match:

                    h, m, s = match.groups()

                    duration = (
                        int(h) * 3600 +
                        int(m) * 60 +
                        float(s)
                    )

            if "time=" in line and duration:

                import re

                match = re.search(
                    r"time=(\d+):(\d+):(\d+\.\d+)",
                    line
                )

                if match:

                    h, m, s = match.groups()

                    current = (
                        int(h) * 3600 +
                        int(m) * 60 +
                        float(s)
                    )

                    percent = int(
                        (current / duration) * 100
                    )

                    if progress_callback:
                        progress_callback(percent)

        process.wait()

        if process.returncode != 0:
            raise Exception("Encoding failed")

        return output_file