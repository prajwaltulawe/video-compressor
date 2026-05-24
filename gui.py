import sys
import os

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QFileDialog,
    QListWidget,
    QVBoxLayout,
    QHBoxLayout,
    QComboBox,
    QLineEdit,
    QProgressBar,
    QMessageBox,
    QCheckBox,
    QSpinBox
)

from PySide6.QtCore import Qt, QThread, Signal
from compressor.encoder import VideoEncoder
from compressor.preset_profiles import PRESET_PROFILES
from compressor.utils import ensure_dir


class EncodeWorker(QThread):

    progress = Signal(int)
    finished = Signal(str)
    error = Signal(str)

    def __init__(self, config):
        super().__init__()
        self.config = config

    def apply_dark_theme(app):

        app.setStyleSheet("""

        QWidget {
            background-color: #1e1e1e;
            color: #ffffff;
            font-size: 12px;
        }

        QPushButton {
            background-color: #2d2d2d;
            border: 1px solid #444;
            padding: 8px;
            border-radius: 6px;
        }

        QPushButton:hover {
            background-color: #3c3c3c;
        }

        QLineEdit, QListWidget,
        QComboBox, QSpinBox {

            background-color: #2b2b2b;
            border: 1px solid #555;
            padding: 6px;
            border-radius: 4px;
        }

        QProgressBar {
            border: 1px solid #555;
            border-radius: 5px;
            text-align: center;
            background: #2b2b2b;
        }

        QProgressBar::chunk {
            background-color: #00aa88;
            border-radius: 5px;
        }

        QLabel {
            font-weight: bold;
        }

        """)

    def run(self):

        try:

            encoder = VideoEncoder(**self.config)

            output = encoder.encode(
                progress_callback=self.progress.emit
            )

            self.finished.emit(output)

        except Exception as e:
            self.error.emit(str(e))


