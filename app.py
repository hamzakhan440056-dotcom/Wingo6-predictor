import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Big vs Small Predictor", layout="centered")

st.title("🎲 Big vs Small Predictor")
st.markdown("Enter last *5 results* (digits 0 to 9):")

Session state
if 'history' not in st.session_state:
    st.session_state.history = []

# Input fields
inputs = []
for i in range(1, 6):
    num = st.number_input(f"Result {i}", min_value=0, max_value=9, step=1, key=f"res{i}")
    inputs.append(num)

# Mode selection
st.markdown("### 🎯 Prediction Strategy")
mode = st.radio("Select Mode:", ["Cautious", "Balanced", "Aggressive"])
*Part 2: Prediction Logic & Display Results*  
Yeh part prediction calculate karta hai, confidence nikalta hai, aur result show karta hai.

def predict_big_small(data, mode):
    avg = np.mean(data)
    
    # Adjust prediction thresholds based on mode
    if mode == "Cautious":
        threshold = 4.5
    elif mode == "Balanced":
        threshold = 4.0
    else:  # Aggressive
        threshold = 3.5

    if avg >= threshold:
        prediction = "Big"
        confidence = min(100, (avg / 9) * 100)
    else:
        prediction = "Small"
        confidence = min(100, ((9 - avg) / 9) * 100)

    return prediction, round(confidence, 1)

# Prediction trigger
if st.button("🔮 Predict"):
    prediction, confidence = predict_big_small(inputs, mode)
    
    # Save to session history
    st.session_state.history.append({
        "Inputs": inputs.copy(),
        "Prediction": prediction,
        "Confidence": confidence,
        "Mode": mode
    })

    # Display results
    st.success(f"✅ *Predicted:* {prediction}")
    st.info(f"📊 *Confidence:* {confidence}%")
   *Part 3: Prediction History + Export Feature*


# Show Prediction History
st.markdown("📜 *Prediction History*")
if st.session_state.history:
    history_df = pd.DataFrame(st.session_state.history)
    st.dataframe(history_df, use_container_width=True)

    # Export button
    history_txt = history_df.to_string(index=False)
    st.download_button("📥 Download History (TXT)", history_txt, file_name="prediction_history.txt")
else:
    st.info("No predictions yet.")
    
# Heatmap-style frequency chart
st.markdown("🧊 *Big vs Small Frequency Chart*")

if st.session_state.history:
    all_results = []
    for h in st.session_state.history:
        all_results.extend(h['inputs'])

    freq = {'Small (0-4)': 0, 'Big (5-9)': 0}
    for n in all_results:
        if n <= 4:
            freq['Small (0-4)'] += 1
        else:
            freq['Big (5-9)'] += 1

    fig, ax = plt.subplots()
    ax.bar(freq.keys(), freq.values(), color=['blue', 'orange'])
    ax.set_ylabel("Count")
    ax.set_title("Big vs Small Frequency")
    st.pyplot(fig)
else:
    st.info("No data to show heatmap.")
