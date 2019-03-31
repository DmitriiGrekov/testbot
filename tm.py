import telebot
from telebot import types
token="889958255:AAFx0HHiWKr1qgcjA5jOYLsW_d84gxiKZ7U"
persons={}
bot=telebot.TeleBot(token)

@bot.message_handler(commands=["start",'help'])
def hand_mes(message):
     Эти параметры для клавиатуры необязательны, просто для удобства
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_phone = types.KeyboardButton(text="Переводчик")
    
    keyboard.add(button_phone)
    send=bot.send_message(message.chat.id, "Выбериет функцию", reply_markup=keyboard)
    bot.register_next_step_handler(send,second)
def second(message):
    bot.send_message(message.chat.id,"Вы отправили -> " +message.text)

bot.polling()
