import logging
import telebot
from domain.entities.summary import SummaryList

class TelegramBot:
    def __init__(self, bot_telegram: telebot.TeleBot, chat_id: str):
        self.bot = bot_telegram
        self.default_chat_id = chat_id
        logging.info("Telegram bot initialized successfully")

    def format_summaries(self, summaries: SummaryList) -> str:
        if not summaries or not summaries.summaries:
            return "No tech trends found today. 🤖"
        
        message = "🚀 **Daily Tech Trends Update** 🚀\n\n"
        
        for i, summary in enumerate(summaries.summaries, 1):
            message += f"**{i}. {summary.title}**\n"
            message += f"- {summary.description}\n"
            message += f" Link: {summary.url}\n\n"
        
        message += "---\n🤖 Powered by Tech Ping Bot"
        return message

    def send_message(self, summaries: SummaryList) -> bool:
        try:
            message_text = self.format_summaries(summaries)
            
            self.bot.send_message(
                chat_id=self.default_chat_id,
                text=message_text,
                parse_mode='Markdown'
            )
            
            logging.info(f"Message sent successfully to chat!")
            return True
            
        except telebot.apihelper.ApiException as e:
            logging.error(f"Telegram API error: {e}")
            return False
        except Exception as e:
            logging.error(f"Unexpected error sending message: {e}")
            return False

    def start_polling(self):
        try:
            logging.info("Starting Telegram bot polling...")
            self.bot.infinity_polling()
        except Exception as e:
            logging.error(f"Error in bot polling: {e}")