import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

st.set_page_config(page_title="Big vs Small Predictor", layout="centered")
st.title("🎲 Big vs Small Predictor")

# --- Session State for History ---
if "history" not in st.session_state:
    st.session_state.history = []

# --- Input Section ---
st.subheader("Enter last 5 results (digits 0 to 9):")
cols = st.columns(5)
inputs = []
for i in range(5):
    num = cols[i].number_input(f"Result {i+1}", min_value=0, max_value=9, step=1, key=f"num_{i}")
    inputs.append(num)

# --- Strategy Selection ---
st.subheader("🎯 Prediction Strategy")
mode = st.radio("Select Mode:", ["Cautious", "Balanced", "Aggressive"], horizontal=True)

# --- Prediction Logic ---
def predict_big_small(numbers, mode="Balanced"):
    count = Counter(["Big" if n >= 5 else "Small" for n in numbers])
    bigs = count["Big"]
    smalls = count["Small"]

    if mode == "Cautious":
        prediction = "Small" if smalls >= 3 else "Big"
        elif mode == "Aggressive":
        prediction = "Big" if bigs >= 2 else "Small"
    else:  # Balanced
        prediction = "Big" if bigs > smalls else "Small"

    confidence = round(100 * max(bigs, smalls) / len(numbers), 1)
    return prediction, confidence

# --- Show Prediction ---
if st.button("🔮 Predict"):
    prediction, confidence = predict_big_small(inputs, mode)
    st.success(f"✅ Predicted: *{prediction}*")
    st.info(f"📊 Confidence: *{confidence}%*")

    # Save to history
    st.session_state.history.append({
        "inputs": inputs.copy(),
        "prediction": prediction,
        "confidence": confidence
    })

# --- History Display ---
if st.session_state.history:
    st.subheader("📜 Prediction History")
    hist_df = pd.DataFrame(st.session_state.history)
    st.dataframe(hist_df[::-1], use_container_width=True)

    # --- Export Buttons ---
    csv = hist_df.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Download CSV", csv, "prediction_history.csv", "text/csv")

    # --- Frequency Chart ---
    st.subheader("🧊 Big vs Small Frequency Chart")
    all_results = []
    for h in st.session_state.history:
        all_results.extend(h["inputs"])

    labels = ["Small" if n < 5 else "Big" for n in all_results]
    freq = Counter(labels)
fig, ax = plt.subplots()
    ax.bar(freq.keys(), freq.values(), color=["skyblue", "lightgreen"])
    ax.set_ylabel("Count")
    ax.set_title("Big vs Small Frequency")
    st.pyplot(fig)
