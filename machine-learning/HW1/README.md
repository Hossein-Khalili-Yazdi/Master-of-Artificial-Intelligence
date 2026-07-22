# 📊 Min-Max Scaling (Data Normalization) in Python

A simple Python script that performs **Min-Max Normalization (Scaling)** on a user-provided dataset. This technique rescales features or numerical values to fit within a specific user-defined target range (e.g., $[0, 1]$ or $[-1, 1]$).

---

## 📌 Features

- **Custom Target Ranges:** Normalizes data from any original range (`old_min`, `old_max`) to any target range (`new_min`, `new_max`).
- **Interactive CLI Input:** Prompts the user to enter 10 numerical values and handles invalid input gracefully.
- **Robust Error Handling:**
  - Prevents **Division by Zero** if all input numbers or bounds are identical.
  - Validates that maximum range values are strictly greater than minimum range values (`max > min`).
  - Catches `ValueError` when non-numeric data is entered.
- **Formatted Output:** Displays side-by-side comparison tables of original vs. transformed numbers formatted to 4 decimal places.

---

## 🧮 Mathematical Formula

The standard formula used for Min-Max Scaling is:

$$X_{\text{scaled}} = \frac{X - \text{old}_\text{min}}{\text{old}_\text{max} - \text{old}_\text{min}} \times (\text{new}_\text{max} - \text{new}_\text{min}) + \text{new}_\text{min}$$

---
🚀 Getting Started
Prerequisites
- Python 3.x installed on your machine.

Running the Script
1. Clone or Download the repository:
```
git clone https://github.com/Hossein-Khalili-Yazdi/Master-of-Artificial-Intelligence/tree/main/machine-learning
cd your-repo-name
```
2.Run the Python script:
```
python min_max_scaler.py
```
💻 Sample Output
```text
برنامه تبدیل اعداد به روش Min-Max Scaling
-----------------------------------------
لطفاً ۱۰ عدد را یکی پس از دیگری وارد کنید:
عدد ۱: 12
...

نتایج تبدیل Min-Max Scaling:
-----------------------------------------
اعداد اصلی: [12.0, 45.0, 67.0, ...]
محدوده فعلی: [0.0, 100.0]
محدوده جدید: [0.0, 1.0]

عدد اصلی: 12.0000     -> عدد تبدیل شده: 0.1200
عدد اصلی: 45.0000     -> عدد تبدیل شده: 0.4500
...
```
📜 License
This project is licensed under the MIT License.
---
