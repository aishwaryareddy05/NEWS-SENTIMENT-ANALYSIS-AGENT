import streamlit as st
import pandas as pd
from textblob import TextBlob
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time
from NewsAgentAI import NewsAgentAI
from utils import apply_custom_styling, create_alert_box, create_info_card, hide_streamlit_style
from config import DEFAULT_QUERY, DEFAULT_REFRESH_INTERVAL

# Configure page
st.set_page_config(
    page_title="News Sentiment AI Agent",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom styling
apply_custom_styling()
hide_streamlit_style()

def main():
    agent = NewsAgentAI()

    st.markdown('<div class="main-header">', unsafe_allow_html=True)
    st.markdown("# 🤖 News Sentiment AI Agent")
    st.markdown("### Real-time news analysis with autonomous sentiment monitoring")
    st.markdown('</div>', unsafe_allow_html=True)

    st.sidebar.header("🎛️ Agent Configuration")

    query = st.sidebar.text_input("News Query", value=DEFAULT_QUERY, help="Enter keywords to search for news")
    auto_refresh = st.sidebar.checkbox("Auto-refresh (30s)", value=False)

    if st.sidebar.button("🔄 Refresh Now", type="primary"):
        st.rerun()

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.sidebar.info(f"Last updated: {current_time}")

    with st.spinner("🔍 AI Agent analyzing news..."):
        articles = agent.fetch_news(query=query)

        if not articles:
            st.warning("No articles found. Please try a different query.")
            return

        processed_data = []
        for article in articles:
            title = article.get('title', '')
            description = article.get('description', '')
            published_at = article.get('publishedAt', '')
            source = article.get('source', {}).get('name', 'Unknown')
            url = article.get('url', '')
            combined_text = f"{title} {description}"
            sentiment_score, sentiment_label = agent.analyze_sentiment(combined_text)
            category = agent.categorize_topic(title, description)

            processed_data.append({
                'title': title,
                'description': description,
                'published_at': published_at,
                'source': source,
                'url': url,
                'sentiment_score': sentiment_score,
                'sentiment_label': sentiment_label,
                'category': category
            })

        df = pd.DataFrame(processed_data)
        insights = agent.generate_insights(df)

        st.subheader("🧠 AI Agent Insights")
        for insight in insights:
            if insight['type'] == 'alert':
                create_alert_box(insight['message'], insight['level'])
            else:
                create_info_card("Agent Analysis", insight['message'], "🤖")

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📰 Total Articles", len(df))
        with col2:
            avg_sentiment = df['sentiment_score'].mean()
            st.metric("📊 Avg Sentiment", f"{avg_sentiment:.2f}")
        with col3:
            positive_count = len(df[df['sentiment_label'] == 'positive'])
            st.metric("😊 Positive News", positive_count)
        with col4:
            negative_count = len(df[df['sentiment_label'] == 'negative'])
            st.metric("😟 Negative News", negative_count)

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("📈 Sentiment Distribution")
            sentiment_counts = df['sentiment_label'].value_counts()
            colors = {'positive': '#28a745', 'negative': '#dc3545', 'neutral': '#6c757d'}
            fig_pie = px.pie(
                values=sentiment_counts.values,
                names=sentiment_counts.index,
                color=sentiment_counts.index,
                color_discrete_map=colors
            )
            st.plotly_chart(fig_pie, use_container_width=True)

        with col2:
            st.subheader("🏷️ Topic Categories")
            topic_counts = df['category'].value_counts()
            fig_bar = px.bar(
                x=topic_counts.index,
                y=topic_counts.values,
                labels={'x': 'Category', 'y': 'Article Count'},
                color=topic_counts.values,
                color_continuous_scale='viridis'
            )
            st.plotly_chart(fig_bar, use_container_width=True)

        st.subheader("📊 Sentiment Timeline")
        fig_line = px.scatter(
            df,
            x='published_at',
            y='sentiment_score',
            color='sentiment_label',
            hover_data=['title', 'source'],
            color_discrete_map={'positive': '#28a745', 'negative': '#dc3545', 'neutral': '#6c757d'}
        )
        fig_line.update_layout(xaxis_title="Publication Time", yaxis_title="Sentiment Score")
        st.plotly_chart(fig_line, use_container_width=True)

        st.subheader("📄 Recent Articles")
        sentiment_filter = st.selectbox(
            "Filter by Sentiment",
            options=['All', 'Positive', 'Negative', 'Neutral'],
            index=0
        )
        filtered_df = df if sentiment_filter == 'All' else df[df['sentiment_label'] == sentiment_filter.lower()]

        for idx, row in filtered_df.head(10).iterrows():
            sentiment_emoji = {'positive': '😊', 'negative': '😟', 'neutral': '😐'}
            with st.expander(f"{sentiment_emoji[row['sentiment_label']]} {row['title'][:80]}..."):
                st.write(f"**Source:** {row['source']}")
                st.write(f"**Category:** {row['category'].title()}")
                st.write(f"**Sentiment:** {row['sentiment_label'].title()} ({row['sentiment_score']:.2f})")
                st.write(f"**Description:** {row['description']}")
                st.write(f"**Published:** {row['published_at']}")
                if row['url']:
                    st.write(f"**Link:** [Read More]({row['url']})")

    if auto_refresh:
        time.sleep(DEFAULT_REFRESH_INTERVAL)
        st.rerun()

if __name__ == "__main__":
    main()
