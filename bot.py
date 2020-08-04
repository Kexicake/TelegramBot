import logging

import requests
import telebot
import wikipedia

import json



class Tel_bot:
    def __init__(self, token):
        """Constructor"""
        self.bot = telebot.TeleBot(token)
        print('\n-----------------------------\n\nConstruction complit!')
        print('\n-----------------------------', end='')

    def sendMes(self, message, text):
        self.bot.send_message(message.chat.id, text)

    def command(self, message):
        keyboards = [telebot.types.ReplyKeyboardMarkup(True), telebot.types.ReplyKeyboardMarkup(True)]
        keyboards[0].row('/start', '/help')
        q = True
        self.log(message)

        if message.text == '/test':
            text = 'test pass'
            q = False
            self.bot.send_message(message.chat.id, text, reply_markup=keyboards[0])

        if q:
            try:
                text = message.text[1:] + '.txt'
                with open(text, 'r', encoding='utf-8') as fh: #открываем файл на чтение
                    self.bot.send_message(message.chat.id, fh.read())   
            except:
                self.sendMes(message, 'Я не знаю такую команду(')

    def opr(self, message):
        wikipedia.set_lang("ru")
        try:
            self.sendMes(message, wikipedia.summary(message.text[9::], sentences=2))
        except:
            self.sendMes(message, 'Хмм... почему-то не могу выполнить запрос, попробуйнаписать по другому.')

    def translate(self, message):

        with open('config.json', 'r', encoding='utf-8') as fh: #открываем файл на чтение
            config = json.load(fh) #загружаем из файла данные в словарь 

        lang = 'ru-en'
        langs = (('ru-en', 'ru-de', 'ru-tt', 'ru-uk'), ('английский', 'немецкий', 'татарский', 'украинский'))
        lang_num = 12
        lang_mes = ''

        # Проверка на указание языка
        if message.text[9:11] == "на":
            # Извлечение языка на который надо перевести
            while True:
                if lang_num == len(message.text) or message.text[lang_num] == ' ':
                    break
                lang_mes += message.text[lang_num]
                lang_num += 1
            # Переводим язык в машинный вид
            for i in range(len(langs[1]) + 1):
                if i == (len(langs[1])):
                    self.sendMes(message, "ERROR: Языка не существует или его нет в базе")
                    return
                if langs[1][i] == lang_mes:
                    lang = langs[0][i]
                    break
        else:
            lang_num = 9

        reque = requests.get('https://translate.yandex.net/api/v1.5/tr.json/translate?',
                             data={'key': config['Translater']['key'], 'text': message.text[lang_num::], 'lang': lang})
        translated = reque.json()
        self.sendMes(message, translated["text"])



  
    def log(self, message):
        logging.basicConfig(level=logging.INFO, filename='log.log', format='%(asctime)s -%(message)s',
                            datefmt='%d-%b-%y %H:%M:%S')
        logging.info(' @' + str(message.chat.username) + ' chatID: ' + str(message.chat.id) + ' username: ' + str(
            message.from_user.first_name) + ' ' + str(message.content_type) + ' - massage: ' + str(message.text))
        print('\n\nMessage {1} from {0}\n\n-----------------------------'.format(message.from_user.first_name,
                                                                                 message.text), end='')
