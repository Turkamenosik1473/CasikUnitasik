import telebot
import random
from telebot import types

bot = telebot.TeleBot('TOKEN')

scores = {}
bests = {}
spins = {}

def get_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("🎰SPIN")
    btn2 = types.KeyboardButton("🎱SCORE / BEST")
    btn3 = types.KeyboardButton("☠RESET")
    btn4 = types.KeyboardButton("❗EXIT")
    markup.add(btn1, btn2, btn3, btn4)
    return markup

@bot.message_handler(commands=['start'])
def url(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(
        text="Casik`s site: ", url='https://github.com/Turkamenosik1473/CasikUnitasik'
    )
    markup.add(btn1)
    bot.send_message(
        message.from_user.id,
        "Casino for the brave & lucky ones",
        reply_markup=markup
    )
    bot.send_message(
        message.from_user.id,
        "Choose an action:",
        reply_markup=get_keyboard()
    )

@bot.message_handler(content_types=['text'])
def casino_engine(message):
    user_id = message.from_user.id

    if user_id not in scores:
        scores[user_id] = 0
    if user_id not in bests:
        bests[user_id] = 0
    if user_id not in spins:
        spins[user_id] = 0

    if message.text == "🎰SPIN":
        slot_case = random.randint(0, 778)
        spins[user_id] += 1
        if (slot_case % 7 == 0) or (slot_case % 9 == 0):
            scores[user_id] += 1
            if scores[user_id] > bests[user_id]:
                bests[user_id] = scores[user_id]
            bot.send_message(
                user_id,
                "😱🤑YOU ARE A WINNER!!!",
                parse_mode="Markdown",
                reply_markup=get_keyboard()
            )
        else:
            bot.send_message(
                user_id,
                "😪😥😮YOU LOST!!!",
                parse_mode="Markdown",
                reply_markup=get_keyboard()
            )
    elif message.text == "🎱SCORE / BEST":
        bot.send_message(
            user_id,
            f"SCORE: {scores[user_id]}",
            parse_mode="Markdown",
            reply_markup=get_keyboard()
        )
        bot.send_message(
            user_id,
            f"BEST: {bests[user_id]}",
            parse_mode="Markdown"
        )
        bot.send_message(
            user_id,
            f"Total spins: {spins[user_id]}",
            parse_mode="Markdown"
        )
    elif message.text == "☠RESET":
        scores[user_id] = 0
        bot.send_message(
            user_id,
            "Score successfully reset.",
            parse_mode="Markdown",
            reply_markup=get_keyboard()
        )
    elif message.text == "❗EXIT":
        scores[user_id] = 0
        bests[user_id] = 0
        spins[user_id] = 0
        bot.send_message(
            user_id,
            "All your progress has been deleted. Bye! 👋",
            parse_mode="Markdown",
            reply_markup=get_keyboard()
        )
    else:
        bot.send_message(
            user_id,
            "Unknown command.",
            reply_markup=get_keyboard()
        )

bot.polling(none_stop=True, interval=0)