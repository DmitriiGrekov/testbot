import telebot
from telebot import types
token="889958255:AAFx0HHiWKr1qgcjA5jOYLsW_d84gxiKZ7U"
persons={}
bot=telebot.TeleBot(token)

@bot.message_handler(commands=["start",'help'])
def hand_mes(message):
    bot.send_message(message.chat.id,'Hello')

bot.polling()
