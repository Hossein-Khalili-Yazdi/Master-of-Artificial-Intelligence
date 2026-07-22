# 🧠 CNN Model Evaluation & Benchmarking Workstation

A desktop application built with **PyQt5**, **TensorFlow/Keras**, and **Matplotlib** for training, evaluating, fine-tuning, and visualizing Convolutional Neural Networks (CNNs) on the **CIFAR-10** dataset.

This tool allows you to select custom or pre-trained architectures, load local weight checkpoints, fine-tune models over customizable epochs, and inspect evaluation metrics (Accuracy, Loss, Confusion Matrix, Classification Report, and sample predictions) in real time.

---

## ✨ Features

* **Multi-Architecture Support**:
  * Custom CNN built from scratch.
  * Pre-trained Transfer Learning Models: **VGG16**, **VGG19**, **InceptionV3**, **ResNet50**, **EfficientNetB0**, **MobileNetV2**.
  * Multi-branch **Hybrid Ensemble** model combining features from VGG16 and InceptionV3.
* **Automated Dataset Management**:
  * Auto-downloads and extracts the **CIFAR-10** dataset if not present locally.
* **Custom Weights Loading**:
  * Auto-detects local `.weights.h5` and `.h5` files in the project root directory.
  * Allows loading pre-trained weights with dynamic shape matching.
* **Interactive Desktop GUI**:
  * Built using **PyQt5** with multi-threading (`QThread`) to keep the UI responsive during training and evaluation.
  * Real-time training progress and epoch logging.
* **Rich Visualizations & Metrics**:
  * Epoch-by-epoch Accuracy/Loss curves.
  * Heatmap confusion matrix via **Seaborn**.
  * Sample image prediction grid with visual indicators for correct (green) and incorrect (red) classifications.
  * Detailed classification report containing Precision, Recall, and F1-Score per class.

---

## 🛠️ Requirements & Installation

### Prerequisites

* **Python**: `3.10` or higher (tested on Python 3.12)
* **OS**: Windows, macOS, or Linux

### Dependencies

Install all required packages using `pip`:

```bash
pip install tensorflow numpy matplotlib seaborn pyqt5 scikit-learn
```
## 🚀 Usage
1. **Clone the Repository**
   
2. **Run the Application**

3. **Workflow:**
    * Select Model: Choose an architecture from the drop-down menu (e.g., Custom CNN, VGG16, ResNet50, Hybrid Ensemble).
    * Select Weight (Optional): Choose a local .weights.h5 file if available, or keep it as None to start fresh/use ImageNet weights.
    * Select Epochs: Choose the desired training duration (e.g., 1, 3, 5, 10, etc.).
    * Start Process: Click 🚀 Compile, Train & Evaluate to start execution.

---

## 🏗️ Supported Architectures

| Model | Input Shape | Upsampling | Pre-trained Weights |
| :--- | :---: | :---: | :---: |
| **Custom CNN** | $32 \times 32 \times 3$ | ❌ | Trained from Scratch |
| **VGG16** | $32 \times 32 \times 3$ | ❌ | ImageNet |
| **VGG19** | $32 \times 32 \times 3$ | ❌ | ImageNet |
| **InceptionV3** | $75 \times 75 \times 3$ | ✅ | ImageNet |
| **ResNet50** | $32 \times 32 \times 3$ | ✅ | ImageNet |
| **EfficientNetB0** | $32 \times 32 \times 3$ | ❌ | ImageNet |
| **MobileNetV2** | $32 \times 32 \times 3$ | ❌ | ImageNet |
| **Hybrid Ensemble** | $32 \times 32 \times 3$ | ✅ (Internal) | VGG16 + InceptionV3 |

---

## 🏷️ Dataset
This project utilizes the CIFAR-10 dataset, which consists of 60,000 $32 \times 32$ color images across 10 distinct categories:
  * Airplane, Automobile, Bird, Cat, Deer, Dog, Frog, Horse, Ship, Truck.
