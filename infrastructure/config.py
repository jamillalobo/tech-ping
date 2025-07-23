import os
from dotenv import load_dotenv
from apify_client import ApifyClient
from langchain_google_genai import GoogleGenerativeAI
import telebot
from newsapi import NewsApiClient

load_dotenv()

class Config:
    """
    Configuration class that manages all API keys and client instances.
    
    This class centralizes all configuration management and provides 
    singleton-like access to various API clients. It validates that
    all required environment variables are present at startup.
    """
    
    def __init__(self):
        self.api_token_telegram = os.getenv("API_TOKEN_TELEGRAM")
        if not self.api_token_telegram:
            raise ValueError("API_TOKEN_TELEGRAM environment variable is required")
            
        self.chat_id = os.getenv("CHAT_ID")
        if not self.chat_id:
            raise ValueError("CHAT_ID environment variable is required")
        
        self.api_token_apify = os.getenv("API_TOKEN_APIFY")
        if not self.api_token_apify:
            raise ValueError("API_TOKEN_APIFY environment variable is required")
        
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        if not self.gemini_api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")

        self.api_key_news = os.getenv("NEWS_API_KEY")
        if not self.api_key_news:
            raise ValueError("NEWS_API_KEY environment variable is required")

        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        
    @property
    def apify_client(self) -> ApifyClient:

        return ApifyClient(self.api_token_apify)

    @property
    def chat_gemini(self) -> GoogleGenerativeAI:

        return GoogleGenerativeAI(
            model="gemini-2.5-flash", 
            google_api_key=self.gemini_api_key
        )

    @property
    def bot_telegram(self) -> telebot.TeleBot:
        return telebot.TeleBot(self.api_token_telegram)
    
    @property
    def news_collector(self) -> NewsApiClient:
        return NewsApiClient(api_key=self.api_key_news)

cfg = Config()