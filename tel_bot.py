import telebot, requests, json, wikipedia, time, adodbapi, PyMySQL

class Tel_bot:
    def __init__(self,token):
        """Constructor"""
        self.bot = telebot.TeleBot(token)
        print('\n-----------------------------\n\nConstruction complit!')

    def sendMes(self, message, text):
        self.bot.send_message(message.chat.id, text)

    def command(self, message):
        keyboards = [telebot.types.ReplyKeyboardMarkup(True), telebot.types.ReplyKeyboardMarkup(True)]
        keyboards[0].row('/start', '/help', '/revers', '/translate')
        keyboards[1].row('/help')

        self.log(message)
        if message.text == '/test':
            text = 'test pass'
            self.bot.send_message(message.chat.id, text, reply_markup=keyboards[0])
        elif message.text == '/start':
            f = open('start.txt', 'r')
            self.bot.send_message(message.chat.id, f.read(), reply_markup=keyboards[0])
        elif message.text == '/version':
            self.log(message)
            f = open('version.txt', 'r')
            self.bot.send_message(message.chat.id, f.read(), reply_markup=keyboards[1])
        elif message.text == '/help':
            f = open('help.txt', 'r')
            self.bot.send_message(message.chat.id, f.read(), reply_markup=keyboards[1])
        else:
            return
        f.close()
        
    def opr(self, message):
        wikipedia.set_lang("ru")
        self.sendMes(message, wikipedia.summary(message.text[9::], sentences = 2))

    def translate(self,message):
        translating = ['https://translate.yandex.net/api/v1.5/tr.json/translate?', 'trnsl.1.1.20200420T153840Z.c64aa64b1ef12707.339289160fc33c01cc0c66ce2604c7200714bf48', 'ru-en' ]  
        
        langs = [['ru-en','ru-de' ,'ru-tt' ,'ru-uk'],['английский', 'немецкий', 'татарский', 'украинский']]
        lang_num = 12
        lang_mes = ''
        
        #Проверка на указание языка
        if message.text[9:11] == "на":
            #Извлечение языка на который надо перевести
            while True:
                if lang_num == len(message.text) or  message.text[lang_num] == ' ' :
                    break
                lang_mes += message.text[lang_num]
                lang_num += 1
            #Переводим язык в машинный вид
            for i in range(len(langs[1])+1):
                if i == (len(langs[1])):
                    self.sendMes(message, "ERROR: Языка не существует или его нет в базе")
                    return
                if langs[1][i] == lang_mes:
                    translating[2] = langs[0][i]
                    break
        else:
            lang_num = 9
    
        reque = requests.get(translating[0], data={'key': translating[1], 'text': message.text[lang_num::], 'lang': translating[2]})
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
        print('\n-----------------------------\n\nMessage {1} from {0}\n'.format(message.from_user.first_name, message.text))
        history.write( '@' + str(message.chat.username) + ' ' + str(message.chat.id) + ' ' + str(message.from_user.first_name) + ' ' + str(message.content_type) + ' - ' + str(message.text) + ' ' + time.ctime() + '\n')
        history.close()