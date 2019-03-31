import telebot
from telebot import types
token="889958255:AAFx0HHiWKr1qgcjA5jOYLsW_d84gxiKZ7U"

bot=telebot.TeleBot(token)

def create_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_phone = types.KeyboardButton(text="Переводчик")
    
    keyboard.add(button_phone)
    return keyboard
@bot.message_handler(commands=["start",'help'])
def hand_mes(message):
    
    keyboard=create_keyboard()
    send=bot.send_message(message.chat.id, "Выбериет функцию", reply_markup=keyboard)
    bot.register_next_step_handler(send,second)
    conn = sqlite3.connect("mydatabase.db") # или :memory: чтобы сохранить в RAM
    cursor = conn.cursor()
    
# Создание таблицы
    cursor.execute("""CREATE TABLE langer
                  (id text, lang text)
               """)
    cursor.execute("INSERT INTO langer VALUES (?,?)", [message.chat.id,"-"])
    
def second(message):
    
    

    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    butt_1 = types.KeyboardButton(text="rus-eng")
    butt_2 = types.KeyboardButton(text="eng-rus")
    button_back = types.KeyboardButton(text="/Назад")
    keyboard.add(butt_1,butt_2,button_back)
    send=bot.send_message(message.chat.id,"Введите язык",reply_markup=keyboard)
    bot.register_next_step_handler(send,third)
def third(message):
    if message.text == "/Назад":
        
        conn = sqlite3.connect('mydatabase.db')
        c = conn.cursor()

        query = "DELETE FROM langer WHERE id = '%s'" %(message.chat.id)
        

        mydata = c.execute(query)
        conn.commit()
        keyboard=create_keyboard()
        bot.send_message(message.chat.id,"Выберите функцию",reply_markup=keyboard)
        return 1
    
    conn = sqlite3.connect("mydatabase.db") # или :memory: чтобы сохранить в RAM
    cursor = conn.cursor()
    query="UPDATE albums SET lang = '%s' WHERE id = '%s'"%(message.text,message.chat.id)
    cursor.execute()
    sql = "SELECT * FROM langer WHERE id=?"
    cursor.execute(sql, [(message.chat.id)])
    bot.send_message(message.chat.id,cursor.fetchall())
    conn.commit() 
    


    

    
        

bot.polling()
