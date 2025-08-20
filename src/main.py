import schedule
import time
import logging
from config import Config
from services.bot import TelegramBot
from services.news_collector import NewsCollector
from services.summarize import Summarizer
from services.tweet_scraper import ScraperTwitter
from utils.logger import setup_logging
from pytz import timezone

def collect_and_send_trends() -> bool:
    try:
        logging.info("=" * 50)
        logging.info("Starting tech trends collection and summary process")
        
        cfg = Config()

        twitter_scraper = ScraperTwitter(cfg.apify_client)
        news_collector = NewsCollector(cfg.news_collector)
        summarizer = Summarizer(cfg.chat_gemini)
        telegram_bot = TelegramBot(cfg.bot_telegram, cfg.chat_id)
        
        logging.info("🤖 Collecting tweets...")
        tweets = twitter_scraper.scrape_twitter(max_tweets=15)
        if not tweets:
            logging.warning("No tweets collected, continuing with news only")
        
        logging.info("🤖 Collecting tech news...")
        news = news_collector.get_news(max_articles=15)
        if not news:
            logging.warning("No news articles collected")

        if not tweets and not news:
            logging.error("No content collected from either source")
            return False
        
        logging.info("🤖Generating AI summary...")
        summary_result = summarizer.summarize_trends(tweets, news)
        
        if not summary_result:
            logging.error("Failed to generate summary")
            return False
        
        logging.info(f"Generated summary with {len(summary_result.summaries)} trend items")
        
        logging.info("🤖 Sending summary to Telegram...")
        send_success = telegram_bot.send_message(summary_result)
        
        if send_success:
            logging.info("✅ Tech trends sent successfully!")
            return True
        else:
            logging.error("❌ Failed to send message to Telegram")
            return False
            
    except Exception as e:
        logging.error(f"Error in collect_and_send_trends: {e}", exc_info=True)
        return False

def schedule_jobs():
    schedule.every().day.at("09:00", timezone("America/Sao_Paulo")).do(
        lambda: collect_and_send_trends()
    ).tag('morning_update')

    schedule.every().day.at("21:00", timezone("America/Sao_Paulo")).do(
        lambda: collect_and_send_trends()
    ).tag('evening_update')
    
    logging.info("✅ Scheduled jobs:")
    logging.info(" Morning update: 9:00 AM daily")
    logging.info(" Evening update: 21:00 PM daily")

def main():
    print("🚀 Starting Tech Ping Bot...")

    setup_logging()
    logging.info("Tech Ping Bot starting up...")
    
    try:
        logging.info("✅ Configuration loaded successfully")

        schedule_jobs()

        logging.info("🤖 Tech Ping Bot is now running...")
        logging.info("Press Ctrl+C to stop the bot")
        
        while True:
            schedule.run_pending()
            time.sleep(10)
            
    except KeyboardInterrupt:
        logging.info("🛑 Tech Ping Bot stopped by user")
        
    except Exception as e:
        logging.error(f"💥 Fatal error: {e}", exc_info=True)
        print(f"\n💥 Fatal error: {e}")

if __name__ == "__main__":
    main()