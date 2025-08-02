
import streamlit as st
import joblib
import pandas as pd
from tweet_generator import SimpleTweetGenerator
from textblob import TextBlob

# Load your model directly (no separate API needed)
@st.cache_resource
def load_model():
    return joblib.load('like_predictor.pkl')

@st.cache_resource
def load_generator():
    return SimpleTweetGenerator()

model = load_model()
generator = load_generator()

st.title("🚀 Tweet Intelligence Engine")
st.write("Generate tweets and predict their engagement!")

import streamlit as st
import requests
import joblib

le_company = joblib.load('company_encoder.pkl')


st.title("Tweet Generator + Like Predictor")

with st.form("Tweet_genandpred"):
    st.text("Enter the following details to generate a tweet and predict its likes!")

    company = st.text_input("Company Name (e.g., Adidas)")
    
    tweet_type = st.selectbox(
        "Select tweet type",
        ["Announcement", "Update", "Promotion", "Milestone", "Event", "Question", "Opinion"],
        index=None,
        placeholder="Choose a tweet style..."
    )
    message = st.text_input("Input a message or topic (e.g., AI product launch)")
    hour = st.number_input("Select tweet time (0–23)", min_value=0, max_value=23, step=1)
    sentiment = st.slider("Select sentiment", -1.0, 1.0, 0.0, step=0.01)
    has_media = st.checkbox("Include image/video in tweet?", value=False)

    submitted = st.form_submit_button("Generate + Predict")

if submitted:
    
    if not company  or not message or not tweet_type:
        st.error("Please fill in all required fields.")
        st.stop()

    
    gen_payload = {
        "company": company,
        "industry": tweet_type, 
        "word_count_target": 20,
        "sentiment_target": sentiment,
        "has_media": int(has_media),
        "message": message
    }

    
    gen_resp = requests.post("https://tweetalyst.onrender.com/generate_smart_tweet", json=gen_payload)
    if gen_resp.ok and "generated_tweet" in gen_resp.json():
        generated_tweet = gen_resp.json()["generated_tweet"]
        st.markdown(f"**Generated Tweet:**\n\n{generated_tweet}")
    else:
        st.error("Failed to generate tweet.")
        st.text(gen_resp.text)
        st.stop()

    
    if company in le_company.classes_:
        company_encoded = le_company.transform([company])[0]
    else:
        company_encoded = le_company.transform(["unknown"])[0]

    

    
    pred_payload = {
        "word_count": len(generated_tweet.split()),
        "char_count": len(generated_tweet),
        "has_media": 1 if has_media else 0,
        "hour": hour,
        "day_of_week": 2, 
        "sentiment": sentiment,
        "message": message,
        "company_encoded": int(company_encoded),
        
    }

    
    pred_resp = requests.post("https://tweetalyst.onrender.com/predict_likes", json=pred_payload)
    if pred_resp.ok and "predicted_likes" in pred_resp.json():
        predicted_likes = pred_resp.json()["predicted_likes"]
        st.success(f"Predicted Likes: **{predicted_likes}**")
    else:
        st.error("Failed to predict likes.")
        st.text(pred_resp.text)


