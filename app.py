import streamlit as st
import pandas as pd
from textblob import TextBlob
import re
import nltk

# --- BULLETPROOF FIX: FORCE DOWNLOAD DICTIONARIES ON WAKEUP ---
@st.cache_resource
def download_nltk_data():
    nltk.download('punkt')
    nltk.download('punkt_tab')

download_nltk_data()
# --------------------------------------------------------------

st.set_page_config(page_title="Sales Intelligence Engine", layout="wide")

st.title("🎙️ AI Sales Intelligence Engine")
st.markdown("Analyze sales call transcripts to extract customer sentiment, objections, and buying signals.")
st.markdown("---")

# --- SIDEBAR: ENTERPRISE SETTINGS ---
st.sidebar.header("⚙️ Intelligence Settings")
competitor_input = st.sidebar.text_input("Track Competitor Mentions (comma-separated):", "AcmeCorp, TechSolutions, GlobalSystems")
competitors_to_track = [c.strip().lower() for c in competitor_input.split(",")]

# The Input Area
st.subheader("1. Input Call Transcript")
sample_transcript = """
Sales Rep: Hi, thanks for taking the time to look at our software.
Customer: No problem. I like the interface, it looks really clean and easy to use.
Sales Rep: Glad to hear that! It integrates directly with your current stack.
Customer: That's great, but honestly, the price is way too high. We were looking at a $15,000 budget, and AcmeCorp quoted us much lower.
Sales Rep: I understand. What if we offered a phased rollout to keep it under budget?
Customer: That might actually work. Send me the revised contract for $14,500 and I'll show it to my manager.
"""
transcript = st.text_area("Paste the transcript here:", value=sample_transcript, height=200)

if st.button("Analyze Call"):
    st.markdown("---")
    
    # --- THE ENTITY EXTRACTOR (REGEX) ---
    st.subheader("2. 🕵️‍♂️ Competitive Intelligence & Budget Extraction")
    
    # Extract Dollar Amounts using Regex
    money_pattern = r'\$\d+(?:,\d+)?(?:\.\d+)?|\b\d+\s*(?:dollars|bucks)\b'
    budget_mentions = re.findall(money_pattern, transcript)
    
    # Extract Competitor Mentions
    found_competitors = [comp for comp in competitors_to_track if comp in transcript.lower()]
    
    colA, colB = st.columns(2)
    with colA:
        st.write("**💰 Budget/Pricing Mentions Detected:**")
        if budget_mentions:
            for amount in budget_mentions:
                st.warning(f"Detected Value: {amount}")
        else:
            st.write("No pricing mentioned.")
            
    with colB:
        st.write("**🚨 Competitor Mentions Detected:**")
        if found_competitors:
            for comp in found_competitors:
                st.error(f"Competitor Flagged: {comp.title()}")
        else:
            st.write("No competitors mentioned.")

    st.markdown("---")
    st.subheader("3. AI Sentiment Analysis")
    
    blob = TextBlob(transcript)
    sentiment_score = blob.sentiment.polarity
    
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
    
    results = []
    for sentence in blob.sentences:
        text = str(sentence)
        polarity = sentence.sentiment.polarity
        
        category = "Neutral"
        if any(word in text.lower() for word in ['price', 'budget', 'expensive', 'cost', 'worried']):
            category = "🚨 Pricing Objection"
        elif any(word in text.lower() for word in ['contract', 'manager', 'buy', 'work', 'like', 'great']):
            category = "✅ Buying Signal"
            
        results.append({"Sentence": text, "Sentiment Score": round(polarity, 2), "Sales Signal": category})

    df = pd.DataFrame(results)
    st.dataframe(df, use_container_width=True)