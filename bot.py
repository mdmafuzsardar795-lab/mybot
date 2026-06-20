import telebot
from telebot import types
import random

TOKEN = '8922524173:AAF5NhkJ5d1zJNdRao05sL8JzE4-9eunDnM'
bot = telebot.TeleBot(TOKEN)

user_balances = {}
user_captchas = {}

def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(types.KeyboardButton("🆔 Account"), types.KeyboardButton("✍️Typing Ear\U0001f92a"))
    markup.row(types.KeyboardButton("\U0001f4b8REFERRAL\U0001f4b8"), types.KeyboardButton("\U0001f48ePayment\U0001f4b8"))
    markup.row(types.KeyboardButton("\U0001f4deSUPPORT\u0001f4de"), types.KeyboardButton("\U0001f4cbMy Task\U0001f4b0"))
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    if user_id not in user_balances:
        user_balances[user_id] = 0
    bot.send_message(message.chat.id, "⚡ Bangladesh 1Captcha বটের মূল মেনুতে আপনাকে স্বাগতম!", reply_markup=main_menu())

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.from_user.id
    if user_id not in user_balances:
        user_balances[user_id] = 0

    if message.text == "🆔 Account":
        bot.send_message(message.chat.id, f"👤 **আপনার অ্যাকাউন্ট ইনফো**\n\n💰 ব্যালেন্স: BDT {user_balances[user_id]}")
    
    elif message.text == "✍️Typing Ear\U0001f92a":
        captcha_text = str(random.randint(10000, 99999))
        user_captchas[user_id] = captcha_text
        
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("Cancel ❌"))
        
        bot.send_message(message.chat.id, f"✍️ **Type this captcha code:**\n\n👉 `{captcha_text}`", parse_mode="Markdown", reply_markup=markup)
        
    elif message.text == "Cancel ❌":
        if user_id in user_captchas:
            del user_captchas[user_id]
        bot.send_message(message.chat.id, "Captcha Cancelled ❌", reply_markup=main_menu())
        
    elif message.text == "\U0001f48ePayment\U0001f4b8":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("bKash"), types.KeyboardButton("Nagad"))
        bot.send_message(message.chat.id, "Select Payment Method ♻️", reply_markup=markup)
        
    elif message.text in ["bKash", "Nagad"]:
        bot.send_message(message.chat.id, "⚠️ আপনার ব্যালেন্স নুন্যতম BDT 500 হতে হবে।", reply_markup=main_menu())
        
    elif message.text in ["\U0001f4b8REFERRAL\U0001f4b8", "\U0001f4deSUPPORT\u0001f4de", "\U0001f4cbMy Task\U0001f4b0"]:
        bot.send_message(message.chat.id, "এই ফিচারটি শীঘ্রই চালু হবে।", reply_markup=main_menu())
        
    else:
        if user_id in user_captchas and message.text == user_captchas[user_id]:
            user_balances[user_id] += 2
            del user_captchas[user_id]
            bot.send_message(message.chat.id, "✅ Correct! BDT 2 added to your account.")
            bot.send_message(message.chat.id, "🔙 আপনি মূল মেনুতে ফিরে এসেছেন। পুনরায় কাজ করতে '✍️Typing Ear\U0001f92a' বাটনে চাপ দিন।", reply_markup=main_menu())
        elif user_id in user_captchas:
            bot.send_message(message.chat.id, "❌ ভুল উত্তর! আবার চেষ্টা করুন বা 'Cancel ❌' করুন।")

bot.polling()
