# app.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import json

from fetch_news import fetch_crypto_news
from sentiment import analyze_sentiment

# Page config
st.set_page_config(page_title="Crypto News Sentiment Analyzer", layout="wide")

st.title("🧠 Crypto News Sentiment Analyzer")
st.write("Get real-time sentiment from recent crypto news articles.")

# Input section
with st.form("query_form"):
    query = st.text_input("🔍 Search Keyword", value="crypto")
    days = st.slider("🗓️ How many days of news?", 1, 7, 1)
    fetch_clicked = st.form_submit_button("Fetch News")

# Fetch News
if fetch_clicked:
    with st.spinner("Fetching news..."):
        articles = fetch_crypto_news(query=query, days=days)

        data = []
        for article in articles:
            sentiment, score = analyze_sentiment(article["title"])
            data.append({
                "Title": article["title"],
                "Source": article["source"]["name"],
                "Sentiment": sentiment,
                "Score": round(score, 3),
                "Published At": article["publishedAt"][:10],
                "URL": article["url"],
                "Description": article.get("description", "")
            })

        df = pd.DataFrame(data)
        st.session_state["news_df"] = df  # Cache the full dataset

# Render UI if data is available
if "news_df" in st.session_state:
    df = st.session_state["news_df"]

    # Sidebar Filters
    st.sidebar.markdown("## 🎛 Filter Options")

    sentiment_options = df["Sentiment"].unique().tolist()
    source_options = df["Source"].unique().tolist()

    selected_sentiments = st.sidebar.multiselect(
        "Sentiment Type", options=sentiment_options, default=sentiment_options
    )

    selected_sources = st.sidebar.multiselect(
        "News Sources", options=source_options, default=source_options
    )

    min_score = st.sidebar.slider(
        "Minimum Sentiment Score", min_value=-1.0, max_value=1.0, value=-1.0, step=0.1
    )

    if st.sidebar.button("🔄 Reset Filters"):
        st.experimental_rerun()

    # Apply filters
    filtered_df = df[
        (df["Sentiment"].isin(selected_sentiments)) &
        (df["Source"].isin(selected_sources)) &
        (df["Score"] >= min_score)
    ]

    st.markdown(f"### 🔍 Filtered News Results ({len(filtered_df)} articles)")
    st.dataframe(filtered_df[["Title", "Source", "Sentiment", "Score"]], use_container_width=True)

    st.divider()

    # Top Sentiment Articles
    st.subheader("📈 Top 3 Bullish Headlines")
    top_bullish = filtered_df[filtered_df["Sentiment"] == "Bullish"].sort_values("Score", ascending=False).head(3)
    if top_bullish.empty:
        st.info("No bullish news found.")
    else:
        for _, row in top_bullish.iterrows():
            st.markdown(f"**🔹 {row['Title']}**  \n[Read more]({row['URL']}) — Score: `{row['Score']}`")

    st.subheader("📉 Top 3 Bearish Headlines")
    top_bearish = filtered_df[filtered_df["Sentiment"] == "Bearish"].sort_values("Score", ascending=True).head(3)
    if top_bearish.empty:
        st.info("No bearish news found.")
    else:
        for _, row in top_bearish.iterrows():
            st.markdown(f"**🔻 {row['Title']}**  \n[Read more]({row['URL']}) — Score: `{row['Score']}`")

    st.divider()

    # Limit expanders
    st.subheader("📰 Expand for Full Article Details")
    max_display = st.slider("How many articles to show below?", 5, min(30, len(filtered_df)), 10)

    for _, row in filtered_df.head(max_display).iterrows():
        with st.expander(f"{row['Title']}"):
            st.write(f"**Sentiment:** {row['Sentiment']}  \n"
                     f"**Score:** {row['Score']}  \n"
                     f"**Published:** {row['Published At']}  \n"
                     f"**Source:** {row['Source']}")
            st.write(row.get("Description", "No description available."))
            st.markdown(f"[🔗 Read Full Article]({row['URL']})", unsafe_allow_html=True)

    st.divider()

    # Charts
    import seaborn as sns

    st.subheader("📊 Sentiment Breakdown")

    sentiment_counts = filtered_df['Sentiment'].value_counts()

