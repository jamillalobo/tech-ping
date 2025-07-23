import logging
from typing import List, Dict, Any
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.exceptions import OutputParserException
from langchain_google_genai import GoogleGenerativeAI
from utils.helpers import format_prompt_text
from domain.entities.summary import SummaryList

PROMPT_INSTRUCTION = """
You are analyzing tech trends from recent tweets and nws articles.

TWEETS DATA:
{tweets}

NEWS DATA:
{news}

IMPORTANT: return your response in this EXACT JSON format:
{{
    "summaries": [
        {{
            "title": "Title of the summary",
            "description": "Description of the summary",
            "url": "URL of the summary"
        }},
}}

Return ONLY the JSON, no other text.
"""

parser = PydanticOutputParser(pydantic_object=SummaryList)


class Summarizer:
    def __init__(self, chat_gemini: GoogleGenerativeAI):
        self.llm = chat_gemini

    def format_news_prompt(self, news: List[Dict[str, Any]]) -> str:
        return format_prompt_text(news, ["title", "description", "url"], "No news available")
    

    def format_tweets_prompt(self, tweets: List[Dict[str, Any]]) -> str:
        return format_prompt_text(tweets, ["text", "url"], "No tweets available")

    def summarize_trends(self, tweets: List[Dict[str, Any]], news: List[Dict[str, Any]]) -> SummaryList:
        formatted_news = self.format_news_prompt(news)
        formatted_tweets = self.format_tweets_prompt(tweets)
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful AI bot. Your name is Tech Ping."),
            ("human", PROMPT_INSTRUCTION)
        ])

        try: 
            prompt_with_instructions = prompt.partial(format_instructions=parser.get_format_instructions())
            chain = prompt_with_instructions | self.llm | parser

            response = chain.invoke({
                "tweets": formatted_tweets,
                "news": formatted_news
            })

            if response and hasattr(response, "summaries") and response.summaries:
                return response
            else:
                logging.error("Response is not a valid SummaryList object")
                return None
        
        except OutputParserException as e:
            logging.error("Error parsing response: %s", e.args[0])
            return None


    
