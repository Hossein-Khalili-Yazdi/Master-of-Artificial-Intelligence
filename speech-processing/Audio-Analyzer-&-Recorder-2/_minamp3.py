import os
import sys
import matplotlib.pyplot as plt
import numpy as np
import sounddevice as sd
import soundfile as sf
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtCore import QElapsedTimer, Qt, QTimer
from PyQt5.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDialog,
    QDoubleSpinBox,
    QFileDialog,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)
from scipy import signal
from scipy.signal import find_peaks

# ~~~##~~~##~~~##~~~##~~~##~~~##~~~##~~~##~~~##~~~##~~~##~~~#
# ~/|\~##~/|\~##~/|\~##~/|\~##~/|\~##~/|\~##~/|\~##~/|\~##~/|\~#

class AudioApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("نرم افزار تحلیل و ضبط صوت")
        self.setGeometry(
            100, 100, 1400, 800
        )  # کمی ارتفاع بیشتر برای جا شدن کنترل‌های جدید

        # ~/|\~##~/|\~##~/|\~##~/|\~##~/|\~##~/|\~##~/|\~##~/|\~##~/|\~#
        # متغیرهای سراسری سیگنال
        self.audio_data = np.array([])
        self.fs = 16000
        self.bit_depth = 16
        self.is_recording = False
        self.stream = None
        self.recorded_chunks = []

        self.is_playing = False
        self.playback_pos = 0
        self.playback_elapsed_timer = QElapsedTimer()

        self.playback_timer = QTimer(self)
        self.playback_timer.setSingleShot(True)
        self.playback_timer.timeout.connect(self.stop_all)

        self.current_theme_index = 0
        self.themes = [
            {
                "name": "Light Glass",
                "qss": """
                    QMainWindow, QDialog { background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #e0c3fc, stop:1 #8ec5fc); }
                    QWidget#CentralWidget { background: transparent; }
                    QPushButton, QComboBox, QSpinBox, QDoubleSpinBox, QLineEdit { background-color: rgba(255, 255, 255, 0.4); border: 1px solid rgba(255, 255, 255, 0.6); border-radius: 4px; color: #333; padding: 5px; }
                    QPushButton:hover { background-color: rgba(255, 255, 255, 0.6); }
                    QPushButton:disabled, QComboBox:disabled { background-color: rgba(255, 255, 255, 0.15); border: 1px solid rgba(255, 255, 255, 0.2); color: rgba(51, 51, 51, 0.4); }
                    QPushButton:pressed { background-color: rgba(0, 0, 0, 0.08); border: 1px solid rgba(0, 0, 0, 0.15); color: rgba(51, 51, 51, 0.8); }
                    QGroupBox { background-color: rgba(255, 255, 255, 0.2); border: 1px solid rgba(255, 255, 255, 0.5); border-radius: 10px; margin-top: 2ex; color: #333; }
                    QGroupBox::title { subcontrol-origin: margin; left: 10px; color: #0052D4; }
                    QLabel, QCheckBox { color: #333; font-weight: bold; }
                """,
                "mpl_text": "black",
                "mpl_face": (0.0, 0.0, 0.0, 0.05),
                "mpl_edge": (0.0, 0.0, 0.0, 0.3),
            },
            {
                "name": "Dark Glass",
                "qss": """
                    QMainWindow, QDialog { background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #0f2027, stop:0.5 #203a43, stop:1 #2c5364); }
                    QWidget#CentralWidget { background: transparent; }
                    QPushButton, QComboBox, QSpinBox, QDoubleSpinBox, QLineEdit { background-color: rgba(255, 255, 255, 0.15); border: 1px solid rgba(255, 255, 255, 0.3); border-radius: 4px; color: white; padding: 5px; }
                    QPushButton:hover { background-color: rgba(255, 255, 255, 0.25); }
                    QPushButton:disabled { background-color: rgba(200, 200, 200, 0.05); color: rgba(255, 255, 255, 0.3); border: 1px solid rgba(255, 255, 255, 0.1); }
                    QPushButton:pressed { background-color: rgba(0, 0, 0, 0.3); border: 1px solid rgba(255, 255, 255, 0.1); color: rgba(255, 255, 255, 0.7); }
                    QGroupBox { background-color: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.2); border-radius: 10px; margin-top: 2ex; color: white; }
                    QGroupBox::title { subcontrol-origin: margin; left: 10px; color: #4facfe; }
                    QLabel, QCheckBox { color: white; font-weight: bold; }
                """,
                "mpl_text": "black",
                "mpl_face": (0.0, 0.0, 0.0, 0.05),
                "mpl_edge": (0.0, 0.0, 0.0, 0.3),
            },
        ]

        self.init_ui()

    # ~~~##~~~##~~~##~~~##~~~##~~~##~~~##~~~##~~~##~~~##~~~##~~~#

    def init_ui(self):
        main_widget = QWidget()
        main_widget.setObjectName("CentralWidget")
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)

        # ~/|\~##~/|\~##~/|\~##~/|\~##~/|\~##~/|\~##~/|\~##~/|\~##~/|\~#
        # پنل سمت چپ (نمودارها)
        plot_layout = QVBoxLayout()
        self.figure, (self.ax_wave, self.ax_spec) = plt.subplots(
            2, 1, figsize=(6, 6), gridspec_kw={"height_ratios": [1, 2]}
        )
        self.figure.patch.set_facecolor("None")
        self.figure.patch.set_alpha(0.5)
        self.canvas = FigureCanvas(self.figure)
        plot_layout.addWidget(self.canvas)
        main_layout.addLayout(plot_layout, stretch=3)

        # ~/|\~##~/|\~##~/|\~##~/|\~##~/|\~##~/|\~##~/|\~##~/|\~##~/|\~#
        # پنل سمت راست (کنترل ها)
        control_layout = QVBoxLayout()

        # ~/|\~##~/|\~##~/|\~##~/|\~##~/|\~##~/|\~##~/|\~##~/|\~##~/|\~#
        # دکمه های اصلی (بالا)
        btn_layout = QHBoxLayout()
        self.btn_record = QPushButton("🔴 Record")
        self.btn_pause_rec = QPushButton("⏸ Pause Record")
        self.btn_stop = QPushButton("⏹ Stop")
        self.btn_play = QPushButton("▶ Play")

        self.btn_record.clicked.connect(self.start_record)
        self.btn_pause_rec.clicked.connect(self.pause_record)
        self.btn_stop.clicked.connect(self.stop_all)
        self.btn_play.clicked.connect(self.toggle_play_pause)

        btn_layout.addWidget(self.btn_record)
        btn_layout.addWidget(self.btn_pause_rec)
        btn_layout.addWidget(self.btn_stop)
        btn_layout.addWidget(self.btn_play)
        control_layout.addLayout(btn_layout)

        # ~/|\~##~/|\~##~/|\~##~/|\~##~/|\~##~/|\~##~/|\~##~/|\~##~/|\~#
        # فایل (New, Open, Save)
        file_group = QGroupBox("مدیریت فایل (File)")
        file_layout = QHBoxLayout()
        self.btn_new = QPushButton("New")
        self.btn_open = QPushButton("Open")
        self.btn_save = QPushButton("Save As")
        self.btn_new.clicked.connect(self.new_file)
        self.btn_open.clicked.connect(self.open_file)
        self.btn_save.clicked.connect(self.save_file)

        self.btn_new.setEnabled(False)
        self.btn_pause_rec.setEnabled(False)
        self.btn_stop.setEnabled(False)
        self.btn_play.setEnabled(False)
        self.btn_save.setEnabled(False)

        file_layout.addWidget(self.btn_new)
        file_layout.addWidget(self.btn_open)
        file_layout.addWidget(self.btn_save)
        file_group.setLayout(file_layout)
        control_layout.addWidget(file_group)

        # ~/|\~##~/|\~##~/|\~##~/|\~##~/|\~##~/|\~##~/|\~##~/|\~##~/|\~#
        # اطلاعات و تنظیمات سیگنال
        info_group = QGroupBox("مشخصات سیگنال (Recording Specs)")
        info_layout = QVBoxLayout()

        self.lbl_filename = QLabel("File: Unsaved / None")
        info_layout.addWidget(self.lbl_filename)

        self.lbl_duration = QLabel("Duration: 0.000 seconds")
        info_layout.addWidget(self.lbl_duration)

        fs_layout = QHBoxLayout()
        fs_layout.addWidget(QLabel("Sampling Freq (Hz):"))
        self.cb_fs = QComboBox()
        self.cb_fs.addItems(["8000", "11025", "12000", "16000", "22050"])
        self.cb_fs.setCurrentText("16000")
        fs_layout.addWidget(self.cb_fs)
        info_layout.addLayout(fs_layout)

        bits_layout = QHBoxLayout()
        bits_layout.addWidget(QLabel("Bits per sample:"))
        self.cb_bits = QComboBox()
        self.cb_bits.addItems(["8", "16"])
        self.cb_bits.setCurrentText("16")
        bits_layout.addWidget(self.cb_bits)
        info_layout.addLayout(bits_layout)
        info_group.setLayout(info_layout)
        control_layout.addWidget(info_group)

        # ~/|\~##~/|\~##~/|\~##~/|\~##~/|\~##~/|\~##~/|\~##~/|\~##~/|\~#
        # تنظیمات Spectrogram
        spec_group = QGroupBox("تنظیمات اسپکتوگرام (Spectrogram Settings)")
        spec_layout = QVBoxLayout()

        frame_len_layout = QHBoxLayout()
        frame_len_layout.addWidget(QLabel("Frame Length (ms):"))
        self.spin_frame_len = QSpinBox()
        self.spin_frame_len.setRange(1, 100)
        self.spin_frame_len.setValue(25)
        frame_len_layout.addWidget(self.spin_frame_len)
        spec_layout.addLayout(frame_len_layout)

        frame_shift_layout = QHBoxLayout()
        frame_shift_layout.addWidget(QLabel("Frame Shift (ms):"))
        self.spin_frame_shift = QSpinBox()
        self.spin_frame_shift.setRange(1, 100)
        self.spin_frame_shift.setValue(10)
        frame_shift_layout.addWidget(self.spin_frame_shift)
        spec_layout.addLayout(frame_shift_layout)

        freq_limit_layout = QHBoxLayout()
        freq_limit_layout.addWidget(QLabel("Max Freq Display (Hz):"))
        self.spin_max_freq = QSpinBox()
        self.spin_max_freq.setRange(100, 11025)
        self.spin_max_freq.setValue(8000)
        self.spin_max_freq.setSingleStep(500)
        self.spin_max_freq.valueChanged.connect(self.update_spec_ylim)
        freq_limit_layout.addWidget(self.spin_max_freq)
        spec_layout.addLayout(freq_limit_layout)

        self.btn_update_spec = QPushButton("بروزرسانی Spectrogram")
        self.btn_update_spec.clicked.connect(self.update_plots)
        spec_layout.addWidget(self.btn_update_spec)
        spec_group.setLayout(spec_layout)

        frame_wideband_mode = QHBoxLayout()
        self.btn_wideband = QPushButton("Wideband (باند پهن)")
        self.btn_narrowband = QPushButton("Narrowband (باند باریک)")
        self.btn_wideband.clicked.connect(self.set_wideband_values)
        self.btn_narrowband.clicked.connect(self.set_narrowband_values)
        frame_wideband_mode.addWidget(self.btn_wideband)
        frame_wideband_mode.addWidget(self.btn_narrowband)
        spec_layout.addLayout(frame_wideband_mode)

        control_layout.addWidget(spec_group)

        # ~/|\~##~/|\~##~/|\~##~/|\~##~/|\~##~/|\~##~/|\~##~/|\~##~/|\~#
        # بزرگنمایی (Zoom)
        zoom_group = QGroupBox("بزرگنمایی زمانی (Zoom)")
        zoom_layout = QHBoxLayout()
        zoom_layout.addWidget(QLabel("From (s):"))
        self.spin_zoom_from = QDoubleSpinBox()
        self.spin_zoom_from.setDecimals(3)
        zoom_layout.addWidget(self.spin_zoom_from)

        zoom_layout.addWidget(QLabel("To (s):"))
        self.spin_zoom_to = QDoubleSpinBox()
        self.spin_zoom_to.setDecimals(3)
        self.spin_zoom_to.setValue(1.0)
        zoom_layout.addWidget(self.spin_zoom_to)

        self.btn_zoom = QPushButton("Zoom")
        self.btn_reset_zoom = QPushButton("Reset")
        self.btn_zoom.clicked.connect(self.apply_zoom)
        self.btn_reset_zoom.clicked.connect(self.reset_zoom)
        zoom_layout.addWidget(self.btn_zoom)
        zoom_layout.addWidget(self.btn_reset_zoom)
        zoom_group.setLayout(zoom_layout)
        control_layout.addWidget(zoom_group)

        # ~/|\~##~/|\~##~/|\~##~/|\~##~/|\~##~/|\~##~/|\~##~/|\~##~/|\~#
        # انتخاب تم
        theme_group = QGroupBox("ظاهر (theme)")
        theme_layout = QHBoxLayout()
        self.theme_combo = QComboBox()
        for theme in self.themes:
            self.theme_combo.addItem(theme["name"])
        self.theme_combo.currentIndexChanged.connect(self.change_theme)
        theme_layout.addWidget(self.theme_combo)
        theme_group.setLayout(theme_layout)
        control_layout.addWidget(theme_group)
        self.apply_theme()

        # ~/|\~##~/|\~##~/|\~##~/|\~##~/|\~##~/|\~##~/|\~##~/|\~##~/|\~#
        # تنظیمات تحلیل فریم (Assignment 3 & 4)
        frame_group = QGroupBox("تحلیل فریم و ویژگی‌ها (Frame & Features)")
        frame_layout = QVBoxLayout()

        # پارامترهای N و M
        nm_layout = QHBoxLayout()
        nm_layout.addWidget(QLabel("N:"))
        self.spin_N = QSpinBox()
        self.spin_N.setRange(1, 10000)
        self.spin_N.setValue(360)
        nm_layout.addWidget(self.spin_N)

        nm_layout.addWidget(QLabel("M:"))
        self.spin_M = QSpinBox()
        self.spin_M.setRange(1, 10000)
        self.spin_M.setValue(120)
        nm_layout.addWidget(self.spin_M)
        frame_layout.addLayout(nm_layout)

        self.spin_N.valueChanged.connect(self.update_max_frame)
        self.spin_M.valueChanged.connect(self.update_max_frame)

        # پارامتر شماره فریم
        fno_layout = QHBoxLayout()
        fno_layout.addWidget(QLabel("Frame No:"))
        self.spin_fno = QSpinBox()
        self.spin_fno.setRange(0, 0)
        self.spin_fno.setValue(0)
        fno_layout.addWidget(self.spin_fno)

        self.lbl_max_frame = QLabel("Max: 0")
        self.lbl_max_frame.setStyleSheet("color: gray;")
        fno_layout.addWidget(self.lbl_max_frame)

        frame_layout.addLayout(fno_layout)
        # self.spin_fno.valueChanged.connect(self.update_wave_marker)

        self.btn_show_frame = QPushButton("نمایش فریم روی نمودار")
        self.btn_show_frame.clicked.connect(
            lambda: self.update_wave_marker(self.spin_fno.value())
        )

        frame_layout.addWidget(self.btn_show_frame)
        # دکمه رسم تکالیف قبلی
        self.btn_analyze_frame = QPushButton("تحلیل فریم و طیف")
        self.btn_analyze_frame.clicked.connect(self.show_frame_analysis)
        frame_layout.addWidget(self.btn_analyze_frame)

        # محاسبه شماره فریم از روی زمان
        time_calc_layout = QHBoxLayout()
        time_calc_layout.addWidget(QLabel("زمان (s)"))
        self.spin_target_time = QDoubleSpinBox()
        self.spin_target_time.setDecimals(3)
        self.spin_target_time.setRange(0, 0)
        time_calc_layout.addWidget(self.spin_target_time)

        self.btn_calc_frame = QPushButton("محاسبه فریم")
        self.btn_calc_frame.clicked.connect(self.calculate_frame_from_time)
        time_calc_layout.addWidget(self.btn_calc_frame)

        self.lbl_calc_result = QLabel("فریم: -")
        self.lbl_calc_result.setStyleSheet("color: #0052D4; font-weight: bold;")
        time_calc_layout.addWidget(self.lbl_calc_result)
        frame_layout.addLayout(time_calc_layout)

        # دکمه‌های مربوط به ویژگی‌های تکلیف 4
        features_layout = QVBoxLayout()

        btn_ezcr = QPushButton("(الف و ب) مقادیر ZCR و Energy")
        btn_ezcr.clicked.connect(self.show_energy_zcr)
        features_layout.addWidget(btn_ezcr)

        btn_corr = QPushButton("(ج) دنباله ضرائب اتوکورولیشن")
        btn_corr.clicked.connect(self.show_autocorr)
        features_layout.addWidget(btn_corr)

        btn_amdf = QPushButton("(د) دنباله ضرائب AMDF")
        btn_amdf.clicked.connect(self.show_amdf)
        features_layout.addWidget(btn_amdf)

        btn_formant = QPushButton("(ه) فرمنت‌های یک فریم")
        btn_formant.clicked.connect(self.show_formants)
        features_layout.addWidget(btn_formant)

        btn_cepstral = QPushButton("(و) ضرایب کپسترال")
        btn_cepstral.clicked.connect(self.show_cepstral)
        features_layout.addWidget(btn_cepstral)

        btn_compare_ez = QPushButton("(ز) مقایسه واکدار/ بی‌واک")
        btn_compare_ez.clicked.connect(self.compare_voiced_unvoiced)
        features_layout.addWidget(btn_compare_ez)

        btn_compare_pitch = QPushButton("(ح) فرکانس گام 200 فریم")
        btn_compare_pitch.clicked.connect(self.compare_pitch_200)
        features_layout.addWidget(btn_compare_pitch)

        frame_layout.addLayout(features_layout)
        frame_group.setLayout(frame_layout)
        control_layout.addWidget(frame_group)

        control_layout.addStretch()
        main_layout.addLayout(control_layout, stretch=1)

        self.reset_plots()

    # ~/|\~##~/|\~##~/|\~##~/|\~##~/|\~##~/|\~##~/|\~##~/|\~##~/|\~#
    # ~~~##~~~##~~~##~~~##~~~##~~~##~~~##~~~##~~~##~~~##~~~##~~~#
    # --- توابع ضبط و پخش ---
    def audio_callback(self, indata, frames, time, status):
        if self.is_recording:
            self.recorded_chunks.append(indata.copy())

    def start_record(self):
        self.fs = int(self.cb_fs.currentText())
        self.bit_depth = int(self.cb_bits.currentText())
        if self.stream is None:
            self.recorded_chunks = []
            self.stream = sd.InputStream(
                samplerate=self.fs, channels=1, callback=self.audio_callback
            )
            self.stream.start()
        self.is_recording = True

        self.btn_record.setEnabled(False)
        self.btn_play.setEnabled(False)
        self.btn_pause_rec.setEnabled(True)
        self.btn_stop.setEnabled(True)
        self.btn_open.setEnabled(False)
        self.btn_new.setEnabled(False)
        self.btn_save.setEnabled(False)

    def pause_record(self):
        self.is_recording = False
        self.btn_record.setEnabled(True)
        self.btn_pause_rec.setEnabled(False)

    def toggle_play_pause(self):
        if self.audio_data is None or len(self.audio_data) == 0:
            return

        if not self.is_playing:
            data_to_play = self.audio_data[self.playback_pos :]
            if len(data_to_play) == 0:
                self.playback_pos = 0
                data_to_play = self.audio_data

            sd.play(data_to_play, self.fs)
            duration_ms = int((len(data_to_play) / self.fs) * 1000)
            self.playback_timer.start(duration_ms)
            self.playback_elapsed_timer.start()

            self.is_playing = True
            self.btn_play.setText("⏸ Pause")

            self.btn_record.setEnabled(False)
            self.btn_new.setEnabled(False)
            self.btn_open.setEnabled(False)
            self.btn_save.setEnabled(False)
            self.btn_stop.setEnabled(True)
        else:
            sd.stop()
            self.playback_timer.stop()

            elapsed_ms = self.playback_elapsed_timer.elapsed()
            frames_played = int((elapsed_ms / 1000.0) * self.fs)
            self.playback_pos += frames_played

            if self.playback_pos >= len(self.audio_data):
                self.playback_pos = 0

            self.is_playing = False
            self.btn_play.setText("▶ Play")

    def stop_all(self):
        self.is_recording = False
        if self.stream is not None:
            self.stream.stop()
            self.stream.close()
            self.stream = None
            if self.recorded_chunks:
                self.audio_data = np.concatenate(self.recorded_chunks, axis=0).flatten()
                self.update_info()
                self.update_plots()

        sd.stop()
        if hasattr(self, "playback_timer") and self.playback_timer.isActive():
            self.playback_timer.stop()

        self.is_playing = False
        self.playback_pos = 0
        self.btn_play.setText("▶ Play")

        self.btn_pause_rec.setEnabled(False)
        self.btn_stop.setEnabled(False)
        self.btn_open.setEnabled(True)
        self.btn_new.setEnabled(True)

        if len(self.audio_data) > 0:
            self.btn_play.setEnabled(True)
            self.btn_record.setEnabled(False)
            self.btn_save.setEnabled(True)
        else:
            self.btn_record.setEnabled(True)
            self.btn_save.setEnabled(False)

    # ~~~##~~~##~~~##~~~##~~~##~~~##~~~##~~~##~~~##~~~##~~~##~~~#
    # --- توابع فایل ---
    def new_file(self):
        self.audio_data = np.array([])
        self.recorded_chunks = []
        self.update_info()
        self.reset_plots()
        self.lbl_filename.setText("File: Unsaved / None")
        self.btn_record.setEnabled(True)
        self.btn_open.setEnabled(True)
        self.btn_new.setEnabled(False)
        self.btn_play.setEnabled(False)
        self.btn_pause_rec.setEnabled(False)
        self.btn_stop.setEnabled(False)
        self.btn_save.setEnabled(False)
        if hasattr(self, "frame_region"):
            self.frame_region = None
        if hasattr(self, "_bg"):
            delattr(self, "_bg")

    def open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "باز کردن فایل صوتی", "", "WAV Files (*.wav)"
        )
        if file_name:
            info = sf.info(file_name)
            self.cb_fs.setCurrentText(str(info.samplerate))
            bit_depth = "8" if "8" in info.subtype else "16"
            self.cb_bits.setCurrentText(bit_depth)

            self.audio_data, self.fs = sf.read(file_name)
            if len(self.audio_data.shape) > 1:
                self.audio_data = self.audio_data[:, 0]

            self.cb_fs.setCurrentText(str(self.fs))
            self.update_info()
            self.update_plots()

            self.lbl_filename.setText(f"File: {os.path.basename(file_name)}")
            self.btn_play.setEnabled(True)
            self.btn_new.setEnabled(True)
            self.btn_record.setEnabled(False)
            self.btn_save.setEnabled(True)

            if hasattr(self, "frame_region"):
                self.frame_region = None
            if hasattr(self, "_bg"):
                delattr(self, "_bg")

    def save_file(self):
        if len(self.audio_data) == 0:
            return
        file_name, _ = QFileDialog.getSaveFileName(
            self, "ذخیره فایل صوتی", "", "WAV Files (*.wav)"
        )
        if file_name:
            subtype = "PCM_16" if self.cb_bits.currentText() == "16" else "PCM_U8"
            sf.write(file_name, self.audio_data, self.fs, subtype=subtype)
            self.lbl_filename.setText(f"File: {os.path.basename(file_name)}")

    # ~~~##~~~##~~~##~~~##~~~##~~~##~~~##~~~##~~~##~~~##~~~##~~~#
    # --- بروزرسانی UI و نمودارها ---
    def update_info(self):
        duration = len(self.audio_data) / self.fs if self.fs > 0 else 0
        self.lbl_duration.setText(f"Duration: {duration:.3f} seconds")
        self.spin_zoom_to.setValue(duration)
        self.spin_zoom_to.setRange(0, duration)
        self.spin_zoom_from.setRange(0, duration)
        self.spin_target_time.setRange(0, duration)
        self.update_max_frame()

    def update_max_frame(self):
        if hasattr(self, "audio_data") and len(self.audio_data) > 0:
            N = self.spin_N.value()
            M = self.spin_M.value()
            total_samples = len(self.audio_data)
            if total_samples >= N:
                max_frame = ((total_samples - N) // M) + 1
                if (max_frame * M) < total_samples:
                    max_frame += 1
                max_fno = max(0, max_frame - 1)
            else:
                max_fno = 0
            self.spin_fno.setMaximum(max_fno)
            self.lbl_max_frame.setText(f"Max: {max_fno}")
        else:
            self.spin_fno.setMaximum(0)
            self.lbl_max_frame.setText("Max: 0")

    def reset_plots(self):
        self.ax_wave.clear()
        self.ax_spec.clear()
        self.ax_wave.set_title("Waveform")
        self.ax_wave.set_xlabel("Time (s)")
        self.ax_wave.set_ylabel("Amplitude")
        self.ax_spec.set_title("Spectrogram")
        self.ax_spec.set_xlabel("Time (s)")
        self.ax_spec.set_ylabel("Frequency (Hz)")
        self.canvas.draw()

    def update_plots(self):
        if (
            not hasattr(self, "audio_data")
            or self.audio_data is None
            or len(self.audio_data) == 0
        ):
            QMessageBox.warning(self, "خطا", "ابتدا یک فایل صوتی باز کنید.")
            return

        nyquist_freq = int(self.fs / 2)
        self.spin_max_freq.setMaximum(nyquist_freq)
        if self.spin_max_freq.value() > nyquist_freq:
            self.spin_max_freq.setValue(nyquist_freq)

        self.ax_wave.clear()
        self.ax_spec.clear()

        time_axis = np.linspace(
            0, len(self.audio_data) / self.fs, num=len(self.audio_data)
        )
        self.ax_wave.plot(time_axis, self.audio_data, color="black", linewidth=0.5)
        self.ax_wave.set_title("Waveform")
        self.ax_wave.set_ylabel("Amplitude")
        self.ax_wave.set_xlim(0, time_axis[-1])

        frame_len_samples = int((self.spin_frame_len.value() / 1000) * self.fs)
        frame_shift_samples = int((self.spin_frame_shift.value() / 1000) * self.fs)
        noverlap = frame_len_samples - frame_shift_samples

        f, t, Sxx = signal.spectrogram(
            self.audio_data, self.fs, nperseg=frame_len_samples, noverlap=noverlap
        )
        Sxx_db = 10 * np.log10(Sxx + 1e-10)

        self.ax_spec.pcolormesh(t, f, Sxx_db, shading="gouraud", cmap="gray_r")
        self.ax_spec.set_title(
            f"Spectrogram (Frame: {self.spin_frame_len.value()}ms, Shift: {self.spin_frame_shift.value()}ms)"
        )
        self.ax_spec.set_ylabel("Frequency (Hz)")
        self.ax_spec.set_xlabel("Time (s)")
        self.ax_spec.set_xlim(0, time_axis[-1])
        self.ax_spec.set_ylim(0, self.spin_max_freq.value())

        self.figure.tight_layout()
        self.canvas.draw()

    def set_wideband_values(self):
        self.spin_frame_len.setValue(5)
        self.spin_frame_shift.setValue(2)
        self.update_plots()

    def set_narrowband_values(self):
        self.spin_frame_len.setValue(50)
        self.spin_frame_shift.setValue(10)
        self.update_plots()

    def update_spec_ylim(self):
        if len(self.audio_data) == 0:
            return
        nyquist_freq = int(self.fs / 2)
        if self.spin_max_freq.value() > nyquist_freq:
            self.spin_max_freq.setValue(nyquist_freq)
        self.ax_spec.set_ylim(0, self.spin_max_freq.value())
        self.canvas.draw()

    # ~~~##~~~##~~~##~~~##~~~##~~~##~~~##~~~##~~~##~~~##~~~##~~~#
    # --- توابع زوم ---
    def apply_zoom(self):
        if len(self.audio_data) == 0:
            return
        t_start = self.spin_zoom_from.value()
        if t_start < (t_end := self.spin_zoom_to.value()):
            self.ax_wave.set_xlim(t_start, t_end)
            self.ax_spec.set_xlim(t_start, t_end)
            self.canvas.draw()

    def reset_zoom(self):
        if len(self.audio_data) == 0:
            return
        max_t = len(self.audio_data) / self.fs
        self.spin_zoom_from.setValue(0)
        self.spin_zoom_to.setValue(max_t)
        self.apply_zoom()

    # ~~~##~~~##~~~##~~~##~~~##~~~##~~~##~~~##~~~##~~~##~~~##~~~#
    # --- توابع تم ---
    def change_theme(self, index):
        self.current_theme_index = index
        self.apply_theme()

    def apply_theme(self):
        theme = self.themes[self.current_theme_index]
        self.setStyleSheet(theme["qss"])
        self.figure.patch.set_facecolor("None")
        self.figure.patch.set_alpha(0.0)

        for ax in [self.ax_wave, self.ax_spec]:
            ax.set_facecolor(theme["mpl_face"])
            ax.tick_params(colors=theme["mpl_text"])
            ax.xaxis.label.set_color(theme["mpl_text"])
            ax.yaxis.label.set_color(theme["mpl_text"])
            ax.title.set_color(theme["mpl_text"])
            for spine in ax.spines.values():
                spine.set_edgecolor(theme["mpl_edge"])
        self.canvas.draw()

    # ~~~##~~~##~~~##~~~##~~~##~~~##~~~##~~~##~~~##~~~##~~~##~~~#
    # --- توابع تحلیل فریم (تکالیف) ---
    def extract_frame(self, frame_no, N, M):
        start_idx = frame_no * M
        end_idx = start_idx + N
        if start_idx >= len(self.audio_data):
            return None
        frame = self.audio_data[start_idx:end_idx]
        if len(frame) < N:
            frame = np.pad(frame, (0, N - len(frame)), "constant")
        return frame

    def calculate_frame_from_time(self):
        if not hasattr(self, "audio_data") or len(self.audio_data) == 0:
            QMessageBox.warning(self, "خطا", "ابتدا یک فایل صوتی باز یا ضبط کنید.")
            return
        target_time = self.spin_target_time.value()
        M = self.spin_M.value()
        frame_no = int((target_time * self.fs) / M)
        if frame_no > (max_fno := self.spin_fno.maximum()):
            frame_no = max_fno
        self.lbl_calc_result.setText(f"شماره فریم: {frame_no}")
        self.spin_fno.setValue(frame_no)

    def apply_pre_emphasis(self, frame):
        frame_float = frame.astype(np.float64)
        r0 = np.sum(frame_float**2)
        r1 = np.sum(frame_float[:-1] * frame_float[1:])
        coeff = r1 / r0 if r0 != 0 else 0
        emphasized_frame = np.zeros_like(frame_float)
        emphasized_frame[0] = frame_float[0]
        emphasized_frame[1:] = frame_float[1:] - coeff * frame_float[:-1]
        return emphasized_frame, coeff

    def apply_windowing(self, frame, window_type):
        N = len(frame)
        if window_type == "Hamming":
            win = np.hamming(N)
        elif window_type == "Hanning":
            win = np.hanning(N)
        else:
            win = np.ones(N)
        return frame * win

    def calculate_spectrum(self, frame):
        fft_data = np.fft.fft(frame)
        half_len = len(frame) // 2
        mag = np.abs(fft_data[:half_len])
        mag = np.where(mag == 0, 1e-10, mag)
        spectrum_db = 20 * np.log10(mag)
        return spectrum_db

    def show_frame_analysis(self):
        if (
            not hasattr(self, "audio_data")
            or self.audio_data is None
            or len(self.audio_data) == 0
        ):
            QMessageBox.warning(self, "خطا", "ابتدا یک فایل صوتی باز کنید.")
            return

        N = self.spin_N.value()
        M = self.spin_M.value()
        frame_no = self.spin_fno.value()
        frame = self.extract_frame(frame_no, N, M)
        if frame is None:
            return

        dialog = QDialog(self)
        dialog.setWindowTitle(f"تحلیل فریم {frame_no}")
        dialog.resize(800, 600)
        layout = QVBoxLayout()
        controls_layout = QHBoxLayout()

        cb_window_dialog = QComboBox()
        cb_window_dialog.addItems(["Rectangular", "Hamming", "Hanning"])
        controls_layout.addWidget(QLabel("Window Type:"))
        controls_layout.addWidget(cb_window_dialog)

        chk_pre_emphasis = QCheckBox("Pre-emphasis")
        controls_layout.addWidget(chk_pre_emphasis)

        lbl_coeff = QLabel("Coeff (α): اعمال نشده")
        lbl_coeff.setStyleSheet("color: red; font-weight: bold;")
        controls_layout.addWidget(lbl_coeff)
        controls_layout.addStretch()

        layout.addLayout(controls_layout)
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))
        canvas = FigureCanvas(fig)
        layout.addWidget(canvas)
        dialog.setLayout(layout)

        def update_plot():
            ax1.clear()
            ax2.clear()
            current_frame = frame.copy()
            window_type = cb_window_dialog.currentText()
            alpha = 0
            if chk_pre_emphasis.isChecked():
                current_frame, alpha = self.apply_pre_emphasis(current_frame)
                lbl_coeff.setText(f"Coeff (α): {alpha:.3f}")
            else:
                lbl_coeff.setText("Coeff (α): -.---")

            windowed_frame = self.apply_windowing(current_frame, window_type)
            spectrum_mag = self.calculate_spectrum(windowed_frame)

            pre_emph_status = (
                f" | Pre-emphasis: ON & alpha={alpha:.3f})"
                if chk_pre_emphasis.isChecked()
                else f" | Pre-emphasis: OFF"
            )

            ax1.plot(windowed_frame, color="black")
            ax1.set_title(f"Waveform - {window_type} Window {pre_emph_status}")
            ax1.set_xlabel("Samples")
            ax1.set_ylabel("Amplitude")
            ax1.grid(True)

            if spectrum_mag is not None:
                freqs = np.linspace(0, self.fs / 2, len(spectrum_mag))
                ax2.plot(freqs, spectrum_mag, color="black")
                ax2.set_title("Spectrum Magnitude")
                ax2.set_xlabel("Frequency (Hz)")
                ax2.set_ylabel("Magnitude (dB)")
                ax2.grid(True)
            fig.tight_layout()
            canvas.draw()

        chk_pre_emphasis.stateChanged.connect(update_plot)
        cb_window_dialog.currentIndexChanged.connect(update_plot)
        update_plot()
        dialog.exec_()

    def update_wave_marker(self, frame_index):
        if not hasattr(self, "audio_data") or len(self.audio_data) == 0:
            return

        N = self.spin_N.value()
        M = self.spin_M.value()

        start_time = (frame_index * M) / self.fs
        end_time = (frame_index * M + N) / self.fs

        if hasattr(self, "frame_region") and self.frame_region in self.ax_wave.patches:
            self.frame_region.remove()

        self.frame_region = self.ax_wave.axvspan(
            start_time, end_time, color="red", alpha=0.3
        )

        self.canvas.draw_idle()

    # ~~~##~~~##~~~##~~~##~~~##~~~##~~~##~~~##~~~##~~~##~~~##~~~#
    # --- توابع تکلیف چهارم ---

    def getEnergy(self, frame):
        """$E = \sum x[n]^2$"""
        return float(np.sum(frame.astype(np.float64) ** 2))

    def getZCR(self, frame):
        """$ZCR = \frac{1}{2N} \sum |sgn(x[n]) - sgn(x[n-1])|$"""
        frame_samples = frame.astype(np.float64)
        zcr_count = np.sum(np.abs(np.diff(np.sign(frame_samples)))) / 2
        return float(zcr_count / len(frame_samples))

    def show_energy_zcr(self):
        if not hasattr(self, "audio_data") or len(self.audio_data) == 0:
            QMessageBox.warning(self, "خطا", "فایل صوتی بارگذاری نشده است.")
            return

        N = self.spin_N.value()
        M = self.spin_M.value()
        fno = self.spin_fno.value()

        frame = self.extract_frame(fno, N, M)
        if frame is None:
            return

        energy = self.getEnergy(frame)
        zcr = self.getZCR(frame)

        total_possible_frames = (len(self.audio_data) - N) // M
        step = max(1, total_possible_frames // 100)
        sampled_energies = [
            self.getEnergy(self.extract_frame(i, N, M))
            for i in range(0, total_possible_frames, step)
        ]
        max_energy = max(sampled_energies) if sampled_energies else 1.0
        pct_energy = (energy / max_energy) * 100 if max_energy > 0 else 0

        dialog = QDialog(self)
        dialog.setWindowTitle("نتایج آنالیز تخصصی فریم")
        dialog.setMinimumWidth(450)
        dialog.setLayoutDirection(Qt.RightToLeft)

        layout = QVBoxLayout()

        info_display = QLabel()
        info_display.setStyleSheet(
            "font-family: 'Segoe UI', Tahoma, sans-serif; "
            "font-size: 11pt; "
            "background-color: #f5f5f5; "
            "padding: 15px; "
            "border: 1px solid #ccc; "
            "border-radius: 4px;"
        )

        text = f"<b>📊 اطلاعات فریم انتخاب شده:</b><br>"
        text += "<hr style='border: 0; border-top: 1px solid #ccc;'>"
        text += f"&nbsp;&nbsp;&nbsp;&nbsp;• شماره فریم: <span style='color: #0066cc; font-weight: bold;'>{fno}</span><br>"

        text += f"&nbsp;&nbsp;&nbsp;&nbsp;• انرژی کل فریم (Energy): <span style='color: #2e7d32; font-weight: bold;'>{energy:.5f}</span> "
        text += f"&nbsp;<span style='color: #555; font-size: 10pt;'>({pct_energy:.1f}% از حداکثر انرژی فریم‌ها)</span><br>"
        text += f"&nbsp;&nbsp;&nbsp;&nbsp;• نرخ عبور از صفر (ZCR): <span style='color: #e65100; font-weight: bold;'>{zcr:.4f}</span>"

        info_display.setText(text)
        layout.addWidget(info_display)

        btn_close = QPushButton("بستن")
        btn_close.setMinimumHeight(35)
        btn_close.clicked.connect(dialog.accept)
        layout.addWidget(btn_close)

        dialog.setLayout(layout)
        dialog.exec_()

    def getCORR(self, frame, fs):
        frame_norm = frame.astype(np.float64)
        n = len(frame_norm)

        corr = np.correlate(frame_norm, frame_norm, mode="full")[n - 1 :]

        min_lag = int(fs / 500)
        max_lag = int(fs / 50)

        pitch_freq = 0.0
        if len(corr) > max_lag:
            search_area = corr[min_lag:max_lag]
            if len(search_area) > 0:
                peak_idx = np.argmax(search_area) + min_lag
                if corr[peak_idx] > 0.25 * corr[0]:
                    pitch_freq = float(fs / peak_idx)
        return corr, pitch_freq

    def show_autocorr(self):
        if not hasattr(self, "audio_data") or len(self.audio_data) == 0:
            QMessageBox.warning(self, "خطا", "فایل صوتی بارگذاری نشده است.")
            return

        N = self.spin_N.value()
        M = self.spin_M.value()
        fno = self.spin_fno.value()

        frame = self.extract_frame(fno, N, M)
        if frame is None:
            return

        zcr = self.getZCR(frame)
        corr, pitch = self.getCORR(frame, self.fs)
        voiced = self.isVoiced(frame)
        if not voiced:
            pitch = 0

        dialog = QDialog(self)
        dialog.setWindowTitle("تحلیل توابع خودهمبستگی (Autocorrelation)")
        dialog.setMinimumWidth(550)
        dialog.setLayoutDirection(Qt.RightToLeft)

        layout = QVBoxLayout()

        fig, ax = plt.subplots(figsize=(6, 3.5))
        canvas = FigureCanvas(fig)

        ax.plot(corr, color="#1f77b4", linewidth=1.5, label="R[k]")
        ax.set_title(
            "Autocorrelation Function $R[k]$", fontsize=11, fontweight="bold", pad=10
        )
        ax.set_xlabel("Lag (k)", fontsize=10)
        ax.grid(True, linestyle="--", alpha=0.6)
        fig.tight_layout()

        layout.addWidget(canvas)

        info_display = QLabel()
        info_display.setStyleSheet(
            "font-family: 'Segoe UI', Tahoma, sans-serif; font-size: 11pt; background-color: #f5f5f5; padding: 12px; border: 1px solid #ccc; border-radius: 4px;"
        )

        if voiced and pitch > 0:
            pitch_status = f"<span style='color: #2e7d32; font-weight: bold;'>{pitch:.2f} Hz [واک‌دار - Voiced]</span>"
        else:
            pitch_status = "<span style='color: #e65100; font-weight: bold;'>تعریف‌نشده [بی‌واک - Unvoiced]</span>"

        text = f"<b>📊 نتایج تحلیل فریم {fno}:</b><br>"
        text += "<hr style='border: 0; border-top: 1px solid #ccc;'>"
        text += f"&nbsp;&nbsp;&nbsp;&nbsp;• نرخ عبور از صفر (ZCR): {zcr:.4f}<br>"
        text += f"&nbsp;&nbsp;&nbsp;&nbsp;• وضعیت و فرکانس گام: {pitch_status}"

        info_display.setText(text)
        layout.addWidget(info_display)

        obs_lbl = QLabel(
            "<b>💡 مشاهده علمی رفتار سیگنال:</b><br>"
            "در فریم‌های <b>واک‌دار (Voiced)</b>، به دلیل تناوبی بودن حرکت تارهای صوتی، تابع اتوکورولیشن دارای قله‌های "
            "تناوبی بسیار واضح و ثانویه است که فاصله اولین قله بزرگ بعد از مبدا، عکسِ فرکانس گام (Pitch) است.<br>"
            "در مقابل، در فریم‌های <b>بی‌واک (Unvoiced)</b> یا نویزی، قله‌ها کاملاً نامنظم بوده و فقط قله اصلی در تأخیر صفر (Lag=0) "
            "به شدت غالب است."
        )
        obs_lbl.setWordWrap(True)
        obs_lbl.setStyleSheet(
            "font-family: Tahoma, sans-serif; font-size: 10pt; color: #444; line-height: 1.5;"
        )
        layout.addWidget(obs_lbl)

        btn_close = QPushButton("بستن")
        btn_close.clicked.connect(dialog.accept)
        layout.addWidget(btn_close)

        dialog.setLayout(layout)
        dialog.exec_()

    def getAMDF(self, frame, fs):
        frame_data = frame.astype(np.float64)
        n = len(frame_data)
        amdf = np.zeros(n)

        for k in range(n):
            amdf[k] = np.sum(np.abs(frame_data[: n - k] - frame_data[k:]))

        min_lag = int(fs / 500)
        max_lag = int(fs / 50)

        pitch_freq = 0.0
        if len(amdf) > max_lag:
            search_area = amdf[min_lag:max_lag]
            if len(search_area) > 0:
                valley_idx = np.argmin(search_area) + min_lag
                # آستانه تشخیص دره عمیق برای فریم واکدار
                if amdf[valley_idx] < 0.65 * np.max(amdf):
                    pitch_freq = float(fs / valley_idx)

        return amdf, pitch_freq

    def show_amdf(self):
        if not hasattr(self, "audio_data") or len(self.audio_data) == 0:
            QMessageBox.warning(self, "خطا", "فایل صوتی بارگذاری نشده است.")
            return

        N = self.spin_N.value()
        M = self.spin_M.value()
        fno = self.spin_fno.value()

        frame = self.extract_frame(fno, N, M)
        if frame is None:
            return

        zcr = self.getZCR(frame)
        amdf, pitch = self.getAMDF(frame, self.fs)
        voiced = self.isVoiced(frame)
        if not voiced:
            pitch = 0

        dialog = QDialog(self)
        dialog.setWindowTitle("تحلیل تابع AMDF")
        dialog.setMinimumWidth(550)
        dialog.setLayoutDirection(Qt.RightToLeft)

        layout = QVBoxLayout()

        fig, ax = plt.subplots(figsize=(6, 3.5))
        canvas = FigureCanvas(fig)

        ax.plot(amdf, color="#d62728", linewidth=1.5, label="D[k]")
        ax.set_title(
            "Average Magnitude Difference Function (AMDF)",
            fontsize=11,
            fontweight="bold",
            pad=10,
        )
        ax.set_xlabel("Lag (k)", fontsize=10)
        ax.set_ylabel("Difference", fontsize=10)
        ax.grid(True, linestyle="--", alpha=0.6)
        ax.legend(loc="upper right")
        fig.tight_layout()

        layout.addWidget(canvas)

        info_display = QLabel()
        info_display.setStyleSheet(
            "font-family: 'Segoe UI', Tahoma, sans-serif; font-size: 11pt; background-color: #f5f5f5; padding: 12px; border: 1px solid #ccc; border-radius: 4px;"
        )

        if voiced and pitch > 0:
            pitch_status = f"<span style='color: #2e7d32; font-weight: bold;'>{pitch:.2f} Hz [واک‌دار - Voiced]</span>"
        else:
            pitch_status = "<span style='color: #e65100; font-weight: bold;'>تعریف‌نشده [بی‌واک - Unvoiced]</span>"

        text = f"<b>📊 نتایج تحلیل AMDF فریم {fno}:</b><br>"
        text += "<hr style='border: 0; border-top: 1px solid #ccc;'>"
        text += f"&nbsp;&nbsp;&nbsp;&nbsp;• نرخ عبور از صفر (ZCR): {zcr:.4f}<br>"
        text += f"&nbsp;&nbsp;&nbsp;&nbsp;• وضعیت و فرکانس گام: {pitch_status}"

        info_display.setText(text)
        layout.addWidget(info_display)

        obs_lbl = QLabel(
            "<b>💡 مشاهده علمی:</b><br>"
            "در تابع AMDF، برعکس اتوکورولیشن، برای فریم‌های <b>واک‌دار (Voiced)</b>، در دوره‌های تناوب گام (Pitch) "
            "شاهد ایجاد 'دره' (Valley) یا کمینه‌های عمیق هستیم. فریم‌های بی‌واک فاقد این دره‌های منظم هستند."
        )
        obs_lbl.setWordWrap(True)
        obs_lbl.setStyleSheet(
            "font-family: Tahoma, sans-serif; font-size: 10pt; color: #444; line-height: 1.5;"
        )
        layout.addWidget(obs_lbl)

        btn_close = QPushButton("بستن")
        btn_close.clicked.connect(dialog.accept)
        layout.addWidget(btn_close)

        dialog.setLayout(layout)
        dialog.exec_()

    def getFormant(self, frame, fs):
        from scipy.signal import find_peaks, lfilter

        pre_emphasis = 0.97
        emphasized_frame = np.append(frame[0], frame[1:] - pre_emphasis * frame[:-1])

        windowed = emphasized_frame * np.hamming(len(emphasized_frame))

        fft_size = 1024
        A = np.fft.fft(windowed, fft_size)
        half_len = fft_size // 2
        freqs = np.linspace(0, fs / 2, half_len)
        mag = 20 * np.log10(np.abs(A[:half_len]) + 1e-10)

        log_mag_full = np.log(np.abs(A) + 1e-10)
        ceps = np.fft.ifft(log_mag_full).real

        lifter_cutoff = 32  
        ceps_smoothed = np.zeros_like(ceps)
        ceps_smoothed[:lifter_cutoff] = ceps[:lifter_cutoff]
        ceps_smoothed[-lifter_cutoff + 1 :] = ceps[-lifter_cutoff + 1 :]

        smoothed_log_spectrum = np.fft.fft(ceps_smoothed).real[:half_len]
        smoothed_mag = smoothed_log_spectrum * (20 / np.log(10))

        peaks, _ = find_peaks(
            smoothed_mag, distance=int(fs / 4000 * 20), prominence=0.6
        )

        formants = freqs[peaks]

        valid_formants = [f for f in formants if 200 < f < 6000]

        has_high_formant = any(1800 <= f <= 3000 for f in valid_formants)
        if not has_high_formant:
            idx_baze = np.where((freqs >= 1800) & (freqs <= 3000))[0]
            if len(idx_baze) > 0:
                sub_smoothed = smoothed_mag[idx_baze]
                sub_peaks, _ = find_peaks(sub_smoothed, distance=5, prominence=0.3)
                if len(sub_peaks) > 0:
                    highest_sub_peak = freqs[
                        idx_baze[sub_peaks[np.argmax(sub_smoothed[sub_peaks])]]
                    ]
                    valid_formants.append(highest_sub_peak)
                    valid_formants = sorted(list(set(valid_formants)))

        has_high_formant = any(3000 <= f <= 4000 for f in valid_formants)
        if not has_high_formant:
            idx_baze = np.where((freqs >= 3000) & (freqs <= 4000))[0]
            if len(idx_baze) > 0:
                sub_smoothed = smoothed_mag[idx_baze]
                sub_peaks, _ = find_peaks(sub_smoothed, distance=5, prominence=0.3)
                if len(sub_peaks) > 0:
                    highest_sub_peak = freqs[
                        idx_baze[sub_peaks[np.argmax(sub_smoothed[sub_peaks])]]
                    ]
                    valid_formants.append(highest_sub_peak)
                    valid_formants = sorted(list(set(valid_formants)))

        has_high_formant = any(4000 <= f <= 8000 for f in valid_formants)
        if not has_high_formant:
            idx_baze = np.where((freqs >= 4000) & (freqs <= 8000))[0]
            if len(idx_baze) > 0:
                sub_smoothed = smoothed_mag[idx_baze]
                sub_peaks, _ = find_peaks(sub_smoothed, distance=5, prominence=0.3)
                if len(sub_peaks) > 0:
                    highest_sub_peak = freqs[
                        idx_baze[sub_peaks[np.argmax(sub_smoothed[sub_peaks])]]
                    ]
                    valid_formants.append(highest_sub_peak)
                    valid_formants = sorted(list(set(valid_formants)))

        return freqs, mag, smoothed_mag, valid_formants[:6]

    def show_formants(self):
        if not hasattr(self, "audio_data") or len(self.audio_data) == 0:
            QMessageBox.warning(self, "خطا", "فایل صوتی بارگذاری نشده است.")
            return

        N = self.spin_N.value()
        M = self.spin_M.value()
        fno = self.spin_fno.value()

        frame = self.extract_frame(fno, N, M)
        if frame is None:
            return

        freqs, mag, smoothed, formants = self.getFormant(frame, self.fs)

        dialog = QDialog(self)
        dialog.setWindowTitle("تحلیل فرمنت‌ها (Formant Analysis)")
        dialog.setMinimumWidth(600)
        dialog.setLayoutDirection(Qt.RightToLeft)

        layout = QVBoxLayout()

        fig, ax = plt.subplots(figsize=(6, 4))
        canvas = FigureCanvas(fig)

        ax.plot(freqs, mag, color="#aec7e8", label="Spectrum", alpha=0.6)
        ax.plot(
            freqs, smoothed, color="#d62728", linewidth=2, label="Smoothed Envelope"
        )

        for i, f in enumerate(formants):
            ax.axvline(x=f, color="#2ca02c", linestyle="--", linewidth=1.5)
            ax.text(
                f,
                max(smoothed) * 0.9,
                f"F{i+1}",
                color="#2ca02c",
                fontweight="bold",
                ha="center",
            )

        ax.set_title(
            "Spectrum and Formants Analysis", fontsize=11, fontweight="bold", pad=10
        )
        ax.set_xlabel("Frequency (Hz)", fontsize=10)
        ax.set_ylabel("Magnitude", fontsize=10)
        ax.grid(True, linestyle="--", alpha=0.6)
        ax.legend(loc="lower right", frameon=True, facecolor="white", framealpha=0.8)
        fig.tight_layout()

        layout.addWidget(canvas)

        info_display = QLabel()
        info_display.setStyleSheet(
            "font-family: 'Segoe UI', Tahoma, sans-serif; font-size: 10pt; background-color: #f5f5f5; padding: 12px; border: 1px solid #ccc; border-radius: 4px;"
        )

        f_list = "<br>".join(
            [f"&nbsp;&nbsp;• <b>F{i+1}</b>: {f:.0f} Hz" for i, f in enumerate(formants)]
        )

        text = f"<b>📊 نتایج فرکانس‌های فرمنت (فریم {fno}):</b><br>"
        text += "<hr style='border: 0; border-top: 1px solid #ccc;'>"

        if formants:
            text += f"{f_list}"
        else:
            text += "فرمنتی در این فریم شناسایی نشد."

        info_display.setText(text)
        layout.addWidget(info_display)

        obs_lbl = QLabel(
            "<b>💡 مشاهده علمی:</b><br>"
            "فرمنت‌ها در واقع رزونانس‌های مجرای گفتار (Vocal Tract) هستند. تغییر شکل زبان و لب‌ها باعث جابجایی این "
            "قله‌های پهن در پوش طیفی شده و باعث تمایز بین واکه‌ها (حروف صدادار) مختلف می‌شود."
        )
        obs_lbl.setWordWrap(True)
        obs_lbl.setStyleSheet(
            "font-family: Tahoma, sans-serif; font-size: 10pt; color: #444; line-height: 1.5;"
        )
        layout.addWidget(obs_lbl)

        btn_close = QPushButton("بستن")
        btn_close.clicked.connect(dialog.accept)
        layout.addWidget(btn_close)

        dialog.setLayout(layout)
        dialog.exec_()

    def getCEPSTRAL(self, frame, fs):
        x = np.asarray(frame, dtype=float)
        x = x - np.mean(x)
        x = x * np.blackman(len(x))

        nfft = 1024
        if len(x) > nfft:
            nfft = 2 ** int(np.ceil(np.log2(len(x))))

        X = np.fft.fft(x, n=nfft)
        log_mag = np.log(np.maximum(np.abs(X), 1e-10))
        ceps = np.fft.ifft(log_mag).real

        ceps = ceps[: nfft // 2]

        liftered = np.zeros_like(ceps)
        min_lag = int(fs / 500)
        max_lag = int(fs / 50)
        max_lag = min(max_lag, len(ceps) - 1)
        liftered[min_lag:max_lag] = ceps[min_lag:max_lag]

        def smooth(y, win=3):
            if len(y) < win:
                return y
            kernel = np.ones(win) / win
            return np.convolve(y, kernel, mode="same")

        ceps_plot = ceps.copy()
        ceps_plot[:1] = 0

        pitch_freq = 0.0
        peak_idx = None

        if max_lag > min_lag:
            search_area = liftered[min_lag:max_lag]
            smoothed_search = smooth(search_area, win=3)

            if len(smoothed_search) > 0:
                local_peak = int(np.argmax(smoothed_search))
                peak_idx = local_peak + min_lag
                peak_val = ceps[peak_idx]

                region_mean = np.mean(np.abs(search_area))
                region_std = np.std(search_area)
                threshold = region_mean + 0.5 * region_std

                if peak_val > threshold:
                    pitch_freq = float(fs / peak_idx)
                else:
                    peak_idx = None

        return ceps_plot, pitch_freq, peak_idx

    def show_cepstral(self):
        if not hasattr(self, "audio_data") or len(self.audio_data) == 0:
            QMessageBox.warning(self, "خطا", "فایل صوتی بارگذاری نشده است.")
            return
    
        N = self.spin_N.value()
        M = self.spin_M.value()
        fno = self.spin_fno.value()
    
        frame = self.extract_frame(fno, N, M)
        if frame is None:
            return
    
        zcr = self.getZCR(frame)
        ceps, pitch, peak_idx = self.getCEPSTRAL(frame, self.fs)
    
        energy = np.mean(np.array(frame, dtype=float) ** 2)
        energy_db = 10 * np.log10(energy + 1e-12)
    
        min_lag = int(self.fs / 500)
        max_lag = int(self.fs / 50)
        max_lag = min(max_lag, len(ceps) - 1)
    
        voiced = self.isVoiced(frame)
    
        # ایجاد دایالوگ با ساختار و چیدمان مشابه AMDF
        dialog = QDialog(self)
        dialog.setWindowTitle("تحلیل کِپستروم (Cepstral Analysis)")
        dialog.setMinimumWidth(550)  # هم‌اندازه با پنجره AMDF
        dialog.setLayoutDirection(Qt.RightToLeft)  # راست‌چین کردن پنجره
    
        layout = QVBoxLayout()
    
        fig, ax = plt.subplots(figsize=(6, 3.5))  # هماهنگ‌سازی ابعاد نمودار
        canvas = FigureCanvas(fig)
    
        # رسم نمودار با رنگ‌بندی و فونت‌های اصلاح‌شده
        ax.plot(ceps, color="#1f77b4", linewidth=1.2, label="Cepstrum")
        ax.set_xlim(0, len(ceps) - 1)
    
        ymin = np.min(ceps)
        ymax = np.max(ceps)
        margin = 0.1 * (ymax - ymin + 1e-6)
        ax.set_ylim(ymin - margin, ymax + margin)
    
        if voiced and peak_idx is not None:
            ellipse_start = peak_idx - 10
            ellipse_end = len(ceps) - 1
            ellipse_center_x = (ellipse_start + ellipse_end) / 2
            ellipse_width = ellipse_end - ellipse_start
    
            ellipse_center_y = ceps[peak_idx]
            ellipse_height = (ymax - ymin) * 0.4
    
            from matplotlib.patches import Ellipse
    
            ellipse = Ellipse(
                xy=(ellipse_center_x, ellipse_center_y),
                width=ellipse_width,
                height=ellipse_height,
                edgecolor="red",
                facecolor="none",
                linewidth=1.5,
                linestyle="--",
                alpha=0.8,
            )
            ax.add_patch(ellipse)
    
            ax.annotate(
                f"{pitch:.1f} Hz",
                xy=(peak_idx, ceps[peak_idx]),
                xytext=(peak_idx + 3, ceps[peak_idx] + ellipse_height * 0.6),
                fontsize=9,
                arrowprops=dict(arrowstyle="->", color="red"),
                color="red",
            )
    
        title = "Cepstrum of Voiced Speech" if voiced else "Cepstrum of Unvoiced Speech"
        ax.set_title(title, fontsize=11, fontweight="bold", pad=10)
        ax.set_xlabel("Quefrency (Samples)", fontsize=10)
        ax.set_ylabel("Cepstral Value", fontsize=10)
        ax.grid(True, linestyle="--", alpha=0.6)  # هماهنگ با استایل شبکه AMDF
        ax.legend(loc="upper right")
        fig.tight_layout()
    
        layout.addWidget(canvas)
    
        # بخش نمایش اطلاعات (Info Display) کاملاً هماهنگ با استایل قبلی
        info_display = QLabel()
        info_display.setStyleSheet(
            "font-family: 'Segoe UI', Tahoma, sans-serif; font-size: 11pt; background-color: #f5f5f5; padding: 12px; border: 1px solid #ccc; border-radius: 4px;"
        )
    
        # تعیین وضعیت واک‌داری با همان رنگ‌های سبز و نارنجی استانداردی که استفاده کردید
        if voiced and pitch > 0:
            pitch_status = f"<span style='color: #2e7d32; font-weight: bold;'>{pitch:.2f} Hz [واک‌دار - Voiced]</span>"
        else:
            pitch_status = "<span style='color: #e65100; font-weight: bold;'>تعریف‌نشده [بی‌واک - Unvoiced]</span>"
    
        # ساخت متن گزارش به صورت فارسی و راست‌چین
        text = f"<b>📊 نتایج تحلیل کپسترال فریم {fno}:</b><br>"
        text += "<hr style='border: 0; border-top: 1px solid #ccc;'>"
        text += f"&nbsp;&nbsp;&nbsp;&nbsp;• طول فریم: {N} نمونه<br>"
        text += f"&nbsp;&nbsp;&nbsp;&nbsp;• نرخ نمونه‌برداری: {self.fs} هرتز<br>"
        text += f"&nbsp;&nbsp;&nbsp;&nbsp;• نرخ عبور از صفر (ZCR): {zcr:.4f}<br>"
        text += f"&nbsp;&nbsp;&nbsp;&nbsp;• انرژی فریم: {energy_db:.2f} dB<br>"
        text += f"&nbsp;&nbsp;&nbsp;&nbsp;• وضعیت و فرکانس گام: {pitch_status}"
        
        if voiced and peak_idx is not None:
            text += f"<br>&nbsp;&nbsp;&nbsp;&nbsp;• شاخص پیک گام (Lag): {peak_idx} نمونه"
    
        info_display.setText(text)
        layout.addWidget(info_display)
    
        # افزودن کادر علمی متناسب با تحلیل Cepstral
        obs_lbl = QLabel(
            "<b>💡 مشاهده علمی:</b><br>"
            "در تحلیل کپستروم، سیگنال به قلمرو <b>Quefrency</b> منتقل می‌شود. برای فریم‌های <b>واک‌دار (Voiced)</b>، "
            "یک «پیک» (Peak) یا برجستگی متمایز در فواصل دوره‌ای گام ظاهر می‌شود که نشان‌دهنده فرکانس اصلی تارآواهاست. "
            "در فریم‌های بی‌واک، چنین پیک شاخصی دیده نمی‌شود."
        )
        obs_lbl.setWordWrap(True)
        obs_lbl.setStyleSheet(
            "font-family: Tahoma, sans-serif; font-size: 10pt; color: #444; line-height: 1.5;"
        )
        layout.addWidget(obs_lbl)
    
        # دکمه بستن دایالوگ
        btn_close = QPushButton("بستن")
        btn_close.clicked.connect(dialog.accept)
        layout.addWidget(btn_close)
    
        dialog.setLayout(layout)
        dialog.exec_()
        
        
    def find_consecutive_v_uv_frames(self, N, M):
        if not hasattr(self, "audio_data") or len(self.audio_data) == 0:
            return [], "No Data"
    
        total_samples = len(self.audio_data)
        max_frame = ((total_samples - N) // M) + 1
    
        frame_types = []  # 1=Voiced, 0=Unvoiced
        energies = []
        zcrs = []
    
        for fno in range(max_frame):
            frame = self.extract_frame(fno, N, M)
            if frame is None:
                break
            e = self.getEnergy(frame)
            z = self.getZCR(frame)
            energies.append(e)
            zcrs.append(z)
    
        energies = np.array(energies)
        zcrs = np.array(zcrs)
    
        med_energy = np.median(energies[energies > np.min(energies)])
        med_zcr = np.median(zcrs)
    
        for fno in range(max_frame):
            frame = self.extract_frame(fno, N, M)
            if frame is None:
                break
            frame_types.append(1 if self.isVoiced(frame) else 0)

        pairs_found = []
        idx = 0
        while idx < len(frame_types) - 1:
            t1, t2 = frame_types[idx], frame_types[idx + 1]
            if t1 != t2:
                # ذخیره نوع هر فریم به صورت صریح
                label = "واکدار ⬅️ بی‌واک" if t1 == 1 else "بی‌واک ⬅️ واکدار"
                pairs_found.append((idx, idx + 1, label, t1, t2))
                idx += 2
            else:
                idx += 1

        if not pairs_found:
            voiced_indices = np.where(np.array(frame_types) == 1)[0]
            unvoiced_indices = np.where(np.array(frame_types) == 0)[0]
            if len(voiced_indices) > 0 and len(unvoiced_indices) > 0:
                v_idx = voiced_indices[0]
                u_idx = unvoiced_indices[np.argmin(np.abs(unvoiced_indices - v_idx))]
                i1, i2 = min(v_idx, u_idx), max(v_idx, u_idx)
                t1, t2 = frame_types[i1], frame_types[i2]
                label = "نزدیک‌ترین جفت غیرمتوالی"
                pairs_found.append((i1, i2, label, t1, t2))
    
        return pairs_found, f"تعداد {len(pairs_found)} جفت فریم در گفتار طبیعی یافت شد."
    
    def isVoiced(self, frame):
        """تشخیص واکداری با ترکیب ZCR، انرژی و کپسترال"""
        zcr = self.getZCR(frame)
        energy = np.mean(np.array(frame, dtype=float) ** 2)
        energy_db = 10 * np.log10(energy + 1e-12)
        
        _, pitch, peak_idx = self.getCEPSTRAL(frame, self.fs)
        
        has_pitch = (pitch > 0 and peak_idx is not None)
        low_zcr = zcr < 0.20
        high_energy = energy_db > -20

        return has_pitch and (low_zcr or high_energy)
    
    def compare_voiced_unvoiced(self):
        if not hasattr(self, "audio_data") or len(self.audio_data) == 0:
            QMessageBox.warning(self, "خطا", "فایل صوتی بارگذاری نشده است.")
            return
    
        N = self.spin_N.value()
        M = self.spin_M.value()
    
        pairs, status_msg = self.find_consecutive_v_uv_frames(N, M)
    
        # فیلتر سکوت
        total_possible_frames = (len(self.audio_data) - N) // M
        step = max(1, total_possible_frames // 100)
        sampled_energies = [
            self.getEnergy(self.extract_frame(i, N, M))
            for i in range(0, total_possible_frames, step)
        ]
        max_energy = max(sampled_energies) if sampled_energies else 1.0
        silence_threshold = max_energy * 0.005
    
        pairs = [
            p for p in pairs
            if self.getEnergy(self.extract_frame(p[0], N, M)) > silence_threshold
            and self.getEnergy(self.extract_frame(p[1], N, M)) > silence_threshold
        ]
    
        if not pairs:
            QMessageBox.warning(self, "خطا",
                "هیچ جفت فریم متوالیِ واکدار و بی‌واک واقعی (خارج از سکوت) در این سیگنال پیدا نشد.")
            return
    
        dialog = QDialog(self)
        dialog.setWindowTitle("انتخاب و مقایسه جفت فریم‌های متوالی گفتار")
        dialog.setMinimumWidth(600)
        dialog.setLayoutDirection(Qt.RightToLeft)
        layout = QVBoxLayout()
    
        selector_layout = QHBoxLayout()
        selector_layout.addWidget(QLabel("جفت فریم مورد نظر را انتخاب کنید:"))
        combo_pairs = QComboBox()
        for i, (fno1, fno2, direction, t1, t2) in enumerate(pairs):
            combo_pairs.addItem(
                f"جفت {i+1} (فریم‌های {fno1} و {fno2}) | جهت: {direction}",
                (fno1, fno2, direction, t1, t2)
            )
        selector_layout.addWidget(combo_pairs)
        layout.addLayout(selector_layout)
    
        info_display = QLabel()
        info_display.setStyleSheet("""
            font-family: 'Segoe UI', Tahoma, sans-serif;
            font-size: 11pt;
            background-color: #f5f5f5;
            padding: 12px;
            border: 1px solid #ccc;
            border-radius: 4px;
        """)
        layout.addWidget(info_display)
    
        analysis_lbl = QLabel(
            "<b>💡 مشاهده علمی:</b><br>"
            "در تمام جفت‌های فوق کاملاً مشهود است که فریم‌های <b>واک‌دار</b> (حرکت تارهای صوتی) "
            "دارای انرژی بسیار بالا و ZCR ناچیزی هستند. در مقابل، فریم‌های <b>بی‌واک</b> "
            "(صامت‌های نویزی مثل س، ش) به دلیل فرکانس بالا بودن ماهیت فیزیکی‌شان، "
            "انرژی کل ناچیز اما نرخ عبور از صفر (ZCR) بسیار شدیدی دارند."
        )
        analysis_lbl.setWordWrap(True)
        analysis_lbl.setStyleSheet(
            "font-family: Tahoma, sans-serif; font-size: 10pt; color: #444; line-height: 1.5;"
        )
        layout.addWidget(analysis_lbl)
    
        def clear_regions():
            for region in getattr(self, "compare_regions", []):
                try:
                    region.remove()
                except Exception:
                    pass
            self.compare_regions = []
    
        def update_pair_info():
            selected = combo_pairs.currentData()
            if not selected:
                return
    
            fno1, fno2, direction, t1, t2 = selected
            frame1 = self.extract_frame(fno1, N, M)
            frame2 = self.extract_frame(fno2, N, M)
    
            e1, z1 = self.getEnergy(frame1), self.getZCR(frame1)
            e2, z2 = self.getEnergy(frame2), self.getZCR(frame2)

            def frame_badge(t):
                if t == 1:
                    return ("<span style='color:#2e7d32;font-weight:bold;'>[واک‌دار - Voiced]</span>", "green")
                return ("<span style='color:#e65100;font-weight:bold;'>[بی‌واک - Unvoiced]</span>", "orange")
    
            badge1, color1 = frame_badge(t1)
            badge2, color2 = frame_badge(t2)
    
            pct1 = (e1 / max_energy) * 100 if max_energy > 0 else 0
            pct2 = (e2 / max_energy) * 100 if max_energy > 0 else 0
    
            text = f"<b>📊 اطلاعات جفت انتخاب شده ({direction}):</b><br>"
            text += "<hr style='border:0;border-top:1px solid #ccc;'>"
            for fno, badge, e, z, pct in [(fno1, badge1, e1, z1, pct1), (fno2, badge2, e2, z2, pct2)]:
                text += f"<b>◀️ فریم (شماره {fno}):</b><br>"
                text += f"&nbsp;&nbsp;&nbsp;&nbsp;• نوع سیگنال: {badge}<br>"
                text += f"&nbsp;&nbsp;&nbsp;&nbsp;• انرژی فریم: {e:.5f} &nbsp;<span style='color:#0066cc;'>({pct:.1f}% از کل انرژی صوتی)</span><br>"
                text += f"&nbsp;&nbsp;&nbsp;&nbsp;• نرخ عبور از صفر (ZCR): {z:.4f}<br><br>"
    
            info_display.setText(text)

            clear_regions()
            for fno, color in [(fno1, color1), (fno2, color2)]:
                start_t = (fno * M) / self.fs
                end_t = (fno * M + N) / self.fs
                self.compare_regions.append(
                    self.ax_wave.axvspan(start_t, end_t, color=color, alpha=0.35)
                )
            self.canvas.draw_idle()
    
        combo_pairs.currentIndexChanged.connect(update_pair_info)
        update_pair_info()
    
        btn_close = QPushButton("بستن")
        btn_close.clicked.connect(dialog.accept)
        layout.addWidget(btn_close)
    
        dialog.setLayout(layout)
        dialog.exec_()

        clear_regions()
        self.canvas.draw_idle()

    def compare_pitch_200(self):
        if not hasattr(self, "audio_data") or len(self.audio_data) == 0:
            QMessageBox.warning(self, "خطا", "فایل صوتی بارگذاری نشده است.")
            return
    
        N = self.spin_N.value()
        M = self.spin_M.value()
        start_fno = self.spin_fno.value()
    
        pitches_corr = []
        pitches_ceps = []
        frames_idx = []
    
        for i in range(200):
            fno = start_fno + i
            frame = self.extract_frame(fno, N, M)
            if frame is None:
                break
    
            _, p_corr = self.getCORR(frame, self.fs)
            _, p_ceps, _ = self.getCEPSTRAL(frame, self.fs)
    
            pitches_corr.append(p_corr)
            pitches_ceps.append(p_ceps)
            frames_idx.append(fno)

        dialog = QDialog(self)
        dialog.setWindowTitle("مقایسه فرکانس گام (۲۰۰ فریم)")
        dialog.setMinimumWidth(600)  # عرض متناسب با دو نمودار زیر هم
        dialog.setLayoutDirection(Qt.RightToLeft)  # راست‌چین کردن پنجره
    
        layout = QVBoxLayout()
    
        # تنظیم بهینه ابعاد نمودارها برای نمایش زیر هم
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6, 5))
        canvas = FigureCanvas(fig)

        ax1.plot(frames_idx, pitches_corr, "b.", markersize=4, label="Autocorr Pitch")
        ax1.set_title("Pitch Tracking using Autocorrelation", fontsize=10, fontweight="bold")
        ax1.set_ylabel("Pitch (Hz)", fontsize=9)
        ax1.grid(True, linestyle="--", alpha=0.6)
        ax1.legend(loc="upper right", fontsize=8)
    
        # نمودار دوم: کپستروم
        ax2.plot(frames_idx, pitches_ceps, "r.", markersize=4, label="Cepstral Pitch")
        ax2.set_title("Pitch Tracking using Cepstrum", fontsize=10, fontweight="bold")
        ax2.set_xlabel("Frame Number", fontsize=9)
        ax2.set_ylabel("Pitch (Hz)", fontsize=9)
        ax2.grid(True, linestyle="--", alpha=0.6)
        ax2.legend(loc="upper right", fontsize=8)
        
        fig.tight_layout()
        layout.addWidget(canvas)

        info_display = QLabel()
        info_display.setStyleSheet(
            "font-family: 'Segoe UI', Tahoma, sans-serif; font-size: 11pt; background-color: #f5f5f5; padding: 12px; border: 1px solid #ccc; border-radius: 4px;"
        )
    
        actual_frames_count = len(frames_idx)
        text = f"<b>📊 گزارش مقایسه الگوریتم‌های ردیابی گام (Pitch Tracking):</b><br>"
        text += "<hr style='border: 0; border-top: 1px solid #ccc;'>"
        text += f"&nbsp;&nbsp;&nbsp;&nbsp;• فریم شروع: {start_fno}<br>"
        text += f"&nbsp;&nbsp;&nbsp;&nbsp;• تعداد فریم‌های آنالیز شده: {actual_frames_count} فریم<br>"
        text += f"&nbsp;&nbsp;&nbsp;&nbsp;• متدهای مقایسه‌شده: اتوکورولیشن (Autocorrelation) و کپسترال (Cepstral)"
    
        info_display.setText(text)
        layout.addWidget(info_display)

        obs_lbl = QLabel(
            "<b>💡 مشاهده علمی:</b><br>"
            "روش <b>کپستروم</b> مقاومت بسیار بهتری در برابر تغییرات فرمنت‌ها دارد، چرا که اثر فیلتر مجرای گفتار را "
            "از منبع صوت (تارآواها) جدا می‌کند. با این حال، در سیگنال‌های نویزی و محیط‌های عملی، روش <b>اتوکورولیشن (Autocorrelation)</b> "
            "معمولاً پاسخ‌های پایدارتر و قله‌های واضح‌تری را برای یافتن فرکانس گام ارائه می‌دهد."
        )
        obs_lbl.setWordWrap(True)
        obs_lbl.setStyleSheet(
            "font-family: Tahoma, sans-serif; font-size: 10pt; color: #444; line-height: 1.5;"
        )
        layout.addWidget(obs_lbl)

        btn_close = QPushButton("بستن")
        btn_close.clicked.connect(dialog.accept)
        layout.addWidget(btn_close)
    
        dialog.setLayout(layout)
        dialog.exec_()


# ~~~##~~~##~~~##~~~##~~~##~~~##~~~##~~~##~~~##~~~##~~~##~~~#
# ~/|\~##~/|\~##~/|\~##~/|\~##~/|\~##~/|\~##~/|\~##~/|\~##~/|\~#

if __name__ == "__main__":
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)

    ex = AudioApp()
    ex.show()

    app.exec_()