# News-summarization-app

# 📢 News Summarization and Sentiment Analysis with Hindi TTS

## 📚 Project Overview
This project extracts news articles related to a given company, analyzes sentiment, performs topic extraction, and generates a comparative sentiment summary. Additionally, a Hindi audio summary is generated.

---

## 🚀 Features
- Extract top 10 news articles using Google News.
- Perform sentiment analysis and topic extraction.
- Comparative analysis between articles.
- Generate Hindi audio summary using Google TTS.
- Streamlit integration for easy user interaction.

---

## 📂 Folder Structure
2. Install Required Libraries
    bash
    Copy
    Edit
    pip install -r requirements.txt
3. Run Flask Backend (API)
     python api.py
4. Run Streamlit Interface (Coming Next 😉)
    streamlit run app.py

   
🎯 API Endpoints
1. /fetch_news – Fetch and Analyze News
    Method: POST
      Payload:
      
          {
            "company_name": "Tesla"
          }

      Response:

        {
          "status": "success",
          "report": { ... }
        }
2. /generate_audio – Generate Hindi Audio Summary
    Method: POST
      Payload:

        {
          "summary_text": "Summary of the sentiment analysis..."
        }
      Response:

        {
          "status": "success",
          "audio_file": "sentiment_report_hi.mp3"
        }
⚡ Technologies Used

   1. Python
   2. Flask (Backend APIs)
   3. Streamlit (Frontend UI)
   4. BeautifulSoup, Feedparser (Web Scraping)
   5. NLTK (Sentiment & Topic Analysis)
   6. gTTS (Text-to-Speech)

    
👨‍💻 Author
Sneha Mishra
Data Analyst | ML Enthusiast | Python & Power BI Expert
