import streamlit as st
import joblib
import pandas as pd

model = joblib.load("app/model.pkl")

st.title("Cricket Win Probability Predictor")

match_type = st.selectbox("Match type", ["ODI", "T20"])

balls_remaining = st.slider("Balls remaining", 0, 300, 150)
runs_needed = st.slider("Runs needed", 0, 500, 250)# highets ever team total is 498
wickets_in_hand = st.slider("Wickets in hand", 0, 10, 5)
current_run_rate = st.slider("Current run rate", 0.0, 36.0, 7.0) # average run rate in odi is between 5.2 and 5.5 and in t20 it is 8.0 and 8.5, and the average of those to is 7.0
required_run_rate = st.slider("Required run rate", 0.0, 36.0, 7.0) # average run rate in odi is between 5.0 and 6.0 and in t20 it is 8.0 and 9.0, and the average of those to is 7.0

match_type_encoded = 0 if match_type == "ODI" else 1

input_data = pd.DataFrame({
    "match_type": [match_type_encoded],
    "balls_remaining": [balls_remaining],
    "runs_needed": [runs_needed],
    "wickets_in_hand": [wickets_in_hand],
    "current_run_rate": [current_run_rate],
    "required_run_rate": [required_run_rate],
})

if st.button(label="Predict Win Probability"):
    win_probability = model.predict_proba(input_data)
    st.text(f"Win probability for the batting team: {win_probability[0][1]:.1%}")