# 🧠 Crypto News Sentiment Analyzer

A real-time crypto news analysis app built with **Streamlit**, that fetches live news articles, analyzes sentiment using **VADER NLP**, and provides interactive **visualizations** and **filtering** tools.

> 💼 Ideal for traders, analysts, and crypto enthusiasts looking to stay ahead with sentiment insights.

---

## 🚀 Demo

🔗 [Live App on Streamlit](https://crypto-sentiment-analyzer-app.streamlit.app/)

---

## ⚙️ Features

- 🔍 **Live crypto news** fetched via [NewsAPI.org](https://newsapi.org/)
- 🧠 **Sentiment analysis** using VADER NLP
- 🎛 Sidebar filters: Sentiment type, Source, Score threshold
- 📈 Visualizations:
  - Sentiment over time
  - Score histogram
  - Source heatmap
  - Donut chart
- 📰 Detailed news view with description + sentiment
- 📤 Export filtered news as JSON

---

## 🧰 Tech Stack

- Python
- Streamlit
- Pandas, Requests
- VADER Sentiment (NLTK)
- Matplotlib, Seaborn

---

## 🔐 Environment Setup

### 1. Clone the repo

```bash
1)git clone https://github.com/PriyanshuYadav09/Crypto-Sentiment-Analyzer
2)cd crypto-sentiment-analyzer
3)pip install -r requirements.txt
4)NEWS_API_KEY = "your_newsapi_key"
5)streamlit run main.py



