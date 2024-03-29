import json

from bot import Tel_bot

with open('config.json', 'r', encoding='utf-8') as fh: #открываем файл на чтение
            config = json.load(fh) #загружаем из файла данные в словарь 


bot = Tel_bot(config['Bot']['Token']) #подключаем бота 
    

@bot.bot.message_handler(content_types=['text']) #обработка текстовых сообщений
def send_text(message): 
    bot.log(message)
    if message.text[0] == '/':
        bot.command(message)

    elif  message.text[:8] == 'Переведи' or message.text[:8] == 'переведи':
        if len(message.text) < 10:
            bot.send(message.chat.id, 'Вы не ввели слово!')
        else:
            bot.translate(message)

    elif message.text[:9] == 'Что такое':
        if len(message.text) < 11:
           bot.send(message.chat.id, 'Вы не ввели слово!')
        else:
            bot.definition(message)

    elif message.text[:9] == 'Переверни':
        if len(message.text) < 11:
            bot.send(message.chat.id, 'Вы не ввели слово!')
        else:
            bot.send(message.chat.id, message.text[:9:-1])

    elif message.text == 'Погода':
        bot.weather(message)

    elif message.text[:3] == 'sms': 
        bot.sms(message.text[4::],message)

    else:
        bot.send(message.chat.id, 'Я тебя не понимаю(')

"""  
@bot.message_handler(content_types=['sticker']) #Обработка стикеров
def sticker_id(message):
    bot1.log(message)
    bot.send_message(message.chat.id, message)

@bot.message_handler(content_types=['audio']) #Обраюотка аудио 
def handle_audio(message):
    bot1.log(message)
    bot.send_message(message.chat.id,'Норм музочка)')
"""

bot.bot.polling()