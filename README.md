# 🫀 Clinical Risk Prediction System

Developed as part of a Bioengineering + Machine Learning project focusing on clinically reliable prediction systems.

A machine learning-based **clinical decision support system** for predicting cardiovascular disease risk using patient clinical data.

---

## 🚨 Problem Statement

Early detection of heart disease is critical.
In clinical settings, **missing a positive case (false negative)** can lead to severe consequences.

This project focuses on:

* **Maximizing recall** (reducing missed diagnoses)
* Providing **reliable probability estimates** for decision-making

---

## 🧠 Approach

* Model: **Calibrated Logistic Regression**
* Threshold tuning: **0.3 (recall-focused decision boundary)**
* Calibration: Ensures predicted probabilities reflect real-world likelihood
* Evaluation:

  * ROC-AUC
  * Precision-Recall Curve
  * Confusion Matrix
  * Cross-validation

---

## ⚖️ Key Design Decisions

### 1. Logistic Regression over Random Forest

Although Random Forest achieved near-perfect performance, it showed signs of **overfitting** due to dataset size.

Logistic Regression was chosen because:

* Better **generalization**
* **Interpretability** (important in healthcare)
* Supports **calibrated probabilities**

---

### 2. Threshold = 0.3 (instead of default 0.5)

* Improves **recall**
* Reduces **false negatives**
* Aligns with clinical priority of **early detection**

---

### 3. Calibration

Used `CalibratedClassifierCV` to ensure:

* Probability outputs are **trustworthy**
* Model can support **risk-based decision making**

---

## 📊 Results

* ROC-AUC: ~0.93
* Improved recall using threshold tuning
* Reliable probability estimates after calibration

---

## 💡 Features

* Risk stratification:

  * Low Risk (< 0.3)
  * Medium Risk (0.3 – 0.6)
  * High Risk (> 0.6)
* Clinical interpretation of predictions
* Recommendation system based on risk level
* Interactive Streamlit web application

---

## 🖥️ Demo

### High Risk Prediction

![High Risk](your-image-name.png)

---

## ⚠️ Limitations

* Dataset is relatively small
* Categorical variables treated as ordinal
* No external clinical validation

---

## 🔮 Future Improvements

* SHAP-based explainability
* Proper categorical encoding (OneHotEncoder)
* Validation on real-world clinical datasets

---

## 🛠️ Tech Stack

* Python
* scikit-learn
* pandas, numpy
* matplotlib, seaborn
* Streamlit (for deployment)
* joblib (model serialization)

---

## ⚠️ Disclaimer

This project is for educational purposes and is **not a substitute for medical diagnosis**.
