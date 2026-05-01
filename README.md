# 🎙️ AI Sales Intelligence Engine

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![NLP](https://img.shields.io/badge/NLP-TextBlob-green.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-Deployed-red.svg)

## 📌 Project Overview
This project is an AI-powered Natural Language Processing (NLP) tool designed for B2B sales teams. It ingests raw sales call transcripts and uses machine learning and regular expressions (Regex) to automatically extract actionable business intelligence. 

Instead of manually reviewing calls, Sales Managers can use this tool to instantly gauge customer sentiment, flag competitor mentions, and extract budget constraints.

🔗 **[Click Here to View the Live Application](Insert Your Streamlit Link Here)**

---

## 🏗️ Core Features & Tech Stack

* **Sentiment Analysis (`TextBlob`):** Calculates the mathematical polarity of the entire conversation and provides a sentence-by-sentence breakdown to identify exactly when a call turned positive or negative.
* **Entity Extraction (`Regex`):** Employs custom regular expressions to automatically detect and extract specific dollar amounts, budget mentions, and competitor names from unstructured text.
* **Business Signal Flagging (`pandas`):** Categorizes sentences into distinct business signals (e.g., "Pricing Objection" or "Buying Signal") based on contextual keywords.
* **Interactive UI (`streamlit`):** A fully responsive web dashboard deployed via Streamlit Community Cloud, allowing users to input custom transcripts and track dynamic competitor lists.

---

## 🚀 How to Run Locally

If you want to clone this repository and test the NLP engine on your own machine:

**1. Clone the repository:**
```bash
git clone [Insert Your GitHub Repo Link Here]
cd sales_nlp_engine