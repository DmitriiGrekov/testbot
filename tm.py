import telebot
token="889958255:AAFx0HHiWKr1qgcjA5jOYLsW_d84gxiKZ7U"

START,TITLE,PRICE,CONFIRMATION=range(4)

bot=telebot.TeleBot(token)
@bot.message_handler(func=lambda message:get_state(message) == START)
def handler_messag(message):
    bot.send_message(message.chat.id,"НАПИШИ НАЗВАНИЕ")
    update_state(message,TITLE)
@bot.message_handler(func=lambda message:get_state(message) == TITLE)
def handler_title(message):
    bot.send_message(message.chat.id,"НАПИШИ ЦЕНУ")
    update_state(message,TITLE)
bot.polling()

from collections import defaultdict
USER_STATE=defaultdict(lambda:START)
def get_state(message):
    return USER_STATE(message.chat.id)
def updete_state(message,state):
    USER_STATE[message.chat.id]=state
