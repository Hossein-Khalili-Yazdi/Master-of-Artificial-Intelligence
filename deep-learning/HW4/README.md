# 🚢 Titanic Survival Classifier (Neural Network)

A binary classification project using a **Keras/TensorFlow neural network** to predict passenger survival on the Titanic.
This project demonstrates a complete, minimal deep learning workflow: data preprocessing, train/test splitting, feature scaling, model training, and evaluation.

---

## 📌 Features

* ⚙️ **End-to-End Pipeline:** Missing value imputation, categorical encoding, and feature scaling handled with `pandas` and `scikit-learn`.
* 🧠 **Neural Network Classifier:** A `Keras Sequential` model (`16 → 8 → 1`, ReLU + Sigmoid) trained for binary classification.
* 🚫 **No Data Leakage:** `StandardScaler` is fit only on the training set and applied to the test set separately.
* 📈 **Training Curve Visualization:** Automated Matplotlib plot of training vs. validation loss across epochs.
* 🎯 **Accuracy Verification:** Final model evaluated on a held-out test set.

---

## 📊 Results & Output

Below are the results from training the model for 50 epochs on the Titanic dataset:

### 1. Training Progress
```text
شروع آموزش مدل...
Epoch 1/50  -> loss: 0.7035, val_loss: 0.6793
Epoch 25/50 -> loss: 0.4094, val_loss: 0.4061
Epoch 50/50 -> loss: 0.3928, val_loss: 0.4083
```

### 2. Final Evaluation
```text
ارزیابی مدل روی داده‌های تست:
Accuracy: 81.56%
Loss: 0.4287

Final training accuracy:   84.53%
Final validation accuracy: 82.52%
----------------------------------------
```

### 3. Dataset Summary
```text
Total rows: 891 | Train rows: 712 | Test rows: 179
Overall survival rate: 38.4%
```

> Note: Results may vary slightly depending on TensorFlow version, random initialization, and hardware.

---

## 🚀 Getting Started

**Prerequisites**

Ensure you have Python 3.8+ installed along with the necessary libraries:

```Bash
pip install pandas numpy tensorflow scikit-learn matplotlib
```

**Dataset**

Place `titanic.csv` (the classic [Titanic dataset](https://www.kaggle.com/c/titanic/data)) in the same directory as the notebook. Expected columns include `Pclass`, `Sex`, `Age`, `SibSp`, `Parch`, `Fare`, and `Survived`.

**Running the Notebook**

Clone the repository and run the Jupyter Notebook

---

## 🛠️ How it Works

**1. Preprocessing**
* Missing `Age` and `Fare` values are filled with the column median.
* The categorical `Sex` column is mapped to numeric values (`male → 0`, `female → 1`).
* Features used: `Pclass`, `Sex`, `Age`, `SibSp`, `Parch`, `Fare`.

**2. Train/Test Split & Scaling**
* Data is split 80/20 into training and test sets (`random_state=42` for reproducibility).
* `StandardScaler` standardizes features (zero mean, unit variance), fit only on training data to avoid data leakage.

**3. Model Architecture**

| Layer | Units | Activation |
|---|:---:|:---:|
| Input | 6 (features) | — |
| Dense | 16 | ReLU |
| Dense | 8 | ReLU |
| Dense (Output) | 1 | Sigmoid |

The model is compiled with:
* **Loss:** `binary_crossentropy`
* **Optimizer:** `adam`
* **Metric:** `accuracy`

**4. Training & Evaluation**
* Trained for 50 epochs, batch size 32, with a 20% validation split.
* Final performance is measured on the held-out test set, and training/validation loss curves are plotted to check for overfitting.

---

## 📜 License

Distributed under the MIT License. See LICENSE for more information.
