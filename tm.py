import telebot
import sqlite3
from telebot import types
from collections import defaultdict
token="889958255:AAFx0HHiWKr1qgcjA5jOYLsW_d84gxiKZ7U"
START,TRANSLATED,LANG1,LANG2=range(4)
bot=telebot.TeleBot(token)    
USER_STATE=defaultdict(lambda:START)

def get_state(message):
    return USER_STATE[message.chat.id]
def update_state(message,state):
    USER_STATE[message.chat.id]=state

@bot.message_handler(func=lambda message: get_state(message) == START)
def handle_message(message):
    bot.send_message(message.chat.id,"Выберите функцию")
    if message.text.lower() == "переводчик":
        update_state(message,TRANSLATED)

@bot.message_handler(func=lambda message: get_state(message) == TRANSLATED)
def handle_lang(message):
    bot.send_message(message.chat.id,"Выберите первый язык")

    
        

bot.polling()
