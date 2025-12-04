import streamlit as st
import numpy as np
import time

st.set_page_config(page_title="Big vs Small Predictor", layout="centered")

st.title("🎲 Big vs Small Predictor")
st.markdown("Enter last 5 results (digits 0 to 9):")

# --- Session state for history ---
if 'history' not in st.session_state:
    st.session_state.history = []

# --- Input form ---
with st.form("input_form"):
    col1, col2 = st.columns(2)
    with col1:
        n1 = st.number_input("Result 1", min_value=0, max_value=9, step=1)
        n2 = st.number_input("Result 2", min_value=0, max_value=9, step=1)
        n3 = st.number_input("Result 3", min_value=0, max_value=9, step=1)
    with col2:
        n4 = st.number_input("Result 4", min_value=0, max_value=9, step=1)
        n5 = st.number_input("Result 5", min_value=0, max_value=9, step=1)

    strategy = st.selectbox("🎯 Prediction Strategy", ["Balanced", "Aggressive", "Cautious"])
    submitted = st.form_submit_button("🔮 Predict")

# --- Prediction logic ---
    def predict_next(numbers, mode):
       avg = np.mean(numbers)
    if mode == "Aggressive":
        pred = avg + np.random.uniform(0.5, 1.5)
    elif mode == "Cautious":
        pred = avg + np.random.uniform(-1.0, 0.5)
    else:
        pred = avg + np.random.uniform(-0.5, 1.0)

    pred = max(0, min(9, round(pred)))  # Keep within 0–9return pred

# --- Show result ---
if submitted:
    inputs = [n1, n2, n3, n4, n5]
    prediction = predict_next(inputs, strategy)
    st.session_state.history.append(prediction)

    st.markdown(f"### 🎯 Predicted Number: `{prediction}`")

    if prediction >= 5:
        st.success("🟢 Prediction: *Big (5–9)* 😎")
    else:
        st.warning("🟠 Prediction: *Small (0–4)* 🤔")

    # Countdown
    with st.empty():
        for i in range(5, 0, -1):
            st.info(f"⌛ Next prediction in {i} seconds...")
            time.sleep(1)

# --- History section ---
if st.session_state.history:
    st.markdown("---")
    st.subheader("📈 Prediction History")
    st.write(st.session_state.history)

    # Download button
    hist_str = "\n".join(str(x) for x in st.session_state.history)
    st.download_button("📥 Download History", hist_str, "history.txt")
