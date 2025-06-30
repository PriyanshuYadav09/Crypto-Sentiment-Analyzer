# fetch_news.py
import requests
from config import NEWS_API_KEY
from datetime import datetime, timedelta

def fetch_crypto_news(query="crypto", days=1, max_pages=3):
    url = "https://newsapi.org/v2/everything"
    from_date = datetime.now() - timedelta(days=days)

    all_articles = []

    max_allowed_results = 100       # NewsAPI free-tier limit
    results_per_page = 50           # You’re using 50 per page
    max_pages = min(max_pages, max_allowed_results // results_per_page)  # Max 2 pages

    for page in range(1, max_pages + 1):
        params = {
            "q": query,
            "sortBy": "publishedAt",
            "language": "en",
            "apiKey": NEWS_API_KEY,
            "pageSize": results_per_page,
            "page": page,
        }

        response = requests.get(url, params=params)
        data = response.json()

        if data.get("status") != "ok":
            print("❌ NewsAPI error:", data)
            break

        for article in data.get("articles", []):
            pub_date = datetime.strptime(article["publishedAt"], "%Y-%m-%dT%H:%M:%SZ")
            if pub_date >= from_date:
                all_articles.append(article)

    return all_articles


