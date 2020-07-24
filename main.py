import telebot

from bot import Tel_bot

token = '873712743:AAGcm-LpRtGTSefr81H9ZrYqRR7JrBUDzA8'
bot = telebot.TeleBot(token)
bot1 = Tel_bot(token)
_opredelenieB = False

@bot.message_handler(commands=['opr'])
def opr_message(message):
    bot1.log(message)
    global _opredelenieB
    if _opredelenieB == False:
        _opredelenieB = True
        bot.send_message(message.chat.id, 'Dicshinory on')
    else:
        _opredelenieB = False
        bot.send_message(message.chat.id, 'Dicshinory off')


@bot.message_handler(content_types=['text'])
def send_text(message): 
    bot1.log(message)
    if message.text[0] == '/':
        bot1.command(message)
    elif  message.text[:8] == 'Переведи' or message.text[:8] == 'переведи':
        if len(message.text) < 10:
            bot1.sendMes(message, 'Вы не ввели слово!')
        else:
            bot1.translate(message)
    elif message.text[:9] == 'Что такое':
        if len(message.text) < 11:
            bot1.sendMes(message, 'Вы не ввели слово!')
        else:
            bot1.opr(message)
    elif message.text[:9] == 'Переверни':
        if len(message.text) < 11:
            bot1.sendMes(message, 'Вы не ввели слово!')
        else:
            bot1.sendMes(message, bot1.revers(message.text[9::]))
    else:
        bot.send_message(message.chat.id, 'Я тебя не понимаю(')

"""  
@bot.message_handler(content_types=['sticker'])
def sticker_id(message):
    bot1.log(message)
    bot.send_message(message.chat.id, message)

@bot.message_handler(content_types=['audio'])
def handle_audio(message):
    bot1.log(message)
    bot.send_message(message.chat.id,'Норм музочка)')
"""

bot.polling()