import telebot
import sqlite3
import requests
from telebot import types
from collections import defaultdict
token="889958255:AAFx0HHiWKr1qgcjA5jOYLsW_d84gxiKZ7U"
START,LANG1,LANG2,RESULT,TEST=range(5)
bot=telebot.TeleBot(token)    

    

@bot.message_handler(commands=["start"])
def handle_message(message):
    markup = types.InlineKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True) #Активация, название, количество кнопок по одной в ряду 
    itembtn1 = types.InlineKeyboardButton('Переводчик',callback_data="translate") #Название кнопки 1 
    itembtn2 = types.InlineKeyboardButton('Тест'callback_data="test")
    markup.add(itembtn1,itembtn2)
    
    bot.send_message(message.chat.id,"Выберите функцию",reply_markup=markup)
    

@bot.message_handler(func=lambda message:get_state(message)== START)
def handle_lang(message):
    if message.text.lower() == "переводчик":
        update_state(message,LANG1)
        
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True) #Активация, название, количество кнопок по одной в ряду 
        itembtn1 = types.KeyboardButton('ru') #Название кнопки 1
        itembtn2 = types.KeyboardButton('en')
    
        markup.add(itembtn1,itembtn2)
        bot.send_message(message.chat.id,'Выберите первый язык',reply_markup=markup)
    elif message.text.lower() == "тест":
        update_state(message,TEST)
        bot.send_message(message.chat.id,"Руслан гей?(да/нет)")
        
    



@bot.message_handler(func=lambda message:get_state(message)== LANG1)
def handle_lang1(message):
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True) #Активация, название, количество кнопок по одной в ряду 
    itembtn1 = types.KeyboardButton('ru') #Название кнопки 1
    itembtn2 = types.KeyboardButton('en')
    
    markup.add(itembtn1,itembtn2)
    bot.send_message(message.chat.id,'Выберите второй язык',reply_markup=markup)
    set_lang(message.chat.id,'lang1',message.text)
    update_state(message,LANG2)
@bot.message_handler(func=lambda message:get_state(message)== LANG2)
def handle_lang2(message):
    bot.send_message(message.chat.id,"Введите фразу")
    update_state(message,RESULT)
    set_lang(message.chat.id,'lang2',message.text)
    if message.text == "/start":
        update_state(message,START)

    
    
@bot.message_handler(func=lambda message:get_state(message)== RESULT)
def translate(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True) #Активация, название, количество кнопок по одной в ряду 
    itembtn1 = types.KeyboardButton('/start') #Название кнопки 1
    
    
    markup.add(itembtn1)
    
    if message.text == "/start":
        update_state(message,START)
        bot.send_message(message.chat.id,"Возвращаюсь в меню",reply_markup=markup)
        
        
    else:
        
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True) #Активация, название, количество кнопок по одной в ряду 
        itembtn1 = types.KeyboardButton('/start') #Название кнопки 1
    
    
        markup.add(itembtn1)
    
    
        
        langer=get_lang(message.chat.id)
        lang1=langer["lang1"]
        lang2=langer["lang2"]
    
        url='https://translate.yandex.net/api/v1.5/tr.json/translate?'
        key='trnsl.1.1.20190201T172728Z.34034e93ef318814.4cd85f71122011aa48770690493d232d5ff78c60'    
        TEXT=message.text
        LANg=lang1+"-"+lang2
        r=requests.post(url,data={'key':key,'text':TEXT,'lang':LANg})
        bot.send_message(message.chat.id,*eval(r.text)['text'])
        bot.send_message(message.chat.id,"Введите фразу",reply_markup=markup)
    
 
@bot.message_handler(func=lambda message:get_state(message)== TEST)
def handle_test(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True) #Активация, название, количество кнопок по одной в ряду 
    itembtn1 = types.KeyboardButton('/start') #Название кнопки 1
    
    
    markup.add(itembtn1)
    if message.text == "/start":
        update_state(message,START)
        bot.send_message(message.chat.id,"Возвращаюсь в меню",reply_markup=markup)
    elif message.text.lower()=="да":
        bot.send_message(message.chat.id,"Красава,уважаю")
    elif message.text.lower() == "нет":
        bot.send_message(message.chat.id,"Руслан ты?")
    else:
        bot.send_message(message.chat.id,"Ты не умеешь играть в эту игру")
    update_state(message,START)
    
    
       
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
