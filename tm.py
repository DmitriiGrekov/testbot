import telebot
import sqlite3
import requests
from telebot import types
from collections import defaultdict
token="889958255:AAFx0HHiWKr1qgcjA5jOYLsW_d84gxiKZ7U"
START,TRANSLATE,TEST=range(3)
bot=telebot.TeleBot(token)    

    

@bot.message_handler(commands=["start"])
def handle_message(message):
    markup =types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)  #Активация, название, количество кнопок по одной в ряду 
    itembtn1 = types.KeyboardButton('Переводчик') #Название кнопки 1 
    itembtn2 = types.KeyboardButton('Тест')
    markup.add(itembtn1,itembtn2)
    
    bot.send_message(message.chat.id,"Выберите функцию",reply_markup=markup)
    

@bot.message_handler(func=lambda message:get_state(message)== START)
def handle_lang(message):
    if message.text.lower() == "переводчик":
        update_state(message,TRANSLATE)
        
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True) #Активация, название, количество кнопок по одной в ряду 
        itembtn1 = types.KeyboardButton('ru') #Название кнопки 1
        itembtn2 = types.KeyboardButton('en')
    
        markup.add(itembtn1,itembtn2)
        send=bot.send_message(message.chat.id,'Выберите первый язык',reply_markup=markup)
        bot.register_next_step_handler(send,set_firstlang)
    elif message.text.lower() == "тест":
        update_state(message,TEST)
        bot.send_message(message.chat.id,"Руслан гей?(да/нет)")
        
    
def set_firstlang(message):
    bot.send_message(message.chat.id,"Устанавливаю первый язык")
    set_lang(message.chat.id,"lang1",message.text)
     
        
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True) #Активация, название, количество кнопок по одной в ряду 
    itembtn1 = types.KeyboardButton('ru') #Название кнопки 1
    itembtn2 = types.KeyboardButton('en')
    backbut=types.KeyboardButton("@НАЗАД")
    
    markup.add(itembtn1,itembtn2,backbut)
    send=bot.send_message(message.chat.id,'Выберите второй язык',reply_markup=markup)
    bot.register_next_step_handler(send,set_secondlang)
def set_secondlang(message):
    bot.send_message(message.chat.id,"Устанавливаю второй язык")
    set_lang(message.chat.id,"lang2",message.text)
     
        
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True) #Активация, название, количество кнопок по одной в ряду 
    
    backbut=types.KeyboardButton("@НАЗАД")
    
    markup.add(backbut)
    send=bot.send_message(message.chat.id,'Введите фразу',reply_markup=markup)
    
    
    
    


@bot.message_handler(func=lambda message:get_state(message)==TRANSLATE )
def handle_lang1(message):
    if message.text == "@НАЗАД":
        update_state(message,START)
        markup =types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)  #Активация, название, количество кнопок по одной в ряду 
        itembtn1 = types.KeyboardButton('Переводчик') #Название кнопки 1 
        itembtn2 = types.KeyboardButton('Тест')
        markup.add(itembtn1,itembtn2)
    
        bot.send_message(message.chat.id,"Выберите функцию",reply_markup=markup)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True) #Активация, название, количество кнопок по одной в ряду 
        itembtn1 = types.KeyboardButton('@НАЗАД') #Название кнопки 1
    
    
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
