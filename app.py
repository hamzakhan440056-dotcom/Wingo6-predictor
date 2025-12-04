Shandar! 🚀

*Part 1: Setup, UI, and Input Capture*  
Yeh part Streamlit UI setup karta hai, user inputs leta hai, aur strategy mode select karwata hai.

```python
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

Input fields
inputs = []
for i in range(1, 6):
    num = st.number_input(f"Result {i}", min_value=0, max_value=9, step=1, key=f"res{i}")
    inputs.append(num)

Mode selection
st.markdown("### 🎯 Prediction Strategy")
mode = st.radio("Select Mode:", ["Cautious", "Balanced", "Aggressive"])
```

*➤ Aap 'Ready' likhein to Part 2 bhejta hoon (Prediction logic + Display).*