class VideoCompressorGUI(QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle(
            "Video Compressor"
        )

        self.resize(700, 500)

        self.files = []

        self.init_ui()

    def apply_preset(self, preset_name):

        from compressor.preset_profiles import PRESET_PROFILES

        preset = PRESET_PROFILES.get(
            preset_name,
            {}
        )

        if not preset:
            return

        codec = preset.get("codec")
        container = preset.get("container")
        resolution = preset.get("resolution")
        bitrate = preset.get("bitrate")
        fps = preset.get("fps")

        # Apply codec
        if codec:
            index = self.codec_combo.findText(codec)

            if index >= 0:
                self.codec_combo.setCurrentIndex(index)

        # Apply container
        if container:
            index = self.container_combo.findText(container)

            if index >= 0:
                self.container_combo.setCurrentIndex(index)

        # Apply resolution
        self.resolution_input.setText(
            resolution if resolution else ""
        )

        # Apply bitrate
        self.bitrate_input.setText(
            bitrate if bitrate else ""
        )

        # Apply FPS
        self.fps_spin.setValue(
            fps if fps else 0
        )

    def init_ui(self):

        layout = QVBoxLayout()

        # File list
        self.file_list = QListWidget()

        layout.addWidget(
            QLabel("Video Files")
        )

        layout.addWidget(self.file_list)

        # Buttons
        btn_layout = QHBoxLayout()

        self.add_btn = QPushButton(
            "Add Files"
        )

        self.add_btn.clicked.connect(
            self.add_files
        )

        self.clear_btn = QPushButton(
            "Clear"
        )

        self.clear_btn.clicked.connect(
            self.file_list.clear
        )

        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.clear_btn)

        layout.addLayout(btn_layout)

        # Preset profiles
        layout.addWidget(
            QLabel("Preset Profiles")
        )

        self.preset_combo = QComboBox()

        self.preset_combo.addItems(
            PRESET_PROFILES.keys()
        )

        self.preset_combo.currentTextChanged.connect(
            self.update_container_options
        )
        
        layout.addWidget(
            self.preset_combo
        )

        # Compression quality
        layout.addWidget(
            QLabel("Compression Quality")
        )

        self.quality_combo = QComboBox()

        self.quality_combo.addItems([
            "fast",
            "balanced",
            "high"
        ])

        layout.addWidget(
            self.quality_combo
        )

        # Codec
        self.codec_combo = QComboBox()

        self.codec_combo.addItems([

            # Modern codecs
            "h264",
            "hevc",
            "vp9",
            "av1",

            # Legacy codecs
            "mpeg4",
            "xvid",

            # Editing codecs
            "prores",
            "dnxhd",
            "cineform",

            # Lossless codecs
            "ffv1",
            "huffyuv",

            # Other codecs
            "mjpeg",
            "theora"
        ])

        self.codec_combo.setToolTip(
            """
            h264    = Best compatibility
            hevc    = Better compression
            vp9     = Web streaming
            av1     = Best modern compression

            prores  = Video editing
            dnxhd   = Professional editing
            cineform= Intermediate editing

            ffv1    = Archival lossless
            huffyuv = Lossless

            xvid    = Legacy AVI codec
            mpeg4   = Older devices
            mjpeg   = Motion JPEG
            theora  = Open-source legacy codec
            """
        )
        
        layout.addWidget(
            QLabel("Codec")
        )

        layout.addWidget(
            self.codec_combo
        )
        
        # Container
        self.container_combo = QComboBox()

        self.container_combo.addItems([
            "mp4",
            "mkv",
            "avi",
            "mov",
            "webm"
        ])

        layout.addWidget(
            QLabel("Container")
        )

        layout.addWidget(
            self.container_combo
        )

        self.update_container_options()

        # Resolution
        self.resolution_input = QLineEdit()

        self.resolution_input.setPlaceholderText(
            "1280:720"
        )

        layout.addWidget(
            QLabel("Resolution")
        )

        layout.addWidget(
            self.resolution_input
        )

        # Bitrate
        self.bitrate_input = QLineEdit()

        self.bitrate_input.setPlaceholderText(
            "4M"
        )

        layout.addWidget(
            QLabel("Bitrate")
        )

        layout.addWidget(
            self.bitrate_input
        )

        # FPS
        self.fps_spin = QSpinBox()

        self.fps_spin.setRange(0, 240)

        layout.addWidget(
            QLabel("FPS (0 = original)")
        )

        layout.addWidget(
            self.fps_spin
        )

        # Audio Codec
        layout.addWidget(
            QLabel("Audio Codec")
        )

        self.audio_combo = QComboBox()

        self.audio_combo.addItems([
            "aac",
            "mp3",
            "opus",
            "vorbis",
            "flac",
            "copy"
        ])

        layout.addWidget(
            self.audio_combo
        )

        # Hardware acceleration
        self.hw_checkbox = QCheckBox(
            "Enable Hardware Acceleration"
        )

        self.hw_checkbox.setChecked(True)

        layout.addWidget(
            self.hw_checkbox
        )

        # Output directory
        output_layout = QHBoxLayout()

        self.output_input = QLineEdit()

        self.output_input.setText(
            os.path.abspath("output")
        )

        self.output_btn = QPushButton(
            "Browse"
        )

        self.output_btn.clicked.connect(
            self.select_output_dir
        )

        output_layout.addWidget(
            self.output_input
        )

        output_layout.addWidget(
            self.output_btn
        )

        layout.addWidget(
            QLabel("Output Directory")
        )

        layout.addLayout(output_layout)

        # Progress
        self.progress_bar = QProgressBar()

        layout.addWidget(
            self.progress_bar
        )

        # Start button
        self.start_btn = QPushButton(
            "Start Compression"
        )

        self.start_btn.clicked.connect(
            self.start_compression
        )

        layout.addWidget(
            self.start_btn
        )

        self.setLayout(layout)

    def add_files(self):

        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Select Videos"
        )

        for file in files:

            self.files.append(file)

            self.file_list.addItem(file)

    def select_output_dir(self):

        directory = QFileDialog.getExistingDirectory(
            self,
            "Select Output Directory"
        )

        if directory:
            self.output_input.setText(directory)

    def update_container_options(self):

        codec = self.codec_combo.currentText()

        self.container_combo.clear()

        if codec in ["vp9", "av1"]:
            self.container_combo.addItems([
                "webm",
                "mkv",
                "mp4"
            ])

        elif codec in [
            "prores",
            "dnxhd",
            "cineform"
        ]:
            self.container_combo.addItems([
                "mov",
                "mkv"
            ])

        elif codec in [
            "ffv1",
            "huffyuv"
        ]:
            self.container_combo.addItems([
                "mkv",
                "avi"
            ])

        else:
            self.container_combo.addItems([
                "mp4",
                "mkv",
                "avi",
                "mov",
                "webm"
            ])

    def start_compression(self):

        if not self.files:

            QMessageBox.warning(
                self,
                "Error",
                "Please add video files."
            )

            return

        ensure_dir(
            self.output_input.text()
        )

        self.current_index = 0

        self.process_next()

    def process_next(self):

        if self.current_index >= len(self.files):

            QMessageBox.information(
                self,
                "Done",
                "All files processed."
            )

            return

        file = self.files[
            self.current_index
        ]

        config = {
            "input_file": file,
            "output_dir": self.output_input.text(),
            "codec": self.codec_combo.currentText(),
            "container": self.container_combo.currentText(),
            "resolution": self.resolution_input.text() or None,
            "bitrate": self.bitrate_input.text() or None,
            "fps": self.fps_spin.value() or None,
            "audio_codec": self.audio_combo.currentText(),
            "preset": self.quality_combo.currentText(),
            "hw_accel": self.hw_checkbox.isChecked()
        }

        self.worker = EncodeWorker(config)

        self.worker.progress.connect(
            self.progress_bar.setValue
        )

        self.worker.finished.connect(
            self.file_finished
        )

        self.worker.error.connect(
            self.file_error
        )

        self.worker.start()

    def file_finished(self, output):

        self.current_index += 1

        self.process_next()

    def file_error(self, error):

        QMessageBox.critical(
            self,
            "Error",
            error
        )

        self.current_index += 1

        self.process_next()


if __name__ == "__main__":

    app = QApplication(sys.argv)

    EncodeWorker.apply_dark_theme(app)

    window = VideoCompressorGUI()

    window.show()

    sys.exit(app.exec())