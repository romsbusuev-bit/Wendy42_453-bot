import os
import telebot
from telebot import types

# ================== НАСТРОЙКИ ==================
BOT_TOKEN = os.environ.get("BOT_TOKEN")  # берём из переменных окружения (Render)

YOUTUBE_URL = "https://www.youtube.com/@Wendy42_453"
TELEGRAM_URL = "https://t.me/Wendy42_453"
# ================================================

bot = telebot.TeleBot(BOT_TOKEN)


def main_menu():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row("📺 YouTube", "📢 Telegram")
    keyboard.row("💬 Связаться", "ℹ️ О боте")
    return keyboard


@bot.message_handler(commands=['start'])
def cmd_start(message):
    inline = types.InlineKeyboardMarkup(row_width=2)
    inline.add(
        types.InlineKeyboardButton("📺 Смотреть на YouTube", url=YOUTUBE_URL),
        types.InlineKeyboardButton("📢 Мой Telegram-канал", url=TELEGRAM_URL)
    )
    bot.send_message(
        message.chat.id,
        f"Привет, {message.from_user.first_name}! 👋\n\n"
        f"Добро пожаловать в бот канала Wendy42_453 🎮\n\n"
        f"👇 Выбирай в меню внизу:",
        reply_markup=main_menu()
    )
    bot.send_message(message.chat.id, "🔗 Мои ссылки:", reply_markup=inline)


@bot.message_handler(func=lambda m: m.text == "📺 YouTube")
def btn_youtube(message):
    inline = types.InlineKeyboardMarkup()
    inline.add(types.InlineKeyboardButton("▶️ Перейти на канал", url=YOUTUBE_URL))
    bot.send_message(message.chat.id, f"📺 Мой YouTube:\n{YOUTUBE_URL}", reply_markup=inline)


@bot.message_handler(func=lambda m: m.text == "📢 Telegram")
def btn_telegram(message):
    inline = types.InlineKeyboardMarkup()
    inline.add(types.InlineKeyboardButton("📢 Открыть канал", url=TELEGRAM_URL))
    bot.send_message(message.chat.id, f"📢 Мой Telegram-канал:\n{TELEGRAM_URL}", reply_markup=inline)


@bot.message_handler(func=lambda m: m.text == "💬 Связаться")
def btn_contact(message):
    bot.send_message(message.chat.id, "💬 Напиши мне сообщение — оно попадёт автору канала.")


@bot.message_handler(func=lambda m: m.text == "ℹ️ О боте")
def btn_about(message):
    bot.send_message(
        message.chat.id,
        "🤖 Я бот канала Wendy42_453.\nПомогаю находить видео и ссылки.\n\n"
        "/start — начать\n/help — помощь\n/links — ссылки"
    )


@bot.message_handler(commands=['help'])
def cmd_help(message):
    bot.send_message(message.chat.id, "/start — старт\n/help — справка\n/links — ссылки\n/echo <текст> — повтор")


@bot.message_handler(commands=['links'])
def cmd_links(message):
    inline = types.InlineKeyboardMarkup(row_width=1)
    inline.add(
        types.InlineKeyboardButton("📺 YouTube", url=YOUTUBE_URL),
        types.InlineKeyboardButton("📢 Telegram-канал", url=TELEGRAM_URL)
    )
    bot.send_message(message.chat.id, "🔗 Мои ссылки:", reply_markup=inline)


@bot.message_handler(commands=['echo'])
def cmd_echo(message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        bot.send_message(message.chat.id, "Напиши так: /echo Привет")
        return
    bot.send_message(message.chat.id, args[1])


@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.send_message(message.chat.id, f"Ты написал: {message.text}")


print("🤖 Бот запущен...")
bot.polling(none_stop=True)