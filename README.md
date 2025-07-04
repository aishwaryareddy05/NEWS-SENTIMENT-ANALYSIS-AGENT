# 📰 News Sentiment AI Agent

An intelligent Streamlit-based application that fetches real-time news articles, performs sentiment analysis, categorizes topics, and provides dynamic insights with visual analytics.

## 🚀 Features

- 🔍 Query news articles in real-time using NewsAPI
- 😊 Sentiment analysis using TextBlob
- 🧠 AI-generated insights and alerts
- 📊 Visualizations: pie charts, bar charts, sentiment timelines
- 📰 Article previews with filtering and expanders
- 🌐 Fully styled and responsive Streamlit UI

---

## 🛠️ Tech Stack

- **Python** 3.10+
- **Streamlit**
- **TextBlob** for sentiment analysis
- **Plotly** for data visualization
- **NewsAPI** for live news fetching
- **dotenv** for environment configuration

---

## 🔄 System Architecture
```mermaid

flowchart TD
    A[User Input: QUERY] --> B[Streamlit Interface]
    B --> C[NewsAgentAI Fetches Articles]
    C --> D[TextBlob Analyzes Sentiment]
    C --> E[Categorization Logic - Topics]
    D --> F[DataFrame Generation]
    E --> F
    F --> G[Visualizations - Charts & Metrics]
    G --> H[Interactive Dashboard Output]
```
---

## 📦 Sequence Diagram

```mermaid
sequenceDiagram
    participant U as User
    participant S as Streamlit UI
    participant A as NewsAgentAI
    participant N as NewsAPI
    participant T as TextBlob

    U->>S: Inputs query
    S->>A: Sends query
    A->>N: Requests articles
    N-->>A: Returns articles
    A->>T: Analyze sentiment
    A->>S: Returns processed data
    S->>U: Displays metrics & visualizations
```

---

## 🧩 Component Architecture

```mermaid
graph TD
    UI[Streamlit UI] -->|Calls| Utils[utils.py: Metrics, Cards, CSS]
    UI -->|Initializes| Agent[NewsAgentAI]
    Agent -->|Uses| Config[config.py: Thresholds & Defaults]
    Agent -->|Calls| NewsAPI[External API]
    Agent -->|Sentiment| TextBlob[TextBlob Library]
    UI -->|Plots| Plotly[Plotly Charts]
```

---

## ☁️ Deployment Overview

```mermaid
graph LR
    Dev[Developer Machine] --> GitHub[GitHub Repo]
    GitHub -->|Deploy| StreamlitCloud[Streamlit Cloud / Localhost]
    StreamlitCloud --> NewsAPI[NewsAPI.org]
    StreamlitCloud --> Users[Web Users]
```

---

## 🔧 Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/news-sentiment-agent.git
cd news-sentiment-agent
```

### 2. Create and Activate Virtual Environment (optional)
```bash
python -m venv env
source env/bin/activate  # or .\env\Scripts\activate on Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables
Create a `.env` file in the root directory:
```ini
NEWS_API_KEY=your_actual_newsapi_key_here
```

### 5. Run the Application
```bash
streamlit run main.py
```

---

## 📁 Project Structure
```
├── main.py                # Streamlit app logic
├── NewsAgentAI.py         # Core class for news fetching & sentiment analysis
├── config.py              # Configurable thresholds & defaults
├── utils.py               # UI utilities for styling and metrics
├── styles.css             # Custom CSS for Streamlit UI
├── .env                   # Your API key (not included in repo)
├── requirements.txt       # Dependencies
└── README.md              # You're reading it!
```

---
### 🚀 Live Demo

Check out the live app here:  
🔗 [**NewsAgentAI Dashboard**](https://aishwaryareddy05-news-sentiment-analysis-agent-main-qvonit.streamlit.app/)

> 📌 *Hosted on Streamlit Cloud*

## ✨ Screenshots

<img src="screenshot-dashboard.png" width="80%" alt="Dashboard Overview"/>

---

## 📌 Notes
- All hardcoded values (API keys, thresholds, defaults) have been externalized.
- Includes fallback sample data if API fails.
- Streamlit auto-refresh supported (30s interval).

---

## 📄 License
MIT License © 2025 
