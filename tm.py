import telebot
import sqlite3
from telebot import types
from collections import defaultdict
token="889958255:AAFx0HHiWKr1qgcjA5jOYLsW_d84gxiKZ7U"
START,TRANSLATED,LANG1,LANG2,RESULT=range(5)
bot=telebot.TeleBot(token)    

    

@bot.message_handler(commands=["start"])
def handle_message(message):
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True) #Активация, название, количество кнопок по одной в ряду 
    itembtn1 = types.KeyboardButton('Переводчик') #Название кнопки 1 
    
    markup.add(itembtn1)
    
    bot.send_message(message.chat.id,"Выберите функцию",reply_markup=markup)
    

@bot.message_handler(func=lambda message:get_state(message)== START)
def handle_lang(message):
    if message.text.lower() == "переводчик":
        update_state(message,TRANSLATED)
        bot.send_message(message.chat.id,'Установлен стате TRANSLATED')



@bot.message_handler(func=lambda message:get_state(message)== TRANSLATED)
def handle_lang1(message):
    bot.send_message(message.chat.id,"Выберите первый язык")
    

    
       
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
    
bot.polling()
