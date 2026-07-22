# 🔁 RNN Sequence Predictor GUI (SimpleRNN vs. LSTM vs. GRU)

An interactive **Tkinter desktop application** for comparing three recurrent neural network architectures — **SimpleRNN**, **LSTM**, and **GRU** — on next-value sequence prediction, with live training logs and an overlaid comparison plot.

---

## 📌 Features

* 🖥️ **Interactive GUI:** Built with `tkinter` + `ttk`, embedding a live Matplotlib plot via `FigureCanvasTkAgg`.
* 🔢 **Multiple Sequence Types:** Choose from 6 built-in sequences — Sine (noisy), Arithmetic, Geometric, Fibonacci, Cauchy, and Triangular Number sequences.
* ⚙️ **Configurable Hyperparameters:** Adjust timesteps, epochs, optimizer (`adam`, `sgd`, `rmsprop`), and batch size directly from the UI.
* 🧠 **Three Models Trained Side-by-Side:** `SimpleRNN`, `LSTM`, and `GRU`, each with a single 50-unit recurrent layer + a Dense output layer.
* 📊 **Live Training Console:** Per-epoch loss for each model streamed into the GUI in real time via a custom Keras `Callback`.
* 📈 **Comparison Plot:** True sequence vs. each model's predictions, with checkboxes to toggle individual model curves on/off.
* 🧵 **Responsive UI:** Training runs on a background thread so the interface never freezes.

---

## 🚀 Getting Started

**Prerequisites**

Ensure you have Python 3.8+ installed along with the necessary libraries:

```Bash
pip install numpy matplotlib scikit-learn tensorflow
```

> `tkinter` ships with most standard Python installations. On some Linux distributions you may need to install it separately (e.g. `sudo apt install python3-tk`).

**Running the App**

Clone the repository and run the notebook/script

Or, if exported as a standalone script:

```Bash
python GUI-Pred-Seq-NN.py
```

**Using the GUI**

1. Select a **Sequence** type from the dropdown.
2. Set **Timesteps**, **Epochs**, **Optimizer**, and **Batch Size**.
3. Click **Run Models** to train all three architectures.
4. Watch per-epoch loss stream into the console panel.
5. Compare the **True Sequence**, **Final Loss**, and **Predicted Values** panels.
6. Use the checkboxes below the plot to show/hide each model's prediction curve.

---

## 🛠️ How it Works

**1. Sequence Generation**
A sequence of length 100 is generated based on the selected type (e.g. noisy sine wave, arithmetic/geometric progression, Fibonacci, Cauchy `1/n`, or triangular numbers `n(n+1)/2`).

**2. Preprocessing**
* Values are scaled to `[0, 1]` using `MinMaxScaler`.
* A sliding-window transform converts the sequence into supervised learning samples: each input is a window of `timesteps` past values, and the target is the next value.

**3. Model Architectures**

All three models share the same shape, differing only in their recurrent layer:

| Layer | Units | Notes |
|---|:---:|---|
| Input | `(timesteps, 1)` | — |
| `SimpleRNN` / `LSTM` / `GRU` | 50 | ReLU activation |
| Dense (Output) | 1 | Linear |

Each model is compiled with:
* **Loss:** `mse` (Mean Squared Error)
* **Optimizer:** user-selected (`adam`, `sgd`, or `rmsprop`)

**4. Training & Comparison**
* Each model is trained independently for the chosen number of epochs and batch size.
* A custom `GUICallback` streams `Epoch — Loss` messages into the console panel after every epoch.
* Predictions are inverse-transformed back to the original scale and plotted alongside the true sequence for visual comparison.

---

## 📜 License

Distributed under the MIT License. See LICENSE for more information.
