import streamlit as st
import base64
import os
from utils import (
    extract_news,
    analyze_sentiment,
    generate_summary,
    extract_topics,
    comparative_analysis,
    generate_final_sentiment,
    text_to_speech
)

# Streamlit Web Interface
st.title("📰 News Summarization and Sentiment Analysis")
company_name = st.text_input("Enter Company Name")

if company_name:
    # Extract and process articles
    articles = extract_news(company_name)
    summary_data = {
        "Company": company_name,
        "Articles": [],
        "Comparative Sentiment Score": {},
        "Final Sentiment Analysis": "",
        "Audio": ""
    }

    for article in articles:
        summary = generate_summary(article["content"])
        sentiment, _ = analyze_sentiment(article["content"])
        topics = extract_topics(article["content"])

        summary_data["Articles"].append({
            "Title": article["title"],
            "Summary": summary,
            "Sentiment": sentiment,
            "Topics": topics
        })

    # Generate Comparative Sentiment Score
    summary_data["Comparative Sentiment Score"] = comparative_analysis(summary_data["Articles"])
    summary_data["Final Sentiment Analysis"] = generate_final_sentiment(summary_data)

    # 🎙️ Generate Audio for Hindi TTS
    try:
        audio_path = text_to_speech(summary_data["Final Sentiment Analysis"], language="hi")

        if audio_path and os.path.exists(audio_path):
            # Read and play the generated audio
            with open(audio_path, "rb") as audio_file:
                audio_bytes = audio_file.read()

            # 🎧 Play the audio in Streamlit
            st.header("🎙️ Hindi TTS")
            st.audio(audio_bytes, format="audio/mp3")

            # 📥 Provide a download button for the audio
            st.download_button(
                label="⬇️ Download Audio",
                data=audio_bytes,
                file_name="audio.mp3",
                mime="audio/mp3"
            )
        else:
            st.error("❌ Error generating audio.")
    except Exception as e:
        st.error(f"⚠️ Error generating audio: {str(e)}")


        
    # Display Summary
    st.header("News Summary Report")
    for article_data in summary_data["Articles"]:
        st.subheader(article_data["Title"])
        st.write(f"**Summary:** {article_data['Summary']}")
        st.write(f"**Sentiment:** {article_data['Sentiment']}")
        st.write(f"**Topics:** {', '.join(article_data['Topics'])}")

    # Comparative Analysis
    st.header("Comparative Analysis")
    st.write(summary_data["Comparative Sentiment Score"])

    # Final Sentiment
    st.header("Final Sentiment Analysis")
    st.write(summary_data["Final Sentiment Analysis"])
