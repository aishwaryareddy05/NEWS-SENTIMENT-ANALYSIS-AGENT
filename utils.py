import streamlit as st
import os
from pathlib import Path

def load_css(file_path):
    """Load CSS file and inject into Streamlit app"""
    try:
        with open(file_path, 'r') as f:
            css_content = f.read()
        st.markdown(f'<style>{css_content}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning(f"CSS file not found: {file_path}")
    except Exception as e:
        st.error(f"Error loading CSS: {e}")

def apply_custom_styling():
    """Apply custom styling to the Streamlit app"""
    # Get the directory of the current script
    current_dir = Path(__file__).parent
    css_file = current_dir / "styles.css"
    
    # Load the CSS file
    load_css(css_file)
    
    # Additional inline styles for specific components
    st.markdown("""
    <style>
        /* Page Configuration */
        .main .block-container {
            padding-top: 1rem;
            padding-bottom: 1rem;
        }
        
        /* Sidebar Styling */
        .sidebar .sidebar-content {
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        }
        
        /* Custom Expander */
        .streamlit-expanderHeader {
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            border: 1px solid #dee2e6;
            border-radius: 8px;
            font-weight: 500;
        }
        
        /* Metric Value Styling */
        [data-testid="metric-container"] {
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            border: 1px solid #dee2e6;
            border-radius: 8px;
            padding: 1rem;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        
        /* Custom Plotly Charts */
        .plotly-graph-div {
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
    </style>
    """, unsafe_allow_html=True)

def get_sentiment_color(sentiment_label):
    """Return color based on sentiment label"""
    color_map = {
        'positive': '#28a745',
        'negative': '#dc3545',
        'neutral': '#6c757d'
    }
    return color_map.get(sentiment_label, '#6c757d')

def get_sentiment_emoji(sentiment_label):
    """Return emoji based on sentiment label"""
    emoji_map = {
        'positive': '😊',
        'negative': '😟',
        'neutral': '😐'
    }
    return emoji_map.get(sentiment_label, '😐')

def create_styled_metric(title, value, delta=None, delta_color="normal"):
    """Create a styled metric card"""
    delta_html = ""
    if delta is not None:
        delta_symbol = "↑" if delta > 0 else "↓" if delta < 0 else "→"
        delta_color_css = "#28a745" if delta > 0 else "#dc3545" if delta < 0 else "#6c757d"
        delta_html = f'<div style="color: {delta_color_css}; font-size: 0.8rem; margin-top: 0.5rem;">{delta_symbol} {abs(delta)}</div>'
    
    st.markdown(f"""
    <div class="metric-container">
        <div style="font-size: 0.9rem; color: #6c757d; margin-bottom: 0.5rem;">{title}</div>
        <div style="font-size: 2rem; font-weight: 700; color: #2c3e50;">{value}</div>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)

def create_alert_box(message, alert_type="info"):
    """Create a styled alert box"""
    st.markdown(f'<div class="alert-box alert-{alert_type}">{message}</div>', unsafe_allow_html=True)

def create_info_card(title, content, icon="ℹ️"):
    """Create a styled info card"""
    st.markdown(f"""
    <div class="info-box">
        <div style="font-size: 1.1rem; font-weight: 600; margin-bottom: 0.5rem;">
            {icon} {title}
        </div>
        <div>{content}</div>
    </div>
    """, unsafe_allow_html=True)

def create_article_card(title, description, source, published_at, sentiment_label, sentiment_score, url=None):
    """Create a styled article card"""
    sentiment_color = get_sentiment_color(sentiment_label)
    sentiment_emoji = get_sentiment_emoji(sentiment_label)
    
    url_html = f'<a href="{url}" target="_blank" style="color: #667eea; text-decoration: none;">📖 Read More</a>' if url else ""
    
    st.markdown(f"""
    <div class="article-card">
        <div class="article-title">{sentiment_emoji} {title}</div>
        <div class="article-meta">
            <span style="color: #667eea; font-weight: 500;">{source}</span> • 
            <span>{published_at}</span> • 
            <span class="sentiment-{sentiment_label}">{sentiment_label.title()} ({sentiment_score:.2f})</span>
        </div>
        <div class="article-description">{description}</div>
        {url_html}
    </div>
    """, unsafe_allow_html=True)

def create_loading_spinner():
    """Create a loading spinner"""
    st.markdown("""
    <div class="loading-spinner">
        <div class="spinner"></div>
    </div>
    """, unsafe_allow_html=True)

def hide_streamlit_style():
    """Hide Streamlit default styling"""
    st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stDeployButton {display: none;}
    </style>
    """, unsafe_allow_html=True)