from flask import Flask, jsonify
from flask_cors import CORS
import base64
from utils import (
    extract_news,
    analyze_sentiment,
    generate_summary,
    extract_topics,
    comparative_analysis,
    generate_final_sentiment,
    text_to_speech
)

app = Flask(__name__)
CORS(app)

# Define a route to handle requests for news summaries
@app.route("/summary/<company_name>")
def get_news_summary(company_name):
    try:
        # Extract news articles related to the company
        articles = extract_news(company_name)
        
        if not articles:
            return jsonify({"error": "No articles found for the given company."}), 404
        
        summary_data = {
            "Company": company_name,
            "Articles": [],
            "Comparative Sentiment Score": {},
            "Final Sentiment Analysis": "",
            "Audio": ""
        }

        for article in articles:
            # Generate a summary for the article
            summary = generate_summary(article["content"])
            
            # Analyze sentiment of the article content
            sentiment, _ = analyze_sentiment(article["content"])
            
            # Extract key topics from the article
            topics = extract_topics(article["content"])

            # Add the processed article data to the summary
            summary_data["Articles"].append({
                "Title": article["title"],
                "Summary": summary,
                "Sentiment": sentiment,
                "Topics": topics
            })

        # Generate comparative sentiment score
        summary_data["Comparative Sentiment Score"] = comparative_analysis(summary_data["Articles"])
        
        # Generate the final sentiment analysis
        summary_data["Final Sentiment Analysis"] = generate_final_sentiment(summary_data)

        # Generate text-to-speech audio (Hindi TTS)
        try:
            audio_data = text_to_speech(summary_data["Articles"], language="hi")
            summary_data["Audio"] = base64.b64encode(audio_data).decode("utf-8")
        except Exception as e:
            summary_data["Audio"] = f"Error generating audio: {str(e)}"

        # Return the final summary as JSON
        return jsonify(summary_data)
    
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500


# Run the Flask app in debug mode
if __name__ == "__main__":
    app.run(debug=True)
