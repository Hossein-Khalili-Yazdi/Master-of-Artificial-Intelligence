# 🎵 Audio Analysis and Recording Software (نرم‌افزار تحلیل و ضبط صوت)

A comprehensive GUI application built with **PyQt5**, **SciPy**, and **Matplotlib** for real-time audio recording, playback, waveform visualization, spectrogram analysis, and advanced digital speech processing.

---

## 🌟 Key Features

### 🎙️ Audio Recording & Playback
* **Real-Time Recording:** Record audio dynamically with options to pause and stop.
* **Flexible Audio Settings:** Configurable sampling frequencies ($8000\text{ Hz}$ to $22050\text{ Hz}$) and bit depths ($8$-bit and $16$-bit).
* **File Management:** Open and save audio files in `.wav` format effortlessly.

### 📊 Real-Time Signal Visualization
* **Dual View:** Simultaneous waveform display and dynamic Spectrogram generation.
* **Wideband vs. Narrowband Modes:** Quick presets to toggle between time resolution (Wideband) and frequency resolution (Narrowband)[cite: 2].
* **Interactive Zooming:** Precision time-frame zooming (`From` / `To` in seconds) to inspect specific parts of the audio[cite: 2].
* **Custom UI Themes:** Switch between **Light Glass** and **Dark Glass** visual modes seamlessly[cite: 2].

### 🔬 Advanced Speech Processing & Frame Analysis
* **Frame Extraction:** Dynamic frame length ($N$) and shift ($M$) selection with auto-calculated frame limits[cite: 2].
* **Windowing & Pre-emphasis:** Apply Rectangular, Hamming, or Hanning windows alongside adaptive pre-emphasis filters[cite: 2].
* **Time-to-Frame Converter:** Automatically locate and jump to the frame corresponding to a given timestamp[cite: 2].
* **Acoustic Feature Extraction:**
  * **Energy & ZCR:** Frame-by-frame Energy ($E = \sum x[n]^2$) and Zero-Crossing Rate calculation[cite: 2].
  * **Autocorrelation Analysis:** Secondary peak estimation for pitch extraction[cite: 2].
  * **AMDF (Average Magnitude Difference Function):** Valley estimation for fundamental pitch period estimation[cite: 2].
  * **Formant Analysis:** Spectral envelope smoothing and identification of vocal tract resonance peaks ($F1, F2, F3$, etc.)[cite: 2].
  * **Cepstral Analysis:** Homomorphic speech processing for pitch estimation in the Quefrency domain[cite: 2].
  * **Voiced/Unvoiced Comparison:** Dynamic search and comparison of adjacent Voiced and Unvoiced speech frames[cite: 2].
  * **200-Frame Pitch Comparison:** Side-by-side pitch tracking comparison across 200 consecutive frames using both Autocorrelation and Cepstral methods[cite: 2].

---

## 🛠️ Prerequisites & Requirements

Ensure you have Python 3.8+ installed. Install all required dependencies via `pip`:

```bash
pip install numpy scipy matplotlib sounddevice soundfile PyQt5
```
---

**Note on Audio Drivers:** `sounddevice` depends on PortAudio. Most operating systems handle this automatically, but Linux users may need:
```Bash
sudo apt-get install libportaudio2
```

---

## 🚀 How to Run
1. **Clone the repository:**
```Bash
git clone [https://github.com/your-username/audio-analysis-gui.git](https://github.com/your-username/audio-analysis-gui.git)
cd audio-analysis-gui
```
2. **Execute the application:**
```Bash
python HW4.py
```

---

## 📖 Usage Guide
1. **Record or Load Audio:**
  - Click **🔴 Record** to record live audio from your microphone, or click **Open** to load an existing `.wav` file.
2. **Adjust Spectrogram Parameters:**
  - Set frame lengths or click **Wideband / Narrowband** for predefined analysis setups.
3. **Analyze Specific Frames:**
  - Enter values for $N$ and $M$ under the **Frame & Features** section, pick a frame index, and click نمایش فریم روی نمودار to highlight it on the waveform.
4. **Run Advanced Algorithms:**
  - Use the dedicated feature buttons to inspect Energy/ZCR, Autocorrelation, AMDF, Formants, Cepstrum, and Pitch Tracking comparisons

--- 

## 📜 License
Distributed under the MIT License. See `LICENSE` for more information.
