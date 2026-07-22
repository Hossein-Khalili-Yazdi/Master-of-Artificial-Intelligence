# Hebbian Learning Neural Network for Logic Gates (AND & OR)

This repository contains an implementation of the **Hebbian Learning Rule** applied to fundamental digital logic gates (**AND** and **OR**). The project demonstrates how a simple unsupervised learning algorithm can adjust weights and bias to correctly classify linearly separable binary patterns.

---

## 📋 Table of Contents
- [Overview](#-overview)
- [Hebbian Learning Concept](#-hebbian-learning-concept)
- [Results](#-results)
  - [AND Gate](#1-and-gate)
  - [OR Gate](#2-or-gate)
- [Installation & Setup](#-installation--setup)
- [Usage](#-usage)
- [License](#-license)

---

## 💡 Overview

The **Hebbs Rule** (often summarized as *"cells that fire together, wire together"*) is one of the oldest and simplest neural network learning algorithms. In this project:
* Bipolar inputs and targets ($1$ and $-1$) are used.
* The network learns the decision boundary for **AND** and **OR** operations.
* Output graphs visually depict the learned decision boundary separating the target classes.

---

## 🧠 Hebbian Learning Concept

For a given training sample with input vector $\vec{x} = [x_1, x_2, \dots, x_n]$ and target output $y$:

1. **Activation:** Input units receive input signals.
2. **Weight Update Rule:**
   
$$\Delta w_i = x_i \cdot y$$
   
$$w_i^{(\text{new})} = w_i^{(\text{old})} + \Delta w_i$$
   
4. **Bias Update Rule:**

$$\Delta b = y$$
   
$$b^{(\text{new})} = b^{(\text{old})} + \Delta b$$

---

## 📊 Results

### 1. AND Gate
* **Final Weights & Bias:**
  * $\text{Bias } (w_0) = -2.0$
  * $w_1 = 2.0$
  * $w_2 = 2.0$

| Input $(x_1, x_2)$ | Target ($y$) | Prediction | Status |
| :---: | :---: | :---: | :---: |
| `[ 1,  1]` | $1$ | $1$ | Correct (✓) |
| `[ 1, -1]` | $-1$ | $-1$ | Correct (✓) |
| `[-1,  1]` | $-1$ | $-1$ | Correct (✓) |
| `[-1, -1]` | $-1$ | $-1$ | Correct (✓) |

---

### 2. OR Gate
* **Final Weights & Bias:**
  * $\text{Bias } (w_0) = 2.0$
  * $w_1 = 2.0$
  * $w_2 = 2.0$

| Input $(x_1, x_2)$ | Target ($y$) | Prediction | Status |
| :---: | :---: | :---: | :---: |
| `[ 1,  1]` | $1$ | $1$ | Correct (✓) |
| `[ 1, -1]` | $1$ | $1$ | Correct (✓) |
| `[-1,  1]` | $1$ | $1$ | Correct (✓) |
| `[-1, -1]` | $-1$ | $-1$ | Correct (✓) |

---

## 🛠 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/your-username/hebbian-learning-logic-gates.git](https://github.com/your-username/hebbian-learning-logic-gates.git)
   cd hebbian-learning-logic-gates
   ```
2. **Install required dependencies:**
   ```bash
    pip install numpy matplotlib jupyter
   ```
## 🚀 Usage

Open and run the Jupyter Notebook:
   ```bash
    jupyter notebook
   ```
Select the main notebook file (`.ipynb`) and execute all cells sequentially to view the training output, evaluation metrics, and decision boundary plots.

## 📜 License
Distributed under the MIT License. See LICENSE for more information.
