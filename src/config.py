from functools import cached_property
import os
from dotenv import load_dotenv
from apify_client import ApifyClient
from langchain_google_genai import GoogleGenerativeAI
import telebot
from newsapi import NewsApiClient

load_dotenv()

class Config:
    def __init__(self):
        self.validate()

    def validate(self):
        items = [
            'API_TOKEN_TELEGRAM',
            'CHAT_ID', 
            'API_TOKEN_APIFY', 
            'GEMINI_API_KEY', 
            'NEWS_API_KEY'
        ]
        for var in items:
            if not os.getenv(var):
                raise ValueError(f"{var} environment variable is required")
        
    @cached_property
    def apify_client(self) -> ApifyClient:
        return ApifyClient(os.getenv('API_TOKEN_APIFY'))

    @cached_property
    def chat_gemini(self) -> GoogleGenerativeAI:
        return GoogleGenerativeAI(
            model="gemini-2.5-flash", 
            google_api_key=os.getenv('GEMINI_API_KEY')
        )

    @cached_property
    def bot_telegram(self) -> telebot.TeleBot:
        return telebot.TeleBot(os.getenv('API_TOKEN_TELEGRAM'))
    
    @cached_property
    def news_collector(self) -> NewsApiClient:
        return NewsApiClient(api_key=os.getenv('NEWS_API_KEY'))
    
    @cached_property
    def chat_id(self) -> str:
        return os.getenv('CHAT_ID')

    @property
    def log_level(self) -> str:
        return os.getenv("LOG_LEVEL", "INFO")
    