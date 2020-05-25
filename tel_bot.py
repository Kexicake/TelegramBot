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
            f.close()
        elif message.text == '/version':
            self.log(message)
            f = open('version.txt', 'r')
            self.bot.send_message(message.chat.id, f.read(), reply_markup=keyboard_help)
            f.close()
        elif message.text == '/help':
            f = open('help.txt', 'r')
            self.bot.send_message(message.chat.id, f.read(), reply_markup=keyboard_help)
            f.close()
        else:
            text = 'bad'
            self.sendMes(message, text)
        

    def translate(self,message):
        translating = ['https://translate.yandex.net/api/v1.5/tr.json/translate?', 'trnsl.1.1.20200420T153840Z.c64aa64b1ef12707.339289160fc33c01cc0c66ce2604c7200714bf48', 'ru-en' ]  
        langs = ['ru-en','ru-de' ,'ru-tt' ,'ru-uk']
        langs_name = ['на английский', 'на немецкий', 'на татарский', 'на украинский']
        lang_num = 12
        lang_mes = ''
        if message.text[9:12] == "на ":
            while True:
                if message.text[lang_num] == ' ':
                    break
                lang_mes += message.text[lang_num]

        self.sendMes(message, message.text[9::12])
            #text = message.text[9:(len(message.text) - endword_count)] 
            #reque = requests.get(translating[0], data={'key': translating[1], 'text': text, 'lang': translating[2]})
            #translated = reque.json()
            #self.sendMes(message, translated["text"])

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