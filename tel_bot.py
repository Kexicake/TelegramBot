import telebot, requests, json, wikipedia, time, adodbapi
class Tel_bot:
    def __init__(self,token):
        """Constructor"""
        self.bot = telebot.TeleBot(token)
        print('Construction complit!\n-----------------------------\n')

    def sendMes(self, message, text):
        self.bot.send_message(message.chat.id, text)

    def command(self, message):
        keyboard_help = telebot.types.ReplyKeyboardMarkup(True)
        keyboard_help.row('/start', '/help', '/revers', '/translate')
        keyboard1 = telebot.types.ReplyKeyboardMarkup(True)
        keyboard1.row('/help')
        
        self.log(message)
        if message.text == '/test':
            text = 'test pass'
        elif message.text == '/start':
            f = open('start.txt', 'r')
            self.bot.send_message(message.chat.id, f.read(), reply_markup=keyboard1)
        elif message.text == '/version':
            self.log(message)
            f = open('version.txt', 'r')
            self.bot.send_message(message.chat.id, f.read(), reply_markup=keyboard_help)
        elif message.text == '/help':
            f = open('help.txt', 'r')
            self.bot.send_message(message.chat.id, f.read(), reply_markup=keyboard_help)
        else:
            text = 'bad'
            self.sendMes(message, text)
        f.close()

    def translate(self,message):
        url = 'https://translate.yandex.net/api/v1.5/tr.json/translate?' 
        key = 'trnsl.1.1.20200420T153840Z.c64aa64b1ef12707.339289160fc33c01cc0c66ce2604c7200714bf48' 
        langs = ['ru-en','ru-de' ,'ru-tt' ,'ru-uk']
        langs_name = ['на английский', 'на немецкий', 'на татарский', 'на украинский']
        message_revers = message.text[::-1]
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
        temp = message_revers[:endword]
        text_lang = temp[::-1] 
        ir = 0
        lang = ''
        ind = False
        while ir <= len(langs_name):
            if ir == len(langs_name):
                self.sendMes(message, 'Такого языка ещё нет в базе или он не существует!')
                ind = True
                break
            if langs_name[ir] == text_lang:
                lang = langs[ir]
                break
            ir += 1 
        if ind == False:
            text = message.text[9:(len(message.text) - endword)] 
            reque = requests.get(url, data={'key': key, 'text': text, 'lang': lang})
            translated = reque.json()
            self.sendMes(message, translated["text"])

#Я знаю что можно написать list[::-1]
    def revers(self, text):
        message_revers = ''
        i = len(text)
        while i > 0:
            i -= 1 
            message_revers += text[i]
        return message_revers
    
    def log(self, message):
        history = open('history.txt', 'a')
        print('Message {1} from {0}\n\n-----------------------------\n'.format(message.from_user.first_name, message.text))
        history.write( '@' + str(message.chat.username) + ' ' + str(message.chat.id) + ' ' + str(message.from_user.first_name) + ' ' + str(message.content_type) + ' - ' + str(message.text) + ' ' + time.ctime() + '\n')
        history.close()