# app.py
from news_api import get_news
from utils import display_news

def main():
    print("📰 News Categories")
    print("business | entertainment | general | health | science | sports | technology\n")

    category = input("Enter the type of headlines you want: ").lower()

    print(f"\n🔍 Fetching {category} news...\n")
    news_data = get_news(category)
    display_news(news_data)

if __name__ == "__main__":
    main()
