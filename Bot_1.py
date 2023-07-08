import telebot
from telebot import types
import webbrowser
import sqlite3
import requests
import json

bot = telebot.TeleBot('6134115976:AAHpQeeXxx-D7u7gniTb9ojK7hbFYlK5MgM')
API = 'c3c6c5c894f602c593b8591f6e2ae976'

def Nonone(Text):
    if Text==None:
        return ""
    else:
        return Text
    
#Comandos que inician con "/""
#Abrir sitio web
@bot.message_handler(commands = ['site', 'website'])
def site(message):
    webbrowser.open('http://vk.com')

name = None

#Clima https://home.openweathermap.org/api_keys
@bot.message_handler(commands = ['start2'])
def start2(message):
    bot.send_message(message.chat.id, 'Привет, рад тебе видет! Напиши название города')

@bot.message_handler(content_types = ['text'])
def get_weather(message):
    city = message.text.strip().lower()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
    if res.status_code == 200:
       data = json.loads(res.text)
       temp = data["main"]["temp"]
       bot.reply_to(message, f'Сейчас погода: {temp}')
       image = 'Soleado.png' if temp > 5.0 else 'Nublado con sol.png'
       file = open('./' + image, 'rb')
       bot.send_photo(message.chat.id, file)
    else:
        bot.reply_to(message, 'Город указан не верно') 


#Подключение к базе данных
@bot.message_handler(commands = ['start1'])
def start1(message):
    conn = sqlite3.connect('Tel_Bot_1')
    cur = conn.cursor()

    cur.execute('CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, name varchar(50), pass varchar(50))')
    conn.commit()
    cur.close()
    conn.close()

    bot.send_message(message.chat.id, 'Привет, сейчас тебя зарегистрируем! Ввидете ваше имя')
    bot.register_next_step_handler(message, user_name)


def user_name(message):
    global name 
    name = message.text.strip()
    bot.send_message(message.chat.id, 'Ввидете пароль')
    bot.register_next_step_handler(message, user_pass)

def user_pass(message):
    password = message.text.strip()
    conn = sqlite3.connect('Tel_Bot_1')
    cur = conn.cursor()
    cur.execute("INSERT INTO users (name, pass) VALUES ('%s', '%s')" % (name, password))
    conn.commit()
    cur.close()
    conn.close()

    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton('Список пользователей', callback_data='users'))
    bot.send_message(message.chat.id, 'Пользователь зарегистрирован!', reply_markup=markup)
    #bot.registrer_next_step.handler(message, user_pass)

@bot.callback_query_handler(func = lambda call : True)
def callback(call):
    conn = sqlite3.connect('Tel_Bot_1')
    cur = conn.cursor()
    cur.execute('SELECT * FROM users')
    users = cur.fetchall()

    info = ""
    for el in users:
        info += f'Имя: {el[1]}, Пароль: {el[2]}\n'

    cur.close()
    conn.close()
    bot.send_message(call.message.chat.id, info)


"""
#Crear botones debajo chat
@bot.message_handler(commands = ['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('Перейти на саит')
    markup.row(btn1)
    btn2 = types.KeyboardButton('Удалить фото')
    btn3 = types.KeyboardButton('Изменить текст')
    markup.row(btn2, btn3)
    #Mandar foto
    file = open('./SKW.png', 'rb')
    bot.send_photo(message.chat.id, file, reply_markup=markup)
    #bot.send_audio()
    #bot.send_video()
    #bot.send_message(message.chat.id, 'Привет', reply_markup=markup)
    #Registrar 
    bot.register_next_step_handler(message, on_click)"""

def on_click(message):
    if message.text == 'Перейти на саит':
        bot.send_message(message.chat.id, 'Webside is open')
    elif message.text == 'Удалить фото':
        bot.send_message(message.chat.id, 'Delete')


#Imagen, audio, video esperado
#Crear botones en el chat
@bot.message_handler(content_types = ['photo'])
def get_photo(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Перейти на саит', url='http://vk.com')
    markup.row(btn1)
    btn2 = types.InlineKeyboardButton('Удалить фото', callback_data='delete')
    btn3 = types.InlineKeyboardButton('Изменить текст', callback_data='edit')
    markup.row(btn2, btn3)
    bot.reply_to(message, "Интересно", reply_markup=markup)

#callback_data convoca este decorador
#callback: True confirmar no esta vacio
"""@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data =='delete':
        bot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
    if callback.data =='edit':
        bot.edit_message_text('Edit text',callback.message.chat.id, callback.message.message_id)    """

""" @bot.message_handler(commands = ['start'])
def start(message):
    bot.send_message(message.chat.id, f"Привет, {Nonone(message.from_user.first_name)} {Nonone(message.from_user.last_name)}") """

@bot.message_handler(commands = ['help'])
def help(message):
    bot.send_message(message.chat.id, "<b>Help</b> <em><u>information</u></em>...", parse_mode='html')

#Informacion propia del usuario que escribe
@bot.message_handler(commands = ['main'])
def main(message):
    bot.send_message(message.chat.id, message)


#Para cualquier mensage tipo texto
@bot.message_handler()
def info(message):
    if message.text.lower() == ("привет" or "Здравствуйте"):
        bot.send_message(message.chat.id, f"Привет, {Nonone(message.from_user.first_name)} {Nonone(message.from_user.last_name)}")
    elif message.text.lower() == "id":
        bot.reply_to(message, f'ID: {message.from_user.id}')
    elif message.text.lower() == ('site' or 'website'):
        webbrowser.open('http://vk.com')
    elif message.text.lower() == 'help':
        bot.send_message(message.chat.id, "<b>Help</b> <em><u>information</u></em>...", parse_mode='html')


bot.polling(non_stop=True)
#bot.infinity_polling()   Otra opción para hacer infinito el bot 