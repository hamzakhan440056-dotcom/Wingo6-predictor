import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

st.set_page_config(page_title="🎲 Big vs Small Predictor", layout="centered")
st.title("🎲 Big vs Small Predictor")

# Initialize session state
if 'history' not in st.session_state:
    st.session_state.history = []

# --- Input section ---
st.subheader("Enter last 5 results (digits 0 to 9):")
inputs = []
cols = st.columns(5)
for i in range(5):
    with cols[i]:
        num = st.number_input(f"Result {i+1}", min_value=0, max_value=9, step=1, key=f"num_{i}")
        inputs.append(num)

st.subheader("🎯 Prediction Strategy")
mode = st.selectbox("Select Mode:", ["Cautious", "Balanced", "Aggressive"])

# --- Prediction Logic ---
def predict(numbers, mode):
    avg = np.mean(numbers)
    if mode == "Cautious":
        threshold = 5.2
    elif mode == "Balanced":
        threshold = 5.0
    else:
        threshold = 4.8
    prediction = "Big" if avg >= threshold else "Small"
    confidence = round(abs(avg - threshold) * 20 + 80, 1)
    return prediction, confidence, avg

# Predict
if st.button("🔮 Predict"):
    pred, conf, avg = predict(inputs, mode)
    st.success(f"✅ Predicted: {pred}")
    st.write(f"📊 Confidence: {conf}%")
    
    # Save to history
    st.session_state.history.append({
        "time": datetime.now().strftime("%H:%M:%S"),
        "inputs": inputs.copy(),
        "prediction": pred,
        "confidence": conf
    })

# --- History Display ---
if st.session_state.history:
    st.subheader("📜 Prediction History")
    df = pd.DataFrame(st.session_state.history)
    st.dataframe(df[::-1], use_container_width=True)

    # --- Frequency Chart ---
    all_results = []
    for h in st.session_state.history:
        all_results.extend(h["inputs"])

    labels = ["Small", "Big"]
    counts = [sum([1 for n in all_results if n < 5]), sum([1 for n in all_results if n >= 5])]
    fig, ax = plt.subplots()
    ax.bar(labels, counts, color=["skyblue", "lightgreen"])
    ax.set_title("Big vs Small Frequency")
    st.pyplot(fig)

    # --- Time-based Trend ---
    st.subheader("⏳ Time-Based Trend")
    times = [h["time"] for h in st.session_state.history]
    preds = [1 if h["prediction"] == "Big" else 0 for h in st.session_state.history]
    fig2, ax2 = plt.subplots()
    ax2.plot(times, preds, marker='o', linestyle='-', color='purple')
    ax2.set_title("Prediction Over Time")
    ax2.set_ylabel("1 = Big | 0 = Small")
    ax2.set_xticks(times[::max(1, len(times)//5)])
    ax2.tick_params(axis='x', rotation=45)
    st.pyplot(fig2)

    # --- Export Button ---
    csv = pd.DataFrame(st.session_state.history).to_csv(index=False).encode()
    st.download_button("⬇️ Download CSV", data=csv, file_name="prediction_history.csv", mime='text/csv')
