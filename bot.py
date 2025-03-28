import telebot
import webbrowser
import pyscreenshot
import os
import subprocess
import ctypes
import pyvolume

TOKEN = "7895037300:AAFqc08uqQldfKzaDdXPwmmqtO97wqEpWSs"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Hello, how can I help you? Use /help to see commands.")

@bot.message_handler(commands=['help'])
def help_command(message):
    bot.reply_to(message, "This is help.")

@bot.message_handler(commands=['launch'])
def launch(message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        bot.reply_to(message, "Please provide an application to launch.")
        return
    ret = subprocess.run(f"start {args[1]}", shell=True).returncode
    text = f"Launching {args[1]}..."
    bot.reply_to(message, text)
    if ret == 1:
        bot.reply_to(message, f"Cannot launch {args[1]}")

@bot.message_handler(commands=['volume'])
def volume(message):
    args = message.text.split()
    if len(args) < 2:
        bot.reply_to(message, "Please provide a volume level (0-100).")
        return
    try:
        volume_level = int(args[1])
        pyvolume.custom(percent=volume_level)
        bot.reply_to(message, f"Volume set to {volume_level}%")
    except ValueError:
        bot.reply_to(message, "Invalid volume level.")

@bot.message_handler(commands=['keyboard'])
def keyboard(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("screenshot", "youtube", "mute")
    markup.row("shutdown", "lock")
    markup.row("close keyboard")
    bot.send_message(message.chat.id, "Keyboard is up.", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    if message.from_user.username == "ViveshDheer":
        msg = message.text.lower()
        if msg == "hello":
            bot.reply_to(message, "Hi Sir")
        elif msg == "youtube":
            webbrowser.open("https://www.youtube.com")
            bot.reply_to(message, "Opening YouTube")
        elif msg == "screenshot":
            path = "screenshot.png"
            img = pyscreenshot.grab()
            img.save(path)
            with open(path, 'rb') as photo:
                bot.send_photo(message.chat.id, photo, caption="Here's your screenshot")
            os.remove(path)
        elif msg == "close keyboard":
            bot.send_message(message.chat.id, "Keyboard down", reply_markup=telebot.types.ReplyKeyboardRemove())
        elif msg == "shutdown":
            subprocess.run('shutdown /s')
            bot.reply_to(message, "Shutting down...")
        elif msg == "lock":
            ctypes.windll.user32.LockWorkStation()
            bot.reply_to(message, "PC locked.")
        elif msg == "mute":
            pyvolume.custom(percent=0)
            bot.reply_to(message, "Muted")
    else:
        bot.reply_to(message, "This is personal, you can't use it.")

print("Bot started")
bot.polling(none_stop=True)