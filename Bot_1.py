import telebot
from telebot import types
import webbrowser

bot = telebot.TeleBot('6134115976:AAHpQeeXxx-D7u7gniTb9ojK7hbFYlK5MgM')

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

#Imagen, audio, video esperado
@bot.message_handler(content_types = ['photo'])
def get_photo(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Перейти на саит', url='http://vk.com')
    markup.row(btn1)
    btn2 = types.InlineKeyboardButton('Удалить фото', callback_data='delete')
    btn3 = types.InlineKeyboardButton('Изменить текст', callback_data='edit')
    markup.row(btn2, btn3)
    bot.reply_to(message, "Интересно", reply_markup=markup)

@bot.message_handler(commands = ['start'])
def start(message):
    bot.send_message(message.chat.id, f"Привет, {Nonone(message.from_user.first_name)} {Nonone(message.from_user.last_name)}")

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
    if message.text.lower() == "привет" or "Здравствуйте":
        bot.send_message(message.chat.id, f"Привет, {Nonone(message.from_user.first_name)} {Nonone(message.from_user.last_name)}")
    elif message.text.lower() == "id":
        bot.reply_to(message, f'ID: {message.from_user.id}')
    elif message.text.lower() == 'site' or 'website':
        webbrowser.open('http://vk.com')
    elif message.text.lower() == 'help':
        bot.send_message(message.chat.id, "<b>Help</b> <em><u>information</u></em>...", parse_mode='html')


bot.polling(non_stop=True)
#bot.infinity_polling()   Otra opción para hacer infinito el bot 