import telebot
import sqlite3
import requests
from telebot import types
from collections import defaultdict
from datetime import datetime
token="889958255:AAFx0HHiWKr1qgcjA5jOYLsW_d84gxiKZ7U"
START,TRANSLATE,TEST,SCHEDULE=range(4)
bot=telebot.TeleBot(token)    
conn = sqlite3.connect(":memory:")
cursor = conn.cursor()
cursor.execute("""CREATE TABLE subjects
                  (person text, subject text,date text,to_date text,questions text)
               """)

@bot.message_handler(commands=["start"])
def handle_message(message):
    markup =types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)  #Активация, название, количество кнопок по одной в ряду 
    itembtn1 = types.KeyboardButton('Переводчик') #Название кнопки 1 
    itembtn2 = types.KeyboardButton('Тест')
    itembtn3 = types.KeyboardButton('Рассписание')
    markup.add(itembtn1,itembtn2,itembtn3)
    
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
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True) #Активация, название, количество кнопок по одной в ряду 
        itembtn3 = types.KeyboardButton('@НАЗАД') #Название кнопки 1
        itembtn1 = types.KeyboardButton('Да')
        itembtn2 = types.KeyboardButton('Нет')
        markup.add(itembtn1,itembtn2,itembtn3)
        bot.send_message(message.chat.id,"Руслан гей?(да/нет)",reply_markup=markup)
    elif message.text.lower() == "рассписание":
        update_state(message,SCHEDULE)
        
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True) #Активация, название, количество кнопок по одной в ряду 
        itembtn1 = types.KeyboardButton('Задать домашку') #Название кнопки 1
        itembtn2 = types.KeyboardButton('Узнать домашку')
    
        markup.add(itembtn1,itembtn2)
        send=bot.send_message(message.chat.id,'Выберите функцию',reply_markup=markup)
        bot.register_next_step_handler(send,first)
def first(message):
    if message.text.lower() == "задать домашку":
        send=bot.send_message(message.chat.id,"Введите предмет")
        bot.register_next_step_handler(send,second)
    elif message.text.lower()=="узнать домашку":
        send=bot.send_message(message.chat.id,"Щас покажу")
        bot.register_next_step_handler(send,show_questions)
def second(message):
    set_lang(message.chat.id,"subject",message.text)
    set_lang(message.chat.id,"date",datetime.today())
    send=bot.send_message(message.chat.id,"Введите дату сдачи")
    bot.register_next_step_handler(send,third)
def third(message):
    set_lang(message.chat.id,"to_date",message.text)
    send=bot.send_message(message.chat.id,"Введите задание")
    bot.register_next_step_handler(send,fourth)
def fourth(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True) #Активация, название, количество кнопок по одной в ряду 
    itembtn3 = types.KeyboardButton('@НАЗАД')
    markup.add(itembtn3)
    conn = sqlite3.connect("mydatabase.db")
    cursor = conn.cursor()
    set_lang(message.chat.id,"questions",message.text)
    cursor.execute("INSERT INTO subjects VALUES (?,?,?,?,?)", [message.chat.id,get_lang(message.chat.id)["subject"],get_lang(message.chat.id)["date"],get_lang(message.chat.id)["to_date"],get_lang(message.chat.id)["questions"]])
    bot.send_message(message.chat.id,"Добавлено",reply_markup=markup)
    update_state(message,START)
    if message.text == "@НАЗАД":
        markup =types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)  #Активация, название, количество кнопок по одной в ряду 
        itembtn1 = types.KeyboardButton('Переводчик') #Название кнопки 1 
        itembtn2 = types.KeyboardButton('Тест')
        itembtn3 = types.KeyboardButton('Рассписание')
        markup.add(itembtn1,itembtn2,itembtn3)
    
        bot.send_message(message.chat.id,"Выберите функцию",reply_markup=markup)
def show_questions(message):
    conn = sqlite3.connect("mydatabase.db")
    cursor = conn.cursor()
    sql = "SELECT * FROM subjects WHERE person=?"
    
    for row in cursor.execute(sql,([message.chat.id])):
        bot.send_message(message.chat.id,row[1])
        
        
    
       
    
    
    
    
        
        
    
            
            
        
        
    


    
    
       
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
