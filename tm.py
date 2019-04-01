import telebot
import sqlite3
from telebot import types
from collections import defaultdict
token="889958255:AAFx0HHiWKr1qgcjA5jOYLsW_d84gxiKZ7U"
START,LANG1,LANG2,RESULT=range(4)
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
        update_state(message,LANG1)
        bot.send_message(message.chat.id,'Выберите первый язык')



@bot.message_handler(func=lambda message:get_state(message)== LANG1)
def handle_lang1(message):
    bot.send_message(message.chat.id,"Выберите второй язык")
    
    set_lang(message.chat.id,'lang1',message.text)
    update_state(message,LANG2)
@bot.message_handler(func=lambda message:get_state(message)== LANG2)
def handle_lang2(message):
    bot.send_message(message.chat.id,"Введите фразу")
    update_state(message,RESULT)
    set_lang(message.chat.id,'lang2',message.text)

    
    
@bot.message_handler(func=lambda message:get_state(message)== RESULT)
def translate(message):
    bot.send_message(message.chat.id,"Ваша фраза- "+message.text)
    langer=get_lang(message.chat.id)
    bot.send_message(message.chat.id,"Ваш язык {}".format(langer))
    
    
       
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
