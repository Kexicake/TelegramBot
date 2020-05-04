import telebot
import requests 
import json
import wikipedia
import time

token = '873712743:AAGcm-LpRtGTSefr81H9ZrYqRR7JrBUDzA8'
bot = telebot.TeleBot(token)

keyboard_help = telebot.types.ReplyKeyboardMarkup(True)
keyboard_help.row('/start', '/help', '/revers', '/translate')
keyboard1 = telebot.types.ReplyKeyboardMarkup(True)
keyboard1.row('/help')

url = 'https://translate.yandex.net/api/v1.5/tr.json/translate?' 
key = 'trnsl.1.1.20200420T153840Z.c64aa64b1ef12707.339289160fc33c01cc0c66ce2604c7200714bf48' 
words = '' 
langs = ['ru-en','ru-de' ,'ru-tt' ,'ru-uk']
langs_name = ['на английский', 'на немецкий', 'на татарский', 'на украинский']

_reversB = False
_opredelenieB = False

def log(message):
    history = open('history.txt', 'a')
    history.write( '@' + str(message.chat.username) + ' ' + str(message.chat.id) + ' ' + str(message.from_user.first_name) + ' ' + str(message.content_type) + ' - ' + str(message.text) + ' ' + time.ctime() + '\n')
    history.close()

def revers(text):
    message_revers = ''
    i = len(text)
    while i > 0:
        i -= 1 
        message_revers += text[i]
    return message_revers

@bot.message_handler(commands=['start'])
def start_message(message):
    log(message)
    f = open('start.txt', 'r')
    bot.send_message(message.chat.id,  f.read(), reply_markup=keyboard1)
    f.close()


@bot.message_handler(commands=['help'])
def help_message(message):
    log(message)
    f = open('help.txt', 'r')
    bot.send_message(message.chat.id,  f.read(), reply_markup=keyboard_help)
    f.close()

@bot.message_handler(commands=['version'])
def version_message(message):
    log(message)
    f = open('version.txt', 'r')
    bot.send_message(message.chat.id,  f.read(), reply_markup=keyboard_help)
    f.close()

@bot.message_handler(commands=['revers'])
def revers_message(message):
    log(message)
    global _reversB
    if _reversB == False:
        _reversB = True
        bot.send_message(message.chat.id, 'revers on')
    else:
        _reversB = False
        bot.send_message(message.chat.id, 'revers off')

@bot.message_handler(commands=['opr'])
def opr_message(message):
    log(message)
    global _opredelenieB
    if _opredelenieB == False:
        _opredelenieB = True
        bot.send_message(message.chat.id, 'Dicshinory on')
    else:
        _opredelenieB = False
        bot.send_message(message.chat.id, 'Dicshinory off')

@bot.message_handler(content_types=['text'])
def send_text(message): 
    global _reversB, words
    words = message
    log(message)
    if _reversB == True:
        bot.send_message(message.chat.id, revers(message.text))
    elif  message.text[:8] == 'Переведи':
        global url, key, langs, langs_name
        message_revers = revers(message.text)
        endword = 0
        count = 0
        indicator = False

        while indicator == False:
            if message_revers[endword] == ' ':
                count += 1
            if count == 2:
                indicator = True
            endword += 1
        endword -= 1
        text_lang = revers(message_revers[:endword])


        ir = 0
        lang = ''
        ind = False
        while ir <= len(langs_name):
            if ir == len(langs_name):
                bot.send_message(message.chat.id, 'Такого языка ещё нет в базе или он не существует!')
                ind = True
                break
            if langs_name[ir] == text_lang:
                lang = langs[ir]
                break
            ir += 1 
        if ind == False:
            text = message.text[9:(len(message.text) - endword)] 
            #lang = "ru-en"
            reque = requests.get(url, data={'key': key, 'text': text, 'lang': lang})
            #text = text + ' - ' + word
            translated = reque.json()
            bot.send_message(message.chat.id, translated["text"])

            #msg = bot.send_message(message.chat.id, 'На какой язык перевести?')
            #bot.register_next_step_handler(msg, translate) 
    elif _opredelenieB == True:
        wikipedia.set_lang("ru")
        bot.send_message(message.chat.id, wikipedia.summary(message.text, sentences = 2))   
    else:
        bot.send_message(message.chat.id, 'Я тебя не понимаю(')

    
@bot.message_handler(content_types=['sticker'])
def sticker_id(message):
    log(message)
    bot.send_message(message.chat.id, message)

@bot.message_handler(content_types=['audio'])
def handle_audio(message):
    log(message)
    bot.send_message(message.chat.id,'Норм музочка)')


bot.polling()