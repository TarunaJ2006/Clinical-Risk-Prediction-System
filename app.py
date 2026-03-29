import streamlit as st
import pandas as pd
import joblib

st.markdown("""
<style>
div.stButton > button:first-child {
    background-color: #2563eb;
    color: white;
    border-radius: 8px;
    height: 3em;
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

# PAGE CONFIG
st.set_page_config(
    page_title="Clinical Risk Prediction",
    page_icon="🫀",
    layout="wide"
)

# LOAD MODEL
model = joblib.load("model.pkl")
columns = joblib.load("columns.pkl")

# SIDEBAR
st.sidebar.title("🫀 About")
st.sidebar.info("""
Clinical Risk Prediction App
                
• Threshold: 0.3 (recall-focused decision boundary)
• Model: Calibrated Logistic Regression  
• Reason: Interpretable and reliable probability estimates
• Goal: Early disease detection  

⚠️ Not a medical diagnosis tool
""")

st.sidebar.markdown("### Key Clinical Drivers")
st.sidebar.write("""
• Chest Pain Type  
• ST Depression  
• Major Vessels (CA)  
• Exercise-induced Angina  
""")

# MAIN CENTERED LAYOUT 
left, center, right = st.columns([1.5, 2, 1.5])

with center:

    # TITLE 
    st.markdown(
        "<h1 style='text-align:center;'>🫀 Clinical Risk Prediction System</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<p style='text-align:center; color:gray;'>Predicting cardiovascular risk using clinical patient data</p>",
        unsafe_allow_html=True
    )

    st.write("")

    # INPUT SECTION
    st.markdown("## Patient Details")

    col1, col2 = st.columns(2)

    with col1:
        age = st.slider(
            "Age (years)", 20, 80, 50,
            help="Higher age increases cardiovascular risk"
        )

        sex = st.selectbox(
            "Sex", [0, 1],
            help="0 = Female, 1 = Male"
        )

        cp = st.selectbox(
            "Chest Pain Type", [0,1,2,3],
            help="0: Typical | 1: Atypical | 2: Non-anginal | 3: Asymptomatic (higher risk)"
        )

        trestbps = st.slider(
            "Resting Blood Pressure (mm Hg)", 80, 200, 120,
            help="High BP (>140) increases risk"
        )

        chol = st.slider(
            "Cholesterol (mg/dl)", 100, 600, 200,
            help=">240 is considered high"
        )

        fbs = st.selectbox(
            "Fasting Blood Sugar > 120", [0,1],
            help="1 indicates diabetes risk"
        )

    with col2:
        restecg = st.selectbox(
            "Rest ECG", [0,1,2],
            help="0: Normal | 1: ST-T abnormality | 2: Hypertrophy"
        )

        thalach = st.slider(
            "Max Heart Rate", 70, 210, 150,
            help="Lower values may indicate heart issues"
        )

        exang = st.selectbox(
            "Exercise Induced Angina", [0,1],
            help="1 = Chest pain during exercise"
        )

        oldpeak = st.slider(
            "ST Depression", 0.0, 6.5, 1.0,
            help="Higher = more heart stress"
        )

        slope = st.selectbox(
            "Slope of ST Segment", [0,1,2],
            help="0: Upsloping | 1: Flat | 2: Downsloping (worse)"
        )

        ca = st.selectbox(
            "Number of Major Vessels", [0,1,2,3,4],
            help="Higher value = more blockage"
        )

        thal = st.selectbox(
            "Thalassemia", [0,1,2,3],
            help="2 indicates reversible defect (high risk)"
        )

    # CENTERED BUTTON
    colb1, colb2, colb3 = st.columns([1,1,1])
    with colb2:
        predict_btn = st.button("🔍 Analyze Patient Risk", type="primary")

    # PREDICTION
    if predict_btn:

        input_df = pd.DataFrame([[ 
            age, sex, cp, trestbps, chol, fbs,
            restecg, thalach, exang, oldpeak,
            slope, ca, thal
        ]], columns=columns)

        input_df = input_df[columns]

        prob = model.predict_proba(input_df)[0][1]
        threshold = 0.3  # from notebook (recall-focused)
        prediction = int(prob >= threshold)
        st.caption("⚙️ Threshold adjusted (0.3) to prioritize recall and reduce missed diagnoses")

        # RISK LEVEL
        if prob < 0.3:
            risk, color = "Low Risk", "#16a34a"
        elif prob < 0.6:
            risk, color = "Medium Risk", "#f59e0b"
        else:
            risk, color = "High Risk", "#dc2626"

        # OUTPUT
        st.markdown("## Prediction Result")

        st.metric("Disease Probability", f"{prob*100:.2f}%")
        st.caption("📊 Probability is calibrated (reflects real-world likelihood)")
        st.progress(float(prob))

        st.markdown(
            f"<h2 style='color:{color}; text-align:center;'>Risk Level: {risk}</h2>",
            unsafe_allow_html=True
        )

        if prediction == 1:
            st.error("⚠️ Model indicates presence of heart disease")
        else:
            st.success("✅ Model indicates low likelihood of heart disease")

        # INTERPRETATION
        st.markdown("### 🧠 Clinical Interpretation")

        if prob > 0.6:
            st.warning("High risk detected based on multiple clinical indicators.")
        elif prob > 0.3:
            st.info("Moderate risk — follow-up recommended.")
        else:
            st.success("Low risk — no major warning signs detected.")

        # WHY THIS PREDICTION
        st.markdown("### 🔍 Why this prediction?")
        st.caption("⚠️ Based on clinical heuristics (not direct model explanation)")

        reasons = []

        if cp >= 2:
            reasons.append("Risky chest pain pattern")

        if exang == 1:
            reasons.append("Exercise-induced angina present")

        if oldpeak > 1:
            reasons.append("High ST depression")

        if ca >= 2:
            reasons.append("Multiple vessel blockage")

        if thalach < 120:
            reasons.append("Low maximum heart rate")

        if chol > 240:
            reasons.append("High cholesterol")

        if not reasons:
            if prob > 0.6:
                reasons.append("Multiple moderate-risk clinical features collectively contribute to elevated risk")
            else:
                reasons.append("No strong high-risk indicators")

        for r in reasons:
            st.write(f"• {r}")

        # RECOMMENDATION
        st.markdown("### 📋 Recommendation")

        if prob > 0.6:
            st.error("Immediate cardiology consultation recommended.")
        elif prob > 0.3:
            st.warning("Lifestyle changes and monitoring advised.")
        else:
            st.success("Maintain a healthy lifestyle.")

        # DISCLAIMER
        st.caption("⚠️ This is a machine learning prediction and not a medical diagnosis.")