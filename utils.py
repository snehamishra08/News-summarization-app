import requests
from bs4 import BeautifulSoup
import nltk
from collections import Counter
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from googletrans import Translator
from gtts import gTTS
import os

# Download required NLTK packages
nltk.download('vader_lexicon')
nltk.download('punkt')
nltk.download('stopwords')


def extract_news(company_name):
    url = f"https://news.google.com/rss/search?q={company_name}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'xml')

    articles = []
    for item in soup.find_all('item'):
        title = item.title.text
        content_html = item.description.text

        # Clean HTML content and extract plain text
        soup_content = BeautifulSoup(content_html, 'html.parser')
        content_text = soup_content.get_text(separator=' ').strip()

        # Handle edge cases for empty or irrelevant content
        if not content_text or len(content_text.split()) < 5:
            content_text = "Content could not be fetched."

        articles.append({'title': title, 'content': content_text})

    return articles




def fetch_full_article(url):
    """Fetch full article content from the link."""
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract text content intelligently based on common patterns
        paragraphs = soup.find_all('p')
        content = " ".join([para.text for para in paragraphs])

        if not content.strip():
            return "Content could not be fetched."
        
        return content
    except Exception as e:
        return f"Error fetching article content: {str(e)}"


def analyze_sentiment(text):
    analyzer = SentimentIntensityAnalyzer()
    scores = analyzer.polarity_scores(text)
    if scores['compound'] >= 0.05:
        return "Positive", scores['compound']
    elif scores['compound'] <= -0.05:
        return "Negative", scores['compound']
    else:
        return "Neutral", scores['compound']


def generate_summary(text):
    sentences = sent_tokenize(text)
    words = word_tokenize(text)
    word_frequencies = Counter(words)
    sentence_scores = {}

    for sentence in sentences:
        for word in word_tokenize(sentence):
            if word in word_frequencies:
                if sentence in sentence_scores:
                    sentence_scores[sentence] += word_frequencies[word]
                else:
                    sentence_scores[sentence] = word_frequencies[word]

    # Select top 3 sentences for summary
    summary_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)[:3]
    summary = ' '.join(summary_sentences)
    return summary


def extract_topics(text):
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text)
    filtered_words = [w for w in words if w.lower() not in stop_words and w.isalnum()]
    word_frequencies = Counter(filtered_words)
    topics = [word for word, freq in word_frequencies.most_common(5)]
    return topics


def comparative_analysis(articles):
    sentiment_distribution = Counter(article['Sentiment'] for article in articles)
    coverage_differences = []

    # Compare sentiment and topics between articles
    for i in range(len(articles)):
        for j in range(i + 1, len(articles)):
            comparison = f"Article {i + 1} ({articles[i]['Sentiment']}) discusses {', '.join(articles[i]['Topics'])}, while Article {j + 1} ({articles[j]['Sentiment']}) discusses {', '.join(articles[j]['Topics'])}."
            impact = "Further analysis is needed to determine the impact of these differences."
            coverage_differences.append({"Comparison": comparison, "Impact": impact})

    topic_overlap = {
        "Common Topics": list(set.intersection(*[set(article['Topics']) for article in articles])),
        "Unique Topics in Article 1": [],
        "Unique Topics in Article 2": []
    }

    # Analyze unique topics in each article
    if len(articles) >= 2:
        topic_overlap["Unique Topics in Article 1"] = list(set(articles[0]['Topics']) - set(articles[1]['Topics']))
        topic_overlap["Unique Topics in Article 2"] = list(set(articles[1]['Topics']) - set(articles[0]['Topics']))

    return {
        "Sentiment Distribution": dict(sentiment_distribution),
        "Coverage Differences": coverage_differences,
        "Topic Overlap": topic_overlap
    }


def generate_final_sentiment(summary_data):
    sentiments = [article['Sentiment'] for article in summary_data['Articles']]
    positive_count = sentiments.count('Positive')
    negative_count = sentiments.count('Negative')

    if positive_count > negative_count:
        return "The overall sentiment towards the company is positive."
    elif negative_count > positive_count:
        return "The overall sentiment towards the company is negative."
    else:
        return "The overall sentiment towards the company is neutral."


def text_to_speech(text, language="hi"):
    try:
        # Translate text to Hindi using googletrans
        translator = Translator()
        translated_text = translator.translate(text, dest=language).text

        # Generate audio using gTTS
        tts = gTTS(text=translated_text, lang=language)
        audio_path = "audio.mp3"
        tts.save(audio_path)

        # Return the path to the generated audio file
        return audio_path

    except Exception as e:
        print(f"Error during translation or TTS: {e}")
        return "Error generating audio"
