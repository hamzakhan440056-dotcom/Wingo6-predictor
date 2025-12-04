import streamlit as st
import numpy as np

st.title("🎲 Big vs Small Predictor")

# User input
nums = []
for i in range(5):
    num = st.number_input(f"Result {i+1}", min_value=0, max_value=9, step=1, key=f"r{i}")
    nums.append(num)

# Strategy input
mode = st.selectbox("🎯 Prediction Strategy", ["Cautious", "Balanced", "Aggressive"])

def predict_next(numbers, mode):
    avg = np.mean(numbers)
    if mode == "Aggressive":
        pred = avg + np.random.uniform(0.5, 1.5)
    elif mode == "Cautious":
        pred = avg + np.random.uniform(-1.0, 0.5)
    else:
        pred = avg + np.random.uniform(-0.5, 1.0)

    pred = round(max(0, min(9, pred)))
    return pred

if st.button("🔮 Predict"):
    prediction = predict_next(nums, mode)
    st.markdown(f"### 🔢 Predicted Number: *{prediction}*")
    if prediction >= 5:
        st.success("Prediction: *Big* ✅")
    else:
        st.warning("Prediction: *Small* ⚠️")
