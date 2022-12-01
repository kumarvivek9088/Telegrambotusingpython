from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.filters import Filters
from telegram import ParseMode,ReplyKeyboardMarkup,ReplyKeyboardRemove
import webbrowser
import pyscreenshot
import os
import subprocess
import ctypes
from shlex import quote
import linearwinvolume as lv
updater=Updater("paste your bot api here",use_context=True)

def start(update: Update, context:CallbackContext):
    update.message.reply_text("Hello how can i help you /help to see commands")

def unknown_command(update:Update, context: CallbackContext):
    update.message.reply_text("This command '%s' is not available" % update.message.text)
def help(update:Update,context: CallbackContext):
    update.message.reply_text("this is help")

def unknowm_text(update:Update ,context: CallbackContext):
    if update.message.from_user['username']=="enter your username here":
        msg=update.message.text
        if msg=="hello":
            update.message.reply_text("hii sir")
        elif msg=="youtube":
            webbrowser.open("www.youtube.com")
            update.message.reply_text("opening youtube")
        elif msg=="screenshot":
            path="screenshot.png"
            img=pyscreenshot.grab()
            img.save(path)
            update.message.reply_photo(open(path,'rb'),caption="here's your screenshot")
            os.remove(path)
        elif msg=="close keyboard":
            reply_markup=ReplyKeyboardRemove()
            update.message.reply_text(reply_markup=reply_markup,text="keyboard down")
        elif msg=="shutdown":
            subprocess.run('shutdown /s')
            text = "Shutted down."
            update.message.reply_text(text=text)
        elif msg=="lock":
            ctypes.windll.user32.LockWorkStation()
            text = "PC locked."
            update.message.reply_text(text=text)
        elif msg=="mute":
            lv.set_volume(0)
            update.message.reply_text("muted")
            
    else:
        update.message.reply_text("This is personal you can't use it")
def launch(update: Update, context: CallbackContext):
    ret = subprocess.run("start %s" % quote(context.args[0]), shell=True).returncode
    text = "Launching " + (context.args[0]) + "..."
    update.message.reply_text(text=text)
    if ret == 1:
        text = "Cannot launch " + (context.args[0])
        update.message.reply_text(text=text)
def volume(update:Update, context: CallbackContext):
    lv.set_volume(int(context.args[0]))

def keyboard(update:Update, context: CallbackContext):
    keyboard=[["screenshot","youtube","mute"],
              ["shutdown","lock"],
              ["close Keyboard"]]
    reply_markup=ReplyKeyboardMarkup(keyboard,resize_keyboard=True)
    update.message.reply_text(reply_markup=reply_markup,text="keyboard is up")

updater.dispatcher.add_handler(CommandHandler("start",start))
updater.dispatcher.add_handler(CommandHandler("help",help))
updater.dispatcher.add_handler(CommandHandler("keyboard",keyboard))
updater.dispatcher.add_handler(CommandHandler("launch",launch))
updater.dispatcher.add_handler(CommandHandler("volume",volume))
updater.dispatcher.add_handler(MessageHandler(Filters.command,unknown_command))
updater.dispatcher.add_handler(MessageHandler(Filters.text,unknowm_text))

updater.start_polling()
print("bot started")