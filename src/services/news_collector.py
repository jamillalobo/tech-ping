from datetime import datetime, timedelta
import logging
from typing import List, Dict, Any

from newsapi import NewsApiClient

from models.article import News

class NewsCollector:
    def __init__(self, news_collector: NewsApiClient):
        self.newsapi = news_collector

    def get_news(self, max_articles: int = 20) -> List[Dict[str, Any]]:
        try:
            now = datetime.now().date()
            yesterday = now - timedelta(days=1)
            
            logging.info(f"Fetching news from {yesterday} to {now}")
            
            all_articles = self.newsapi.get_everything(
                q='("artificial intelligence" OR "machine learning" OR "tech startup" OR "software" OR "programming" OR "gemini" OR "openai" OR "llm" OR "framework")',
                sources='techcrunch,the-verge,ars-technica,wired,engadget,bbc-news,google-news',
                domains='techcrunch.com,theverge.com,arstechnica.com,wired.com,engadget.com,bbc.co.uk,google.com',
                from_param=yesterday.isoformat(),
                to=now.isoformat(),
                language='en',
                sort_by='relevancy',
                page_size=min(max_articles, 100) 
            )
            
            if not all_articles or not all_articles.get('articles'):
                logging.warning("No articles found from NewsAPI")
                return []
            
            formatted_articles = []
            for article in all_articles['articles'][:max_articles]:
                if not article.get('content') or len(article['content']) < 50:
                    continue
                    
                formatted_article: News = {
                    "title": article.get("title", "No Title"),
                    "text": article.get("content", "No Content"),
                    "url": article.get("url", ""),
                }
                formatted_articles.append(formatted_article)
            
            logging.info(f"Successfully collected {len(formatted_articles)} news articles")
            
            return self.filter_tech_keywords(formatted_articles)
            
        except Exception as e:
            logging.error(f"Error fetching news: {e}")
            return []

    def filter_tech_keywords(self, articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        tech_keywords = [
            'ai', 'artificial intelligence', 'machine learning',
            'startup', 'tech', 'software', 'programming', 'developer',
            'cloud', 'automation', 'mobile app', 'web development', 'api', 'framework', 'llm', 'gemini', 'openai', 'google'
        ]
        
        filtered_articles = []
        for article in articles:
            article_text = (article.get('title', '') + ' ' + article.get('text', '')).lower()
            
            if any(keyword in article_text for keyword in tech_keywords):
                filtered_articles.append(article)
        
        logging.info(f"Filtered {len(articles)} articles down to {len(filtered_articles)} tech-relevant articles")
        return filtered_articles

