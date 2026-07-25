# 🎵 Audio Analyzer & Recorder (نرم‌افزار تحلیل و ضبط صوت)

A feature-rich desktop application built with **Python**, **PyQt5**, **Matplotlib**, and **SciPy** for real-time audio recording, playback, file processing, and interactive dynamic signal visualization (Waveforms & Spectrograms).

---

## 🌟 Key Features

* **🎙️ Audio Recording & Playback:**
  * Real-time audio recording with dynamic pause/resume support.
  * Custom sampling frequencies (8 kHz to 22.05 kHz) and sample bit depths (8-bit or 16-bit PCM).
  * Non-blocking audio playback controls (Play, Pause, Stop).

* **📊 Advanced Audio Visualization:**
  * **Waveform Display:** Time-domain signal representation.
  * **Spectrogram Analysis:** Real-time STFT calculation converted to logarithmic dB scale.
  * **Preset Modes:** Quick switching between **Wideband** (high temporal resolution) and **Narrowband** (high frequency resolution) configurations.
  * **Dynamic Frequency & Time Zoom:** Precise time-range zooming and interactive upper-bound frequency limit adjustments.

* **🎨 Modern UI & Themes:**
  * Stylish glassmorphic UI design supporting multiple themes (**Light Glass** and **Dark Glass**)[cite: 1].
  * Persian / English bilingual user interface elements[cite: 1].

---

## 🛠️ Requirements & Dependencies

Make sure you have Python 3.8+ installed. The application depends on the following libraries[cite: 1]:

```bash
pip install numpy scipy sounddevice soundfile PyQt5 matplotlib
```

---

## 🚀 Getting Started
1. **Clone the Repository**
```Bash
git clone [https://github.com/your-username/audio-analyzer.git](https://github.com/your-username/audio-analyzer.git)
cd audio-analyzer
```
2. **Run the Application**
```Bash
python main.py
```

---

## 🎛️ How to Use
1. **Record Audio:**
  - Select your desired **Sampling Frequency** and **Bits per sample** from the side panel
  - Click **🔴 Record** to start capturing audio from your default microphone
  - Use **⏸ Pause** or **⏹ Stop** when finished
2. **Open / Save WAV Files:**
  - Click **Open** to load existing 8-bit or 16-bit WAV files
  - Click **Save As** to export your recorded audio
3. **Adjust Spectrogram & Zoom:**
  - Click Wideband or Narrowband to automatically adjust frame parameters
  - Adjust **Frame Length (ms)** and **Frame Shift (ms)** manually for customized STFT settings.
  - Set time bounds in the **Zoom** section and click **Zoom** to inspect fine audio structures.

---

## 📜 License
Distributed under the MIT License. See `LICENSE` for more information.
