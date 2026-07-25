import sys
import os
import numpy as np
import sounddevice as sd
import soundfile as sf
from scipy import signal
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QComboBox, 
                             QFileDialog, QGroupBox, QLineEdit, QDoubleSpinBox, QSpinBox)
from PyQt5.QtCore import Qt, QTimer, QElapsedTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT
import matplotlib.pyplot as plt

#~~~##~~~##~~~##~~~##~~~##~~~##~~~##~~~##~~~##~~~##~~~##~~~#
#~/|\~##~/|\~##~/|\~##~/|\~##~/|\~##~/|\~##~/|\~##~/|\~##~/|\~#
class AudioApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("نرم افزار تحلیل و ضبط صوت")
        self.setGeometry(100, 100, 1400, 700)

        #~/|\~##~/|\~##~/|\~##~/|\~##~/|\~##~/|\~##~/|\~##~/|\~##~/|\~#
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
                    QMainWindow { background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #e0c3fc, stop:1 #8ec5fc); }
                    QWidget#CentralWidget { background: transparent; }
                    QPushButton, QComboBox, QSpinBox, QDoubleSpinBox, QLineEdit { background-color: rgba(255, 255, 255, 0.4); border: 1px solid rgba(255, 255, 255, 0.6); border-radius: 4px; color: #333; padding: 5px; }
                    QPushButton:hover { background-color: rgba(255, 255, 255, 0.6); }
                    QPushButton:disabled, QComboBox:disabled { background-color: rgba(255, 255, 255, 0.15); border: 1px solid rgba(255, 255, 255, 0.2); color: rgba(51, 51, 51, 0.4); }
                    QPushButton:pressed { background-color: rgba(0, 0, 0, 0.08); border: 1px solid rgba(0, 0, 0, 0.15); color: rgba(51, 51, 51, 0.8); }
                    QGroupBox { background-color: rgba(255, 255, 255, 0.2); border: 1px solid rgba(255, 255, 255, 0.5); border-radius: 10px; margin-top: 2ex; color: #333; }
                    QGroupBox::title { subcontrol-origin: margin; left: 10px; color: #0052D4; }
                    QLabel { color: #333; font-weight: bold; }
                """,
                "mpl_text": "black",
                "mpl_face": (0.0, 0.0, 0.0, 0.05),
                "mpl_edge": (0.0, 0.0, 0.0, 0.3)
            },
            {
                "name": "Dark Glass",
                "qss": """
                    QMainWindow { background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #0f2027, stop:0.5 #203a43, stop:1 #2c5364); }
                    QWidget#CentralWidget { background: transparent; }
                    QPushButton, QComboBox, QSpinBox, QDoubleSpinBox, QLineEdit { background-color: rgba(255, 255, 255, 0.15); border: 1px solid rgba(255, 255, 255, 0.3); border-radius: 4px; color: white; padding: 5px; }
                    QPushButton:hover { background-color: rgba(255, 255, 255, 0.25); }
                    QPushButton:disabled { background-color: rgba(200, 200, 200, 0.05); color: rgba(255, 255, 255, 0.3); border: 1px solid rgba(255, 255, 255, 0.1); }
                    QPushButton:pressed { background-color: rgba(0, 0, 0, 0.3); border: 1px solid rgba(255, 255, 255, 0.1); color: rgba(255, 255, 255, 0.7); }
                    QGroupBox { background-color: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.2); border-radius: 10px; margin-top: 2ex; color: white; }
                    QGroupBox::title { subcontrol-origin: margin; left: 10px; color: #4facfe; }
                    QLabel { color: white; font-weight: bold; }
                """,
                "mpl_text": "black",
                "mpl_face": (0.0, 0.0, 0.0, 0.05),
                "mpl_edge": (0.0, 0.0, 0.0, 0.3)
            }
        ]
        
        self.init_ui()

    #~~~##~~~##~~~##~~~##~~~##~~~##~~~##~~~##~~~##~~~##~~~##~~~#

    def init_ui(self):
        main_widget = QWidget()
        main_widget.setObjectName("CentralWidget")
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)

        #~/|\~##~/|\~##~/|\~##~/|\~##~/|\~##~/|\~##~/|\~##~/|\~##~/|\~#
        # پنل سمت چپ (نمودارها)
        plot_layout = QVBoxLayout()
        self.figure, (self.ax_wave, self.ax_spec) = plt.subplots(2, 1, figsize=(6, 6), gridspec_kw={'height_ratios': [1, 2]})
        self.figure.patch.set_facecolor('None')
        self.figure.patch.set_alpha(0.5)
        self.canvas = FigureCanvas(self.figure)
        #self.toolbar = NavigationToolbar2QT(self.canvas, main_widget)
        plot_layout.addWidget(self.canvas)
        #plot_layout.addWidget(self.toolbar)
        main_layout.addLayout(plot_layout, stretch=3)

        #~/|\~##~/|\~##~/|\~##~/|\~##~/|\~##~/|\~##~/|\~##~/|\~##~/|\~#
        # پنل سمت راست (کنترل ها)
        control_layout = QVBoxLayout()

        #~/|\~##~/|\~##~/|\~##~/|\~##~/|\~##~/|\~##~/|\~##~/|\~##~/|\~#
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

        #~/|\~##~/|\~##~/|\~##~/|\~##~/|\~##~/|\~##~/|\~##~/|\~##~/|\~#
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

        #~/|\~##~/|\~##~/|\~##~/|\~##~/|\~##~/|\~##~/|\~##~/|\~##~/|\~#
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

        #~/|\~##~/|\~##~/|\~##~/|\~##~/|\~##~/|\~##~/|\~##~/|\~##~/|\~#
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
        self.spin_max_freq.setRange(100, 11025) # تا سقف 24 کیلوهرتز (برای fs=22050)
        self.spin_max_freq.setValue(8000)       # مقدار پیش‌فرض
        self.spin_max_freq.setSingleStep(500)   # گام‌های 500 هرتزی
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
        #self.btn_narrowband.setStyleSheet("background-color: lightblue;") 
        frame_wideband_mode.addWidget(self.btn_wideband)
        frame_wideband_mode.addWidget(self.btn_narrowband)
        spec_layout.addLayout(frame_wideband_mode)

        control_layout.addWidget(spec_group)
        
        #~/|\~##~/|\~##~/|\~##~/|\~##~/|\~##~/|\~##~/|\~##~/|\~##~/|\~#
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

        #~/|\~##~/|\~##~/|\~##~/|\~##~/|\~##~/|\~##~/|\~##~/|\~##~/|\~#
        # ایجاد دراپ‌داون برای انتخاب تم
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
        
        control_layout.addStretch()
        main_layout.addLayout(control_layout, stretch=1)

        self.reset_plots()

    #~/|\~##~/|\~##~/|\~##~/|\~##~/|\~##~/|\~##~/|\~##~/|\~##~/|\~#
    #~~~##~~~##~~~##~~~##~~~##~~~##~~~##~~~##~~~##~~~##~~~##~~~#
    # --- توابع ضبط و پخش ---
    def audio_callback(self, indata, frames, time, status):
        if self.is_recording:
            self.recorded_chunks.append(indata.copy())

    def start_record(self):
        self.fs = int(self.cb_fs.currentText())
        self.bit_depth = int(self.cb_bits.currentText())
        if self.stream is None:
            self.recorded_chunks = []
            self.stream = sd.InputStream(samplerate=self.fs, channels=1, callback=self.audio_callback)
            self.stream.start()
        self.is_recording = True
        
        #self.btn_new.setEnabled(True)
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
            # --- حالت Play (پخش یا ادامه پخش) ---
            data_to_play = self.audio_data[self.playback_pos:]
            
            # اگر به انتهای فایل رسیده بودیم، از اول پخش کن
            if len(data_to_play) == 0:
                self.playback_pos = 0
                data_to_play = self.audio_data
    
            sd.play(data_to_play, self.fs)
            
            # محاسبه زمان باقی‌مانده به میلی‌ثانیه و شروع تایمرها
            duration_ms = int((len(data_to_play) / self.fs) * 1000)
            self.playback_timer.start(duration_ms)
            self.playback_elapsed_timer.start()
            
            self.is_playing = True
            self.btn_play.setText("⏸ Pause")
            
            # مدیریت دکمه‌ها
            self.btn_record.setEnabled(False)
            self.btn_new.setEnabled(False)
            self.btn_open.setEnabled(False)
            self.btn_save.setEnabled(False)
            self.btn_stop.setEnabled(True)
            
        else:
            # --- حالت Pause (توقف موقت) ---
            sd.stop()
            self.playback_timer.stop()
            
            # محاسبه مقدار دیتای پخش شده و به‌روزرسانی موقعیت
            elapsed_ms = self.playback_elapsed_timer.elapsed()
            frames_played = int((elapsed_ms / 1000.0) * self.fs)
            self.playback_pos += frames_played
            
            # جلوگیری از خطای خروج از محدوده
            if self.playback_pos >= len(self.audio_data):
                self.playback_pos = 0
                
            self.is_playing = False
            self.btn_play.setText("▶ Play")


    def stop_all(self):
        # توقف ضبط
        self.is_recording = False
        if self.stream is not None:
            self.stream.stop()
            self.stream.close()
            self.stream = None
            if self.recorded_chunks:
                self.audio_data = np.concatenate(self.recorded_chunks, axis=0).flatten()
                self.update_info()
                self.update_plots()

        # توقف پخش و تایمرها
        sd.stop() 
        if hasattr(self, 'playback_timer') and self.playback_timer.isActive():
            self.playback_timer.stop()

        # ریست کردن متغیرهای وضعیت پخش
        self.is_playing = False
        self.playback_pos = 0
        self.btn_play.setText("▶ Play")

        # مدیریت دکمه‌ها
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


    #~~~##~~~##~~~##~~~##~~~##~~~##~~~##~~~##~~~##~~~##~~~##~~~#
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

    def open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "باز کردن فایل صوتی", "", "WAV Files (*.wav)")
        if file_name:
            info = sf.info(file_name)
            
            # بررسی و تنظیم FS و Bits
            self.cb_fs.setCurrentText(str(info.samplerate))
            
            # تشخیص 8 یا 16 بیت
            bit_depth = '8' if '8' in info.subtype else '16'
            self.cb_bits.setCurrentText(bit_depth)
            
            # خواندن دیتا
            self.audio_data, self.fs = sf.read(file_name)
            
            # اگر فایل استریو بود، کانال اول را برمی‌داریم
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

    def save_file(self):
        if len(self.audio_data) == 0: return
        file_name, _ = QFileDialog.getSaveFileName(self, "ذخیره فایل صوتی", "", "WAV Files (*.wav)")
        if file_name:
            subtype = 'PCM_16' if self.cb_bits.currentText() == '16' else 'PCM_U8'
            sf.write(file_name, self.audio_data, self.fs, subtype=subtype)

            self.lbl_filename.setText(f"File: {os.path.basename(file_name)}")

    #~~~##~~~##~~~##~~~##~~~##~~~##~~~##~~~##~~~##~~~##~~~##~~~#
    # --- بروزرسانی UI و نمودارها ---
    def update_info(self):
        duration = len(self.audio_data) / self.fs if self.fs > 0 else 0
        self.lbl_duration.setText(f"Duration: {duration:.3f} seconds")
        self.spin_zoom_to.setValue(duration)
        self.spin_zoom_to.setRange(0, duration)
        self.spin_zoom_from.setRange(0, duration)

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
        if len(self.audio_data) == 0: return

        # تنظیم سقف مجاز انتخاب فرکانس بر اساس فرکانس نمونه‌برداری فعلی (قضیه نایکوئیست)
        nyquist_freq = int(self.fs / 2)
        self.spin_max_freq.setMaximum(nyquist_freq)
        
        # اگر کاربر مقداری بیشتر از نایکوئیست وارد کرده بود، اصلاح شود
        if self.spin_max_freq.value() > nyquist_freq:
            self.spin_max_freq.setValue(nyquist_freq)
        
        self.ax_wave.clear()
        self.ax_spec.clear()

        # Waveform
        time_axis = np.linspace(0, len(self.audio_data) / self.fs, num=len(self.audio_data))
        self.ax_wave.plot(time_axis, self.audio_data, color='black', linewidth=0.5)
        self.ax_wave.set_title("Waveform")
        self.ax_wave.set_ylabel("Amplitude")
        self.ax_wave.set_xlim(0, time_axis[-1])

        # Spectrogram
        frame_len_samples = int((self.spin_frame_len.value() / 1000) * self.fs)
        frame_shift_samples = int((self.spin_frame_shift.value() / 1000) * self.fs)
        noverlap = frame_len_samples - frame_shift_samples

        f, t, Sxx = signal.spectrogram(self.audio_data, self.fs, nperseg=frame_len_samples, noverlap=noverlap)
        
        # تبدیل به دسی‌بل برای نمایش بهتر
        Sxx_db = 10 * np.log10(Sxx + 1e-10) 
        
        self.ax_spec.pcolormesh(t, f, Sxx_db, shading='gouraud', cmap='gray_r')
        self.ax_spec.set_title(f"Spectrogram (Frame: {self.spin_frame_len.value()}ms, Shift: {self.spin_frame_shift.value()}ms)")
        self.ax_spec.set_ylabel("Frequency (Hz)")
        self.ax_spec.set_xlabel("Time (s)")
        self.ax_spec.set_xlim(0, time_axis[-1])
        self.ax_spec.set_ylim(0, self.spin_max_freq.value())
        #self.ax_spec.set_ylim(0, self.fs / 2)
        

        self.figure.tight_layout()
        self.canvas.draw()
        
    def set_wideband_values(self):
        # مقادیر استاندارد وایدبند (میلی‌ثانیه)
        self.spin_frame_len.setValue(5)
        self.spin_frame_shift.setValue(2)
        #self.btn_wideband.setStyleSheet("background-color: lightblue;")
        #self.btn_narrowband.setStyleSheet("")
        self.update_plots()
    
    def set_narrowband_values(self):
        # مقادیر استاندارد نروبند (میلی‌ثانیه)
        self.spin_frame_len.setValue(50)
        self.spin_frame_shift.setValue(10)
        #self.btn_narrowband.setStyleSheet("background-color: lightblue;")
        #self.btn_wideband.setStyleSheet("")
        self.update_plots()

    def update_spec_ylim(self):
        """تغییر آنی محدوده فرکانس نمایشی بدون محاسبه مجدد اسپکتروگرام"""
        if len(self.audio_data) == 0: 
            return
        
        # اطمینان از اینکه مقدار از فرکانس نایکوئیست تجاوز نکند
        nyquist_freq = int(self.fs / 2)
        if self.spin_max_freq.value() > nyquist_freq:
            self.spin_max_freq.setValue(nyquist_freq)
            
        self.ax_spec.set_ylim(0, self.spin_max_freq.value())
        self.canvas.draw()
        
    #~~~##~~~##~~~##~~~##~~~##~~~##~~~##~~~##~~~##~~~##~~~##~~~#
    # --- توابع زوم ---
    def apply_zoom(self):
        if len(self.audio_data) == 0: return
        t_start = self.spin_zoom_from.value()
        t_end = self.spin_zoom_to.value()
        if t_start < t_end:
            self.ax_wave.set_xlim(t_start, t_end)
            self.ax_spec.set_xlim(t_start, t_end)
            self.canvas.draw()

    def reset_zoom(self):
        if len(self.audio_data) == 0: return
        max_t = len(self.audio_data) / self.fs
        self.spin_zoom_from.setValue(0)
        self.spin_zoom_to.setValue(max_t)
        self.apply_zoom()

    #~~~##~~~##~~~##~~~##~~~##~~~##~~~##~~~##~~~##~~~##~~~##~~~#
    # --- توابع تم ---
    def change_theme(self, index):
        self.current_theme_index = index
        self.apply_theme()

    def apply_theme(self):
        theme = self.themes[self.current_theme_index]
        
        self.setStyleSheet(theme["qss"])
        
        self.figure.patch.set_facecolor('None')
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

#~~~##~~~##~~~##~~~##~~~##~~~##~~~##~~~##~~~##~~~##~~~##~~~#
#~/|\~##~/|\~##~/|\~##~/|\~##~/|\~##~/|\~##~/|\~##~/|\~##~/|\~#

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = AudioApp()
    ex.show()
    sys.exit(app.exec_())
