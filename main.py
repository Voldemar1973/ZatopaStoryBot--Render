import os
import telebot
from flask import Flask

TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(TOKEN, parse_mode='Markdown')
app = Flask(__name__)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(telebot.types.InlineKeyboardButton("1 грн підписка", url="https://secure.wayforpay.com/sub/Shvudka"))
    keyboard.add(telebot.types.InlineKeyboardButton("🎮 Гра Потопмен", url="https://zatopamen.fun/game"))
    keyboard.add(telebot.types.InlineKeyboardButton("📜 Правила", callback_data="rules"))
    bot.send_message(message.chat.id, 
                     "Привіт! 👋 Надішли свою історію затоплення (фото/відео) і отримай шанс виграти iPhone 16!",
                     reply_markup=keyboard)

@bot.callback_query_handler(func=lambda c: c.data == "rules")
def send_rules(c):
    text = ("📜 *Правила челенджу ZatopaStory*\n\n"
            "1. Надіслати історію затоплення (фото/відео).\n"
            "2. Найцікавіші публікуються.\n"
            "3. Головний приз – iPhone 16.\n"
            "4. Підписка – 1 грн на місяць, захист і бонуси.\n\n"
            "➡ Після /start можна підписатися і грати.")
    bot.send_message(c.message.chat.id, text)

@bot.message_handler(content_types=['photo', 'video', 'text'])
def forward_story(msg):
    chat_id = os.getenv("ARCHIVE_CHAT", "")
    caption = msg.caption if hasattr(msg, 'caption') else ''
    if msg.content_type == 'photo':
        bot.send_photo(chat_id, msg.photo[-1].file_id, caption=caption)
    elif msg.content_type == 'video':
        bot.send_video(chat_id, msg.video.file_id, caption=caption)
    elif msg.content_type == 'text':
        bot.send_message(chat_id, msg.text)
    bot.reply_to(msg, "Дякую — твоя історія прийнята!")

def run_bot():
    bot.infinity_polling()

if __name__ == '__main__':
    from threading import Thread
    Thread(target=run_bot).start()
    app.run(host='0.0.0.0', port=int(os.getenv("PORT", 5000)))
