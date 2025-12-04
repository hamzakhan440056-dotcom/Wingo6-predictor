import streamlit as st
import numpy as np
import pandas as pd
import time
import matplotlib.pyplot as plt
from io import BytesIO

# --- Helper functions ---

def save_history(record):
    if 'history' not in st.session_state:
        st.session_state['history'] = []
    st.session_state['history'].append(record)
    if len(st.session_state['history']) > 100:
        st.session_state['history'] = st.session_state['history'][-100:]

def get_risk_level(prediction):
    if prediction < 4:
        return 'High Risk', 'red'
    elif prediction < 6:
        return 'Medium Risk', 'orange'
    else:
        return 'Low Risk', 'green'

def make_prediction(inputs, strategy):
    avg = np.mean(inputs)
    if strategy == "Cautious":
        pred = avg * 0.9
    elif strategy == "Balanced":
        pred = avg
    else:  # Aggressive
        pred = avg * 1.1
    pred = max(min(pred, 9), 0)  # Clamp between 0 and 9
    confidence = 100 - abs(pred - avg) * 10
    for i in range(5, 0, -1):
            countdown_placeholder.markdown(f"⌛ Next prediction in *{i}* seconds...")
            time.sleep(1)
            countdown_placeholder.empty()

with col2:
    st.markdown("### 🔥 History (Last 5)")
    if 'history' in st.session_state and st.session_state['history']:
        recent = st.session_state['history'][-5:]
        for rec in reversed(recent):
            st.markdown(f"- Inputs: {rec['inputs']} | Strategy: {rec['strategy']} → Prediction: *{rec['prediction']}* (Conf: {rec['confidence']:.2f}%) Risk: {rec['risk']}")
    else:
        st.write("No history yet.")

# --- Charts ---

if 'history' in st.session_state and st.session_state['history']:
    st.markdown("---")
    st.markdown("### 📈 Prediction Trendline")
    preds = [rec['prediction'] for rec in st.session_state['history']]
    fig, ax = plt.subplots(figsize=(10, 3))
    ax.plot(preds, marker='o', linestyle='-', color='blue')
    ax.set_title("Predictions Over Time")
    ax.set_xlabel("Prediction Number")
    ax.set_ylabel("Predicted Value")
    st.pyplot(fig)

    st.markdown("### 🔥 Prediction Heatmap")
    all_preds = np.array(preds).round().astype(int)
    counts = pd.Series(all_preds).value_counts().sort_index()
    heatmap_data = pd.DataFrame({'Count': counts})
        return round(pred, 2), confidence

# --- Main App ---

st.title("🎲 Big vs Small Predictor")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("Enter last 5 results (digits 0 to 9):")
    inputs = []
    for i in range(5):
        inputs.append(st.number_input(f"Result {i+1}", min_value=0, max_value=9, value=0, key=f"input_{i}"))

    strategy = st.selectbox("🎯 Prediction Strategy", ["Cautious", "Balanced", "Aggressive"])

    if st.button("🔮 Predict"):
        prediction, confidence = make_prediction(inputs, strategy)
        risk_text, risk_color = get_risk_level(prediction)

        st.markdown(f"🚀 *Prediction:* {prediction}")
        st.markdown(f"💡 *Confidence:* {confidence:.2f}%")
        st.markdown(f"<span style='color:{risk_color}; font-weight:bold;'>Risk Level: {risk_text}</span>", unsafe_allow_html=True)

        emoji = "🤩" if risk_text == 'Low Risk' else "⚠️" if risk_text == 'High Risk' else "🙂"
        st.markdown(f"*Feedback:* {emoji}")

        # Save to history
        save_history({
            'inputs': inputs,
            'strategy': strategy,
            'prediction': prediction,
            'confidence': confidence,
            'risk': risk_text
        })

        # Countdown timer
        countdown_placeholder = st.empty()
    fig2, ax2 = plt.subplots(figsize=(8, 1))
    ax2.bar(heatmap_data.index, heatmap_data['Count'], color='purple')
    ax2.set_title("Prediction Frequency Heatmap")
    ax2.set_xlabel("Predicted Value (Rounded)")
    ax2.set_ylabel("Frequency")
    st.pyplot(fig2)

# --- Export History ---

if 'history' in st.session_state and st.session_state['history']:
    df = pd.DataFrame(st.session_state['history'])
    csv = df.to_csv(index=False).encode('utf-8')
    txt = df.to_string(index=False)

    st.download_button("📥 Export History as CSV", csv, "big_small_history.csv", "text/csv")
    st.download_button("📥 Export History as TXT", txt, "big_small_history.txt", "text/plain")
