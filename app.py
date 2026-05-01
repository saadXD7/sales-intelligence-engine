import streamlit as st
import pandas as pd
from textblob import TextBlob

st.set_page_config(page_title="Sales Intelligence Engine", layout="wide")

st.title("🎙️ AI Sales Intelligence Engine")
st.markdown("Analyze sales call transcripts to extract customer sentiment, objections, and buying signals.")
st.markdown("---")

# The Input Area
st.subheader("1. Input Call Transcript")
sample_transcript = """
Sales Rep: Hi, thanks for taking the time to look at our software.
Customer: No problem. I like the interface, it looks really clean and easy to use.
Sales Rep: Glad to hear that! It integrates directly with your current stack.
Customer: That's great, but honestly, the price is way too high for our current budget. I'm worried about the ROI.
Sales Rep: I understand. What if we offered a phased rollout?
Customer: That might actually work. Send me the revised contract and I'll show it to my manager.
"""
transcript = st.text_area("Paste the transcript here:", value=sample_transcript, height=200)

if st.button("Analyze Call"):
    st.markdown("---")
    st.subheader("2. AI Analysis Results")
    
    # NLP Processing
    blob = TextBlob(transcript)
    sentiment_score = blob.sentiment.polarity
    
    # Metric Cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if sentiment_score > 0.1:
            st.success(f"Overall Tone: Positive ({sentiment_score:.2f})")
        elif sentiment_score < -0.1:
            st.error(f"Overall Tone: Negative ({sentiment_score:.2f})")
        else:
            st.warning(f"Overall Tone: Neutral ({sentiment_score:.2f})")
            
    with col2:
        st.info(f"Total Sentences: {len(blob.sentences)}")
        
    with col3:
        st.info(f"Word Count: {len(blob.words)}")

    st.markdown("### Sentence-by-Sentence Breakdown")
    
    # Analyze individual sentences for business signals
    results = []
    for sentence in blob.sentences:
        text = str(sentence)
        polarity = sentence.sentiment.polarity
        
        # Simple Keyword Extraction for Sales Context
        category = "Neutral"
        if any(word in text.lower() for word in ['price', 'budget', 'expensive', 'cost', 'worried']):
            category = "🚨 Pricing Objection"
        elif any(word in text.lower() for word in ['contract', 'manager', 'buy', 'work', 'like', 'great']):
            category = "✅ Buying Signal"
            
        results.append({"Sentence": text, "Sentiment Score": round(polarity, 2), "Sales Signal": category})

    df = pd.DataFrame(results)
    st.dataframe(df, use_container_width=True)