# Bar chart (compact)
    st.markdown("#### 📶 Bar Chart")
    fig_bar, ax_bar = plt.subplots(figsize=(5, 2.5))
    sns.barplot(
        x=sentiment_counts.index,
        y=sentiment_counts.values,
        ax=ax_bar,
        palette="pastel"
    )
    ax_bar.set_ylabel("Count")
    ax_bar.set_xlabel("Sentiment")
    ax_bar.set_title("Sentiment Distribution", fontsize=10)
    st.pyplot(fig_bar)

# Pie chart (compact)
    st.markdown("#### 🥧 Pie Chart")
    fig_pie, ax_pie = plt.subplots(figsize=(3.5, 3.5))
    ax_pie.pie(
        sentiment_counts.values,
        labels=sentiment_counts.index,
        autopct='%1.1f%%',
        colors=['#2ecc71', '#e74c3c', '#f1c40f'],
        startangle=140,
        textprops={'fontsize': 8}
    )
    ax_pie.axis('equal')
    st.pyplot(fig_pie)
    
    st.expander("📈 Show Visualization Tools")
    
    st.divider()
if "news_df" in st.session_state:
    df = st.session_state["news_df"]
    sentiment_counts = df["Sentiment"].value_counts()

    st.divider()
    st.subheader("📊 Explore More Visualizations")

    selected_viz = st.radio(
        "Choose a chart to display:",
        [
            "📈 Sentiment Over Time",
            "🧭 Sentiment Score Distribution",
            "📰 Sentiment by Source (Heatmap)",
            "🥯 Sentiment Donut Chart"
        ],
        horizontal=False
    )

    if selected_viz == "📈 Sentiment Over Time":
        st.markdown("#### 📈 Average Sentiment Score Over Time")
        df["Published At"] = pd.to_datetime(df["Published At"])
        trend_data = df.groupby("Published At")["Score"].mean().reset_index()

        fig, ax = plt.subplots(figsize=(6, 3))
        sns.lineplot(data=trend_data, x="Published At", y="Score", marker="o", ax=ax)
        ax.set_ylabel("Average Score")
        ax.set_xlabel("Date")
        st.pyplot(fig)

    elif selected_viz == "🧭 Sentiment Score Distribution":
        st.markdown("#### 📊 Sentiment Score Histogram")
        fig, ax = plt.subplots(figsize=(6, 3))
        sns.histplot(df["Score"], bins=20, kde=True, ax=ax, color="skyblue")
        ax.set_xlabel("Sentiment Score")
        st.pyplot(fig)

    elif selected_viz == "📰 Sentiment by Source (Heatmap)":
        st.markdown("#### 📰 Heatmap: Sentiment Count by News Source")
        heatmap_data = df.pivot_table(
            index="Source", columns="Sentiment", values="Score", aggfunc="count", fill_value=0
        )
        fig, ax = plt.subplots(figsize=(7, 4))
        sns.heatmap(heatmap_data, annot=True, fmt="d", cmap="YlOrBr", ax=ax)
        st.pyplot(fig)

    elif selected_viz == "🥯 Sentiment Donut Chart":
        st.markdown("#### 🥯 Donut Chart: Sentiment Share")
        fig, ax = plt.subplots(figsize=(3.5, 3.5))
        wedges, texts, autotexts = ax.pie(
            sentiment_counts.values,
            labels=sentiment_counts.index,
            autopct='%1.1f%%',
            colors=['#2ecc71', '#e74c3c', '#f1c40f'],
            startangle=140,
            wedgeprops={'width': 0.4}
        )
        ax.axis('equal')
        st.pyplot(fig)

else:
    st.warning("⚠️ Please fetch news first to see visualizations.")



    st.divider()

    # JSON Export
if "news_df" in st.session_state:
    st.markdown("---")
    st.subheader("📤 Export Sentiment Data")

    json_data = filtered_df.to_json(orient="records", indent=2)
    st.download_button(
        label="⬇️ Download JSON",
        data=json_data,
        file_name="crypto_sentiment_data.json",
        mime="application/json"
    )
else:
    st.warning("⚠️ Fetch news first to enable export.")



