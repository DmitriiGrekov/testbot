import telebot
import sqlite3
from telebot import types
from collections import defaultdict
token="889958255:AAFx0HHiWKr1qgcjA5jOYLsW_d84gxiKZ7U"
START,TRANSLATED,LANG1,LANG2,RESULT=range(5)
bot=telebot.TeleBot(token)    
USER_STATE=defaultdict(lambda:START)
PERSONS=defaultdict(lambda:{})
def get_state(message):
    return USER_STATE[message.chat.id]
def update_state(message,state):
    USER_STATE[message.chat.id]=state
def set_lang(user_id,key,value):
    PERSONS[user_id][key]=value
def get_lang(user_id):
    return PERSONS[user_id]
    
    

@bot.message_handler(commands=["start"])
def handle_message(message):
    keyboar=types.ReplyKeyboardMarkup(True,True)
    button1=types.ReplyKeyboardButton("Переводчик")
    keyboar.add(button1)
    bot.send_message(message.chat.id,"Выберите функцию",reply_markup=keyboar)
    

@bot.message_handler(content_types=["text"])
def handle_lang(message):
    if message.text.lower == "переводчик":
        update_state(message,TRANSLATED)



@bot.message_handler(func=lambda message:get_state(message)==TRANSLATED)
def handle_lang1(message):
    bot.send_message(message.chat.id,"Выберите первый язык")
    

    
        

bot.polling()
