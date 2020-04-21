import telebot
import requests 
import json
import wikipedia
import time

token = open('bot_token.txt')
bot = telebot.TeleBot(token.read())

keyboard_help = telebot.types.ReplyKeyboardMarkup(True)
keyboard_help.row('/start', '/help', '/revers', '/translate')
keyboard1 = telebot.types.ReplyKeyboardMarkup(True)
keyboard1.row('/help')

url = 'https://translate.yandex.net/api/v1.5/tr.json/translate?' 
key = 'trnsl.1.1.20200420T153840Z.c64aa64b1ef12707.339289160fc33c01cc0c66ce2604c7200714bf48' 
lang = 'en-ru','ru-en' 

_reversB = False
_translateB = False
_opredelenieB = False



@bot.message_handler(commands=['start'])
def start_message(message):
    f = open('start.txt', 'r')
    history = open('history.txt', 'a')
    history.write( '@' + str(message.chat.username) + ' ' + str(message.chat.id) + ' ' + time.ctime() + '\n')
    bot.send_message(message.chat.id,  f.read(), reply_markup=keyboard1)
    f.close()
    history.close()

@bot.message_handler(commands=['help'])
def help_message(message):
    f = open('help.txt', 'r')
    bot.send_message(message.chat.id,  f.read(), reply_markup=keyboard_help)
    f.close()

@bot.message_handler(commands=['version'])
def version_message(message):
    f = open('version.txt', 'r')
    bot.send_message(message.chat.id,  f.read(), reply_markup=keyboard_help)
    f.close()

@bot.message_handler(commands=['revers'])
def revers_message(message):
    global _reversB
    if _reversB == False:
        _reversB = True
        bot.send_message(message.chat.id, 'revers on')
    else:
        _reversB = False
        bot.send_message(message.chat.id, 'revers off')

@bot.message_handler(commands=['translate'])
def translate_message(message):
    global _translateB
    if _translateB == False:
        _translateB = True
        bot.send_message(message.chat.id, 'translate on')
    else:
        _translateB = False
        bot.send_message(message.chat.id, 'translate off')

@bot.message_handler(commands=['opr'])
def opr_message(message):
    global _opredelenieB
    if _opredelenieB == False:
        _opredelenieB = True
        bot.send_message(message.chat.id, 'Dicshinory on')
    else:
        _opredelenieB = False
        bot.send_message(message.chat.id, 'Dicshinoryoff')

@bot.message_handler(content_types=['text'])
def send_text(message): 
    global _reversB, _translateB
    if _reversB == True:
        message_revers = ''
        i = len(message.text)
        while i > 0:
            i -= 1 
            message_revers += message.text[i] 
        bot.send_message(message.chat.id, message_revers)
    elif  _translateB == True:
        global url, key, lang
        translated = requests.post(url, data={'key': key, 'text': message.text, 'lang': lang})
        not_farm_text = translated.text
        sb = False
        word = ''
        i = 0
        while i<len(not_farm_text):
            if not_farm_text[i-2] == '[':
                sb = True
            if not_farm_text[i] == '"':
                sb = False
            if sb == True:
                word += not_farm_text[i]
            i += 1
        text = 'Слово/a ' + message.text + ' на английском - ' + word
        bot.send_message(message.chat.id, text)
    elif _opredelenieB == True:
        wikipedia.set_lang("ru")
        bot.send_message(message.chat.id, wikipedia.summary(message.text, sentences=2))
    elif message.text == 'Пока':
        bot.send_message(message.chat.id, 'Пака')
    elif message.text == 'Привет':
        bot.send_message(message.chat.id, 'Привет, мой создатель')    
    else:
        bot.send_message(message.chat.id, 'Я тебя не понимаю(')
    
@bot.message_handler(content_types=['sticker'])
def sticker_id(message):
    bot.send_message(message.chat.id, message)

@bot.message_handler(content_types=['audio'])
def handle_audio(message):
	bot.send_message(message.chat.id, 'Норм музочка)')

bot.polling()