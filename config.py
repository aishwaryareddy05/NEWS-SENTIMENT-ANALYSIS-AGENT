from pathlib import Path
import os

# Default values
DEFAULT_QUERY = "technology"
DEFAULT_REFRESH_INTERVAL = 30

# Sentiment thresholds
POSITIVE_THRESHOLD = 0.1
NEGATIVE_THRESHOLD = -0.1
INSIGHT_POS_THRESHOLD = 0.2
INSIGHT_NEG_THRESHOLD = -0.2
NEGATIVE_COVERAGE_RATIO = 0.3

# CSS file location
STYLE_PATH = Path(__file__).parent / "styles.css"


TOPIC_KEYWORDS = {
    'technology': ['ai', 'tech', 'digital', 'software', 'computer', 'internet', 'cyber'],
    'business': ['stock', 'market', 'business', 'finance', 'economy', 'trade'],
    'health': ['health', 'medical', 'hospital', 'doctor', 'medicine', 'covid'],
    'environment': ['climate', 'environment', 'renewable', 'green', 'pollution'],
    'politics': ['government', 'political', 'election', 'policy', 'congress'],
    'sports': ['sport', 'game', 'team', 'player', 'match', 'tournament'],
    'entertainment': ['movie', 'music', 'celebrity', 'entertainment', 'film']
}
