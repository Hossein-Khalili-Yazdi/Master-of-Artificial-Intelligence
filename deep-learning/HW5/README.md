# ⛽ Auto-MPG Regression (Neural Network)

A regression project using a **Keras/TensorFlow neural network** to predict a car's fuel efficiency (`mpg`) from its technical specifications.
This project demonstrates a minimal deep learning regression workflow: data cleaning, train/test splitting, feature scaling, model training, and evaluation.

---

## 📌 Features

* ⚙️ **End-to-End Pipeline:** Data cleaning (missing/invalid value removal, type casting) handled with `pandas` and `numpy`.
* 🧠 **Neural Network Regressor:** A `Keras Sequential` model (`64 → 32 → 1`, ReLU activations) trained to predict a continuous target (`mpg`).
* 🚫 **No Data Leakage:** `StandardScaler` is fit only on the training set and applied to the test set separately.
* 📈 **Training Curve Visualization:** Automated Matplotlib plot of training vs. validation loss (MSE) across epochs.
* 🎯 **Multiple Evaluation Metrics:** Model performance reported via MSE, MAE, and RMSE on the held-out test set.

---

## 🚀 Getting Started

**Prerequisites**

Ensure you have Python 3.8+ installed along with the necessary libraries:

```Bash
pip install pandas numpy tensorflow scikit-learn matplotlib
```

**Dataset**

Place `auto-mpg.csv` (the classic [Auto-MPG dataset](https://archive.ics.uci.edu/dataset/9/auto+mpg)) in the same directory as the notebook. The dataset should include a `mpg` target column along with numeric specification columns (e.g., cylinders, displacement, horsepower, weight, acceleration, model year, origin). A `car name` column, if present, is dropped automatically.

**Running the Notebook**

Clone the repository and run the Jupyter Notebook:

```Bash
git clone https://github.com/your-username/auto-mpg-regression.git
cd auto-mpg-regression
jupyter notebook Regression.ipynb
```

---

## 🛠️ How it Works

**1. Data Cleaning**
* The `car name` column is dropped (not a useful numeric feature).
* Missing/invalid values represented as `'?'` are converted to `NaN` and any rows containing them are dropped.
* All remaining columns are cast to `float`.

**2. Feature/Target Split & Scaling**
* `mpg` is used as the regression target; all other columns are used as features.
* Data is split 80/20 into training and test sets (`random_state=42` for reproducibility).
* `StandardScaler` standardizes features (zero mean, unit variance), fit only on training data to avoid data leakage.

**3. Model Architecture**

| Layer | Units | Activation |
|---|:---:|:---:|
| Input | # of features | — |
| Dense | 64 | ReLU |
| Dense | 32 | ReLU |
| Dense (Output) | 1 | Linear |

The model is compiled with:
* **Loss:** `mse` (Mean Squared Error)
* **Optimizer:** `adam`
* **Metrics:** `mae` (Mean Absolute Error), `rmse` (Root Mean Squared Error)

**4. Training & Evaluation**
* Trained for 100 epochs, batch size 32, with a 20% validation split.
* Final performance (loss/MAE/RMSE) is measured on the held-out test set, and training/validation loss curves are plotted to check for overfitting.

---

## 📜 License

Distributed under the MIT License. See LICENSE for more information.
