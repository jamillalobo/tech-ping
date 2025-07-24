import sys
import os

from src.models.summary import Summary, SummaryList
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_config():
    print("🔧 Testing configuration...")
    try:
        from src.config import cfg
        print("✅ Configuration loaded successfully")
        print(f"   - Telegram chat ID: {cfg.chat_id[:5]}...")
        return True
    except Exception as e:
        print(f"❌ Configuration failed: {e}")
        return False

def test_news_collector():
    print("\n📰 Testing news collection...")
    try:
        from src.services.news_collector import NewsCollector
        
        collector = NewsCollector()
        articles = collector.get_news(max_articles=5)
        
        if articles:
            print(f"✅ Collected {len(articles)} news articles")
            print(f"   - First article: {articles[0]['title'][:50]}...")
            return True
        else:
            print("⚠️  No articles collected (might be API limits)")
            return False
            
    except Exception as e:
        print(f"❌ News collection failed: {e}")
        return False

def test_twitter_scraper():
    print("\n🐦 Testing Twitter scraping...")
    try:
        from src.services.tweet_scraper import ScraperTwitter
        
        scraper = ScraperTwitter()
        tweets = scraper.scrape_twitter(max_tweets=3)
        
        if tweets:
            print(f"✅ Collected {len(tweets)} tweets")
            print(f"   - First tweet: {tweets[0][:50]}...")
            return True
        else:
            print("⚠️  No tweets collected (might be API limits)")
            return False
            
    except Exception as e:
        print(f"❌ Twitter scraping failed: {e}")
        return False

def test_summarizer():
    print("\n🧠 Testing AI summarization...")
    try:
        from src.services.summarize import Summarizer
        
        summarizer = Summarizer()
        sample_tweets = [
            "Exciting news about AI developments in machine learning!",
            "New framework released for web development.",
            "Breakthrough in quantum computing research."
        ]
        
        sample_news = [
            {
                "title": "AI Revolution in Tech",
                "text": "Artificial intelligence is transforming the technology landscape with new innovations.",
                "url": "https://example.com/ai-news"
            }
        ]
        
        summary = summarizer.summarize_trends(sample_tweets, sample_news)
        
        if summary and summary.summaries:
            print(f"✅ Generated {len(summary.summaries)} trend summaries")
            print(f"   - First trend: {summary.summaries[0].title}")
            return True
        else:
            print("❌ Failed to generate summaries")
            return False
            
    except Exception as e:
        print(f"❌ AI summarization failed: {e}")
        return False

def test_telegram_bot():
    print("\n📱 Testing Telegram bot initialization...")
    try:
        from src.services.bot import TelegramBot

        bot = TelegramBot()

        sample_summaries = SummaryList(summaries=[
            Summary(
                title="Test Tech Trend",
                description="This is a test description for formatting."
            )
        ])
        
        formatted_message = bot.format_summaries(sample_summaries)
        
        if formatted_message and "Test Tech Trend" in formatted_message:
            print("✅ Telegram bot initialized and message formatting works")
            print("   - Message preview:", formatted_message[:100] + "...")
            return True
        else:
            print("❌ Message formatting failed")
            return False
            
    except Exception as e:
        print(f"❌ Telegram bot test failed: {e}")
        return False

def main():
    print("🧪" + "="*50 + "🧪")
    print("        TECH PING BOT - COMPONENT TESTS")
    print("🤖" + "="*50 + "🤖")
    
    tests = [
        ("Configuration", test_config),
        ("News Collector", test_news_collector),
        ("Twitter Scraper", test_twitter_scraper),
        ("AI Summarizer", test_summarizer),
        ("Telegram Bot", test_telegram_bot),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except KeyboardInterrupt:
            print("\n🛑 Tests interrupted by user")
            break
        except Exception as e:
            print(f"❌ Unexpected error in {test_name}: {e}")
            results[test_name] = False
    
    # Summary
    print("\n" + "="*50)
    print("📊 TEST RESULTS SUMMARY:")
    print("="*50)
    
    passed = sum(results.values())
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:20} | {status}")
    
    print("="*50)
    print(f"📈 TOTAL: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your bot is ready to run!")
    else:
        print("⚠️  Some tests failed. Check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    main() 