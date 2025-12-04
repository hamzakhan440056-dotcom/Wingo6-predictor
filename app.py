import streamlit as st

st.set_page_config(page_title="Big vs Small Predictor", layout="centered")

st.title("🎲 Big vs Small Predictor")
st.markdown("Enter last 5 results (each from 0 to 9):")

# User Inputs
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    n1 = st.number_input("1", min_value=0, max_value=9, step=1)
with col2:
    n2 = st.number_input("2", min_value=0, max_value=9, step=1)
with col3:
    n3 = st.number_input("3", min_value=0, max_value=9, step=1)
with col4:
    n4 = st.number_input("4", min_value=0, max_value=9, step=1)
with col5:
    n5 = st.number_input("5", min_value=0, max_value=9, step=1)

if st.button("🔮 Predict"):
    st.write("Prediction logic will go here.")
  # Here’s *Part 2* – Basic prediction logic and result display with feedback:

# import numpy as np

def predict_big_small(numbers):
    avg = np.mean(numbers)
    if avg >= 5:
        return "BIG", "🟢", "Prediction: Likely HIGH numbers ahead!"
    else:
        return "SMALL", "🔴", "Prediction: Likely LOW numbers ahead!"

# Collect user input into a list
numbers = [n1, n2, n3, n4, n5]

if st.button("🔮 Predict"):
    result, color, message = predict_big_small(numbers)
    
    st.markdown(f"### {color} *{result}*")
    st.markdown(f"_{message}_")

    # Optional: Show input summary
    st.write("You entered:", numbers)
  Here’s *Part 3* – Add *risk meter, countdown timer, and prediction hiscountdow

# import time
import matplotlib.pyplot as plt

# --- Risk Meter ---
def get_confidence(numbers):
    std_dev = np.std(numbers)
    confidence = max(0, 100 - std_dev * 10)  # Arbitrary confidence logic
    if confidence > 80:
        color = "green"
    elif confidence > 50:
        color = "orange"
    else:
        color = "red"
    return int(confidence), color

if 'history' not in st.session_state:
    st.session_state['history'] = []

if st.button("📊 Show Risk & History"):
    confidence, bar_color = get_confidence(numbers)
    st.markdown(f"*Confidence:* `{confidence}%`")
    st.progress(confidence)

    # Save to history
    st.session_state['history'].append(np.mean(numbers))

    # Line chart of prediction history
    if len(st.session_state['history']) > 1:
        st.line_chart(st.session_state['history'])

# --- Countdown ---
st.markdown("### ⏳ Next prediction in:")
countdown = st.empty()
for i in range(5, 0, -1):
    countdown.markdown(f"*{i}* seconds...")
    time.sleep(1)
countdown.empty()
Here’s *Part 4* – Add *Export, Heatmap, and Responsive Layout*:

# import seaborn as sns
import matplotlib.pyplot as plt
# from io import BytesIO

# --- Export Buttons ---
if st.session_state.get('history'):
    df = pd.DataFrame(st.session_state['history'], columns=["Prediction"])
    
    csv = df.to_csv(index=False).encode()
    st.download_button("⬇️ Export CSV", csv, "predictions.csv", "text/csv")

    txt = "\n".join(map(str, st.session_state['history']))
    st.download_button("📝 Export TXT", txt, "predictions.txt", "text/plain")

# --- Heatmap Chart ---
if len(st.session_state['history']) >= 5:
    st.markdown("### 🔥 Prediction Heatmap")
    fig, ax = plt.subplots(figsize=(8, 1))
    sns.heatmap([st.session_state['history']], cmap="YlOrRd", cbar=False, ax=ax)
    st.pyplot(fig)

# --- Responsive Layout ---
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    st.metric("Last", f"{st.session_state['history'][-1]:.2f}")
with col2:
    st.metric("Avg", f"{np.mean(st.session_state['history']):.2f}")
with col3:
    st.metric("Max", f"{np.max(st.session_state['history']):.2f}")
