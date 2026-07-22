# 📊 Multi-Dataset Machine Learning Classifier Benchmark 🤖📊

A Python-based benchmarking framework to evaluate and compare the performance of popular Machine Learning classification algorithms across various standard datasets using `scikit-learn`.

---

## 📋 Table of Contents
- [Overview](#overview)
- [Datasets Included](#datasets-included)
- [Algorithms Tested](#algorithms-tested)
- [Evaluation Metrics](#evaluation-metrics)
- [Features](#features)
- [Installation & Requirements](#installation--requirements)
- [How to Run](#how-to-run)
- [Benchmark Results](#benchmark-results)
- [License](#license)

---

## 🔍 Overview

This project provides a comparative analysis of three fundamental Machine Learning classifiers across five benchmark datasets. It automatically handles data preprocessing, model training, evaluation, tie-breaker detection, and outputs color-coded performance summaries right in your terminal.

---

## 📁 Datasets Included

The benchmark uses the following datasets provided by `scikit-learn`:

| Dataset | Task Type | Classes / Target |
| :--- | :--- | :--- |
| **Breast Cancer** | Binary Classification | Malignant / Benign |
| **Wine** | Multi-class Classification | 3 Wine Classes |
| **Iris** | Multi-class Classification | 3 Plant Species |
| **Digits** | Multi-class Classification | 10 Handwritten Digits (0–9) |
| **Diabetes** | Binary Classification (Derived)* | Above/Below Median Progression |

> *\*Note: The continuous target of the Diabetes dataset is binarized at the median value to allow classification benchmarking.*

---

## 🤖 Algorithms Tested

1. **K-Nearest Neighbors (KNN)** (`n_neighbors=5`)
2. **Gaussian Naive Bayes** (`GaussianNB`)
3. **Decision Tree Classifier** (`max_depth=10`, `random_state=42`)

---

## 📐 Evaluation Metrics

Each model is evaluated on test split data (80/20 train-test ratio) using the following metrics:
- **Accuracy**
- **Precision** (Macro-averaged)
- **Recall** (Macro-averaged)
- **F1-Score** (Macro-averaged)

---

## ✨ Features

* **Automated Data Preprocessing**: Standardizes features using `StandardScaler` and handles stratified train/test splitting.
* **Tie-Breaker Detection**: Automatically detects when two or more models achieve identical top scores (within $10^{-9}$ floating-point precision) and reports joint winners.
* **ANSI Color-Coded Console Output**:
  * 🟦 **Blue**: KNN Victory
  * 🟩 **Green**: Naive Bayes Victory
  * 🟥 **Red**: Decision Tree Victory
  * 🩵 **Cyan**: Draw / Joint Victory
* **Visualization Ready**: Configured with custom chart palettes using `matplotlib` and `seaborn`.

---

## ⚙️ Installation & Requirements

Ensure you have Python 3.8+ installed. Clone this repository and install the required dependencies:

```bash
git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
cd your-repo-name
pip install pandas numpy matplotlib seaborn scikit-learn
```

## 🚀 How to Run
Execute the main script or open the Jupyter Notebook:
```bash
python main.py
```
or run the notebook inside Jupyter Lab / VS Code:

```bash
jupyter lab benchmark_notebook.ipynb
```
## 📊 Benchmark Results

Here is an overview of the winning models by evaluation metric based on the automated benchmark output:

## 🏆 Winners Summary

| Dataset | Winner (Accuracy) | Winner (Precision) | Winner (Recall) | Winner (F1-Score) |
| :--- | :--- | :--- | :--- | :--- |
| **Breast Cancer** | 🟦 KNN (0.9561) | 🟦 KNN (0.9551) | 🟦 KNN (0.9504) | 🟦 KNN (0.9526) |
| **Wine** | 🩵 KNN & Naive Bayes (0.9722) | 🟩 Naive Bayes (0.9744) | 🩵 KNN & Naive Bayes (0.9762) | 🟩 Naive Bayes (0.9743) |
| **Iris** | 🟩 Naive Bayes (0.9667) | 🟩 Naive Bayes (0.9697) | 🟩 Naive Bayes (0.9667) | 🟩 Naive Bayes (0.9666) |
| **Digits** | 🟦 KNN (0.9639) | 🟦 KNN (0.9646) | 🟦 KNN (0.9637) | 🟦 KNN (0.9634) |
| **Diabetes** | 🟦 KNN (0.7528) | 🟦 KNN (0.7528) | 🟦 KNN (0.7528) | 🟦 KNN (0.7528) |

## 📜 License
This project is open-source and available under the MIT License.

