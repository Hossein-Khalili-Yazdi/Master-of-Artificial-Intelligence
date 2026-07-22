# 📊 Machine Learning Projects 🤖

Welcome to the **Machine Learning** repository folder! This directory contains a collection of practical exercises, classifier benchmarks, data preprocessing techniques, and unsupervised/supervised algorithm implementations using Python and `scikit-learn`.

---

## 📁 Repository Structure & Projects

Here is an overview of the projects included in this folder:

```text
machine-learning/
├── Min-Max Scaling (Data Normalization) in Python/
├── Breast Cancer Diagnosis using Decision Tree Classification/
├── Breast Cancer Diagnosis using Decision Tree Classification (K-Means)/
└── Multi-Dataset Machine Learning Classifier Benchmark/
```

## 📑 Project Details
1. 📏 Min-Max Scaling (Data Normalization) in Python
   - Focus: Data Preprocessing & Feature Engineering
   - Description: Demonstrates feature scaling and data normalization techniques using Min-Max Scaling to transform feature values into a bounded range (typically $[0, 1]$). It highlights the importance of feature scaling for distance-based algorithms and feature consistency.
2. 🌲 Breast Cancer Diagnosis using Decision Tree Classification
   - Focus: Supervised Learning / Binary Classification
   - Description: Implements a Decision Tree classifier on the UCI/scikit-learn Breast Cancer Wisconsin dataset to predict whether a tumor is malignant or benign. Includes model evaluation, feature importance analysis, and performance metrics.
3. 🔍 Breast Cancer Diagnosis using Decision Tree Classification (K-Means)
   - Focus: Unsupervised & Supervised Learning Integration
   - Description: Explores tumor diagnosis by combining K-Means clustering with Decision Tree classification. Analyzes how unsupervised cluster assignments can assist feature representation or pre-labeling before applying supervised classification trees.
4. 🏆 Multi-Dataset Machine Learning Classifier Benchmark
   - Focus: Model Comparison & Benchmarking Framework
   - Description: A comprehensive benchmarking suite comparing multiple classification algorithms across 5 standard datasets (Breast Cancer, Wine, Iris, Digits, Diabetes).
   - Models Evaluated: K-Nearest Neighbors (KNN), Gaussian Naive Bayes, Decision Tree Classifier.
   - Features: Automated preprocessing, tie-breaker detection, multi-metric output (Accuracy, Precision, Recall, F1-Score), and console metric visualizers.
## ⚙️ Prerequisites & Dependencies
To run the notebooks or scripts in these directories, install the necessary dependencies:
```
pip install numpy pandas scikit-learn matplotlib seaborn
```
## 🚀 Getting Started
1. Clone the main repository:

```Bash
git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
```
2. Navigate to the machine-learning directory:

```Bash
cd machine-learning
```
3. Explore any subfolder and launch Jupyter Notebook or Python scripts:

```Bash
jupyter lab
```

## 📜 License
This collection is open-source and available under the MIT License.
