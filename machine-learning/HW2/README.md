# 🔬 Breast Cancer Diagnosis using Decision Tree Classification

This project performs exploratory data analysis (EDA) and builds a machine learning pipeline using a **Decision Tree Classifier** to classify breast cancer tumors as either **Benign** or **Malignant** based on clinical feature measurements.

---

## 📊 Dataset Overview

The dataset used in this project is the **Wisconsin Diagnostic Breast Cancer (WDBC)** (`data.csv`), which consists of **569 instances** and **32 attributes**:

* **Total Samples:** 569 rows
* **Target Feature (`target`):**
  * `B` (Benign) — ~62.7%
  * `M` (Malignant) — ~37.3%
* **Feature Characteristics:** Computed from a digitized image of a fine needle aspirate (FNA) of a breast mass. Features represent morphological properties of cell nuclei, including `radius`, `texture`, `perimeter`, `area`, `smoothness`, `symmetry`, etc., measured by Mean, Standard Error (SE), and Worst value.

---

## 🛠️ Requirements & Installation

To run this notebook, ensure you have Python 3.8+ installed along with the following libraries:

```bash
pip install scikit-learn pandas numpy matplotlib seaborn graphviz
```
**Core Libraries:**
 - Pandas & NumPy: Data manipulation, cleaning, and matrix operations.
 - Matplotlib & Seaborn: Data visualization and Exploratory Data Analysis (EDA).
 - Scikit-Learn: Data preprocessing, Decision Tree modeling, evaluation metrics (Confusion Matrix, ROC-AUC), and hyperparameter tuning (GridSearchCV).

## 🚀 Project Workflow
1. Exploratory Data Analysis (EDA):
   - Inspecting dataset structure (shape, info, describe).
   - Analyzing target class balance (M vs. B).
   - Checking for missing/null values.
2. Data Preprocessing:
   - Dropping unnecessary columns (e.g., Unnamed: 32 and id).
   - Renaming the target column diagnosis to target.
3. Modeling & Evaluation:
   - Training a DecisionTreeClassifier.
   - Evaluating performance using Accuracy, Precision, Recall, F1-Score, and ROC-AUC.
   - Visualizing the Decision Tree diagram and Confusion Matrix.

## 💻 How to Run
 1. Place the data.csv file in the same directory as the Jupyter notebook.
 2. Launch the notebook and execute the cells sequentially:
```bash
jupyter notebook
```
## 📄 License
This project is open-source and available for educational and research purposes.
