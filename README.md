# 🤖 Tech Ping Bot

A smart Telegram bot that delivers tech trend updates twice daily by analyzing tweets from tech influencers and latest tech news articles using AI summarization.

## ✨ Features

- **Twice Daily Updates**: Automatic delivery at 9:00 AM and 9:00 PM
- **Twitter Intelligence**: Scrapes tweets from top tech influencers and trending topics
- **News Aggregation**: Collects latest articles from premier tech news sources
- **AI Summarization**: Uses Google Gemini AI to create concise, relevant summaries

## 🏗️ Project Structure

```
tech-ping/
├── src/
│   ├── main.py                       
│   ├── config.py                     
│   ├── services/
│   │   ├── twitter_scraper.py       
│   │   ├── news_collector.py        
│   │   ├── summarizer.py            
│   │   └── bot.py             
│   ├── models/
│   │   └── summary.py 
│   │   └── article.py               
│   ├── utils/
│   │   ├── formatter.py            
│   │   └── logger.py                
│   └── constants.py                 
├── tests/
│   └── ...                          
├── requirements.txt
└── README.md
```

## 🚀 Quick Start

### 1. Clone and Setup

```bash
git clone https://github.com/jamillalobo/tech-ping
cd tech-ping
pip install -r requirements.txt
```

### 2. Create Environment File

```bash
cp .env.example .env
```

### 3. Configure API Keys

Edit the `.env` file with your API credentials:

#### 🤖 Telegram Bot Setup
1. Message [@BotFather](https://t.me/botfather) on Telegram
2. Create a new bot with `/newbot`
3. Copy the API token to `API_TOKEN_TELEGRAM`
4. Get your chat ID:
   - Create a groupchat with your bot
   - Copy the chat ID from the chat url (using starts with -)

#### 🔍 Apify Setup (Twitter Scraping)
1. Sign up at [Apify.com](https://apify.com/)
2. Get your API token from the [Integrations page](https://console.apify.com/account/integrations)
3. Add it to `API_TOKEN_APIFY`

#### 🧠 Google Gemini AI Setup
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create an API key
3. Add it to `GEMINI_API_KEY`

#### 📰 NewsAPI Setup
1. Sign up at [NewsAPI.org](https://newsapi.org/)
2. Get your free API key
3. Add it to `NEWS_API_KEY`

### 4. Run the Bot

```bash
cd src
python main.py
```

## 🎯 Usage

### Scheduled Operation
The bot runs automatically with scheduled updates:
- **9:00 AM**: Morning tech trends digest
- **9:00 PM**: Evening tech trends summary

### Monitoring
- Check `tech_ping_bot.log` for detailed operation logs
- Console output shows real-time status
- All errors are logged with full stack traces

## 🔧 Configuration Options

#### Schedule Times
Edit `src/main.py` to change update times:
```python
schedule.every().day.at("09:00").do(...)  # Change times here
schedule.every().day.at("21:00").do(...)
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes with proper comments
4. Add tests if applicable
5. Submit a pull request

## 📝 Contribuições
Contributions are welcome! Feel free to open issues and send pull requests.

---
Developed by Jamilla Lobo <♡︎/>