import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
from io import StringIO

st.set_page_config(page_title="Big vs Small Predictor", layout="centered")
st.title("🎲 Big vs Small Predictor")

# Session setup
if 'history' not in st.session_state:
    st.session_state['history'] = []

# --- Prediction Logic ---
def predict_big_small(numbers, mode):
    avg = np.mean(numbers)
    variance = np.std(numbers)

    if mode == "Aggressive":
        threshold = 4.0
    elif mode == "Cautious":
        threshold = 5.0
    else:
        threshold = 4.5

    pred = "Big" if avg >= threshold else "Small"
    confidence = round(100 - variance * 10, 1)
    confidence = max(50, min(confidence, 99))
    return pred, confidence

# --- User Inputs ---
with st.form("prediction_form"):
    st.subheader("📥 Enter last 5 results (digits 0 to 9):")
    nums = []
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            num = st.number_input(f"Result {i+1}", min_value=0, max_value=9, value=0, step=1, key=f"num_{i}")
            nums.append(num)

    st.markdown("### 🎯 Prediction Strategy")
    mode = st.radio("Select Mode:", ["Cautious", "Balanced", "Aggressive"])

    submitted = st.form_submit_button("🔮 Predict")

# if submitted:
    pred, conf = predict_big_small(nums, mode)
    st.success(f"✅ Predicted: *{pred}*")
    st.info(f"📊 Confidence: *{conf}%*")

    st.session_state['history'].append({"Inputs": nums, "Prediction": pred, "Confidence": conf})
    if len(st.session_state['history']) > 100:
        st.session_state['history'] = st.session_state['history'][-100:]

    time.sleep(1)

# --- History & Charts ---
if st.session_state['history']:
    st.markdown("---")
    st.subheader("📜 Prediction History")

    df = pd.DataFrame(st.session_state['history'])

    st.dataframe(df, use_container_width=True)

    # Heatmap
    st.subheader("📊 Prediction Heatmap")
    preds = [row["Prediction"] for row in st.session_state['history']]
    counts = pd.Series(preds).value_counts()
    st.bar_chart(counts)

    # --- Export Buttons ---
    csv_data = df.to_csv(index=False).encode()
    txt_data = "\n".join([str(row) for row in st.session_state['history']]).encode()

    st.download_button("📥 Export as CSV", csv_data, "predictions.csv", "text/csv")
    st.download_button("📥 Export as TXT", txt_data, "predictions.txt", "text/plain")
