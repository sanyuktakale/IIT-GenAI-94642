# utils.py

def display_news(data):
    if data.get("status") != "ok":
        print(" Failed to fetch news")
        return

    if not data["articles"]:
        print("⚠ No articles found for this category")
        return

    for article in data["articles"]:
        print("-" * 50)
        print(f"Title : {article['title']}")
        print(f"Source: {article['source']['name']}")
        
