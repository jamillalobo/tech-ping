import logging
from typing import List, Dict, Any

class ScraperTwitter:
    def __init__(self):
        from infrastructure.config import cfg
        self.client = cfg.apify_client

    def scrape_twitter(self, max_tweets: int = 10) -> List[str]:
        try:
            scraper_input = {
                "customMapFunction": "(object) => { return {...object} }",
                "includeSearchTerms": True,
                "maxItems": max_tweets,
                "onlyImage": False,
                "onlyQuote": False,
                "onlyTwitterBlue": False,
                "onlyVerifiedUsers": False,
                "onlyVideo": False,
                "searchTerms": [
                    "artificial intelligence", "machine learning",
                    "ChatGPT", "OpenAI", "GPT", "AI tools",
                    "tech startup", "programming", "software development",
                    "mobile app", "web development", "frontend", "backend",
                ],
                "sort": "Latest",
                "tweetLanguage": "en",
                "twitterHandles": [
                    "leerob",  
                    "t3dotgg",        
                    "karpathy", 
                    "karpathy",        
                    "ylecun",          
                    "github",         
                    "GoogleAI",        
                    "OpenAI",          
                    "techcrunch",      

                ]
            }
            
            logging.info(f"Starting Twitter scraping for {max_tweets} tweets...")

            run = self.client.actor("xtdata/twitter-x-scraper").call(run_input=scraper_input)
            
            if not run or "defaultDatasetId" not in run:
                logging.error("Failed to get dataset ID")
                return []
            
            dataset_id = run["defaultDatasetId"]
            logging.info(f"Scraping completed! Processing dataset {dataset_id}")

            tweets = list(self.client.dataset(dataset_id).iterate_items())
            
            if not tweets:
                logging.warning("No tweets found in the dataset")
                return []

            result = []
            for tweet in tweets:
                try:
                    if not tweet.get('full_text'):
                        continue

                    tweet_text = tweet.get("full_text", tweet.get("text", ""))
                    tweet_url = tweet.get("url", "")
                    
                    if tweet_text and len(tweet_text.strip()) > 20:  
                        cleaned_text = " ".join(tweet_text.split())

                    if len(tweet_text) < 30 or len(tweet_text) > 280:
                        continue

                    formatted_tweet = {
                        "text": cleaned_text,
                        "url": tweet_url
                    }

                    result.append(formatted_tweet)
                        
                except Exception as e:
                    logging.warning(f"Error processing individual tweet: {e}")
                    continue
            
            logging.info(f"Successfully extracted {len(result)} tweets")
            return result[:max_tweets] 
            
        except Exception as e:
            logging.error(f"Error scraping Twitter: {e}")
            return []

