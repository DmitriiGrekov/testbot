import telebot
from telebot import types
token="889958255:AAFx0HHiWKr1qgcjA5jOYLsW_d84gxiKZ7U"
persons={}
bot=telebot.TeleBot(token)

def create_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_phone = types.KeyboardButton(text="Переводчик",request_location=True)
    button_phone = types.KeyboardButton(text="/Назад")
    keyboard.add(button_phone)
    return keyboard
@bot.message_handler(commands=["start",'help'])
def hand_mes(message):
     
    keyboard=create_keyboard()
    send=bot.send_message(message.chat.id, "Выбериет функцию", reply_markup=keyboard)
    bot.register_next_step_handler(send,second)
def second(message):
    if message.text == 'Переводчик':
        lon=message.location.longitude
        lan=message.location.latitude
        bot.send_message(message.chat.id,"Широта "+lon+"Долгота "+lan)
    
        

bot.polling()
