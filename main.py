
from aiogram import Bot, Dispatcher, executor, types
import logging
import os

API_TOKEN = '8124924572:AAE0LeFfmulT-1ny-d3za98BlQ_MuSRsXVU'
WAYFORPAY_LINK = 'https://secure.wayforpay.com/sub/Shvudka'
ADMIN_ID = 123456789  # ← ЗАМІНИ на свій Telegram ID

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
        types.InlineKeyboardButton("📜 Правила челенджу", callback_data="rules"),
        types.InlineKeyboardButton("🔐 Підписка Shvudka", url=WAYFORPAY_LINK)
    )
    await message.answer(
        "Привіт! 👋\nТебе колись затоплювали? Або ти когось? 😅\nПоділись історією та виграй iPhone 16 📱\n\nНадішли свою історію у вигляді тексту, фото або відео.",
        reply_markup=keyboard
    )

@dp.message_handler(commands=['rules'])
async def show_rules_cmd(message: types.Message):
    await send_rules(message)

@dp.message_handler(commands=['subscribe'])
async def send_subscribe(message: types.Message):
    await message.answer("🔐 Оформити підписку за 1 грн:", reply_markup=subscription_keyboard())

@dp.message_handler(commands=['support'])
async def send_support(message: types.Message):
    await message.answer("✉ З усіх питань пиши @YourSupportUsername або на email support@shvudka.com")

@dp.callback_query_handler(lambda c: c.data == 'rules')
async def send_rules(callback_query: types.CallbackQuery):
    rules_text = (
        "📜 *Правила челенджу 'ZatopaStory'*\n\n"
        "1. Надішли свою історію про затоплення (можна текст, фото або відео).\n"
        "2. Найцікавіші історії потрапляють до публічного голосування.\n"
        "3. Переможець отримає *iPhone 16* 📱\n"
        "4. Більше історій — більше шансів!\n"
        "5. Підписка на сервіс *Shvudka* — це ще один плюс до твоїх шансів 😉\n\n"
        "🗓 Результати — 15 вересня! Успіхів!"
    )
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, rules_text, parse_mode='Markdown')

@dp.message_handler(content_types=['text', 'photo', 'video'])
async def handle_submission(message: types.Message):
    if ADMIN_ID:
        try:
            await message.copy_to(chat_id=ADMIN_ID)
        except:
            await message.answer("⚠ Не вдалося передати історію адміну. Повідом нас про помилку через /support")

    await message.answer(
        "Дякуємо! Твоя історія збережена 🙌\n\nХочеш більше шансів на виграш і захист, якщо знову затопить?\n\n🚨 Підключи Shvudka — сервіс швидкої допомоги при затопленнях:\n✔ Юрист\n✔ Прибирання\n✔ Осушення\n✔ Озонування\n✔ Антипліснява\n\n🎁 Перший місяць всього за 1 грн!",
        reply_markup=subscription_keyboard()
    )

def subscription_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton("🔐 Оформити підписку за 1 грн", url=WAYFORPAY_LINK)
    keyboard.add(button)
    return keyboard

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
