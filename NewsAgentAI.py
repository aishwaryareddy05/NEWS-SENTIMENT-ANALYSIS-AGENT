import json
import os
from collections import Counter
import re
from textblob import TextBlob
import requests
from datetime import datetime, timedelta
import streamlit as st
from dotenv import load_dotenv
from config import POSITIVE_THRESHOLD, NEGATIVE_THRESHOLD, INSIGHT_POS_THRESHOLD, INSIGHT_NEG_THRESHOLD, NEGATIVE_COVERAGE_RATIO, TOPIC_KEYWORDS

load_dotenv()

class NewsAgentAI:
    def __init__(self):
        self.api_key = os.getenv("NEWS_API_KEY")
        self.base_url = "https://newsapi.org/v2/everything"

    def fetch_news(self, query="technology", sources=None, page_size=50):
        try:
            if not self.api_key:
                return self._get_sample_news()

            params = {
                'q': query,
                'apiKey': self.api_key,
                'language': 'en',
                'sortBy': 'publishedAt',
                'pageSize': page_size,
                'from': (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
            }

            if sources:
                params['sources'] = sources

            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get('articles', [])
        except Exception as e:
            st.error(f"Error fetching news: {e}")
            return self._get_sample_news()

    def _get_sample_news(self):
        return [
            {
                'title': 'AI Revolution Transforms Healthcare Industry',
                'description': 'Artificial intelligence is revolutionizing healthcare with breakthrough diagnostic tools and personalized treatment plans.',
                'publishedAt': '2024-01-20T10:30:00Z',
                'source': {'name': 'TechNews'},
                'url': 'https://example.com/ai-healthcare'
            },
            {
                'title': 'Tech Stocks Plummet Amid Economic Uncertainty',
                'description': 'Major technology companies face significant losses as market volatility continues to impact investor confidence.',
                'publishedAt': '2024-01-20T09:15:00Z',
                'source': {'name': 'FinanceDaily'},
                'url': 'https://example.com/tech-stocks'
            },
            {
                'title': 'Breakthrough in Quantum Computing Announced',
                'description': 'Scientists achieve major milestone in quantum computing, bringing us closer to practical quantum applications.',
                'publishedAt': '2024-01-20T08:45:00Z',
                'source': {'name': 'ScienceToday'},
                'url': 'https://example.com/quantum-computing'
            },
            {
                'title': 'Climate Change Solutions Show Promise',
                'description': 'New renewable energy technologies demonstrate significant potential for reducing carbon emissions globally.',
                'publishedAt': '2024-01-20T07:30:00Z',
                'source': {'name': 'EcoNews'},
                'url': 'https://example.com/climate-solutions'
            },
            {
                'title': 'Cybersecurity Threats Increase Dramatically',
                'description': 'Organizations worldwide report surge in cyber attacks, highlighting need for enhanced security measures.',
                'publishedAt': '2024-01-20T06:20:00Z',
                'source': {'name': 'SecurityAlert'},
                'url': 'https://example.com/cybersecurity'
            }
        ]

    def analyze_sentiment(self, text):
        if not text:
            return 0, 'neutral'

        blob = TextBlob(text)
        polarity = blob.sentiment.polarity

        if polarity > POSITIVE_THRESHOLD:
            return polarity, 'positive'
        elif polarity < NEGATIVE_THRESHOLD:
            return polarity, 'negative'
        else:
            return polarity, 'neutral'

    def categorize_topic(self, title, description):
        text = f"{title} {description}".lower()

        for category, keywords in TOPIC_KEYWORDS.items():
            if any(keyword in text for keyword in keywords):
                return category

        return 'other'

    def generate_insights(self, df):
        insights = []

        avg_sentiment = df['sentiment_score'].mean()
        if avg_sentiment < INSIGHT_NEG_THRESHOLD:
            insights.append({
                'type': 'alert',
                'level': 'negative',
                'message': f'🚨 NEGATIVE SENTIMENT DETECTED: Average sentiment is {avg_sentiment:.2f}. Market conditions may be concerning.'
            })
        elif avg_sentiment > INSIGHT_POS_THRESHOLD:
            insights.append({
                'type': 'alert',
                'level': 'positive',
                'message': f'✅ POSITIVE SENTIMENT DETECTED: Average sentiment is {avg_sentiment:.2f}. Market outlook appears optimistic.'
            })

        topic_counts = df['category'].value_counts()
        dominant_topic = topic_counts.index[0]
        insights.append({
            'type': 'info',
            'message': f'📊 TRENDING TOPIC: {dominant_topic.title()} dominates news coverage with {topic_counts.iloc[0]} articles'
        })

        negative_news = df[df['sentiment_label'] == 'negative']
        if len(negative_news) > len(df) * NEGATIVE_COVERAGE_RATIO:
            insights.append({
                'type': 'alert',
                'level': 'negative',
                'message': f'⚠️ HIGH NEGATIVE COVERAGE: {len(negative_news)} out of {len(df)} articles are negative'
            })

        return insights
