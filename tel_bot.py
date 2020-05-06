import telebot, requests, json, wikipedia, time, adodbapi
class Tel_bot:
    def __init__(self,token):
        """Constructor"""
        self.bot = telebot.TeleBot(token)
        print('Construction complit!\n-----------------------------\n')
    
    def sendMes(self, message, text):
        self.bot.send_message(message.chat.id, text)
    def sendMesK(self, message, text, keyboard):
        self.bot.send_message(message.chat.id, text, reply_markup=keyboard)

    def command(self, message):
        self.log(message)
        if message.text == '/test':
            text = 'test pass'
        elif message.text == '/start':
            f = open('start.txt', 'r')
            self.bot.send_message(message.chat.id,  f.read(), reply_markup=keyboard1)
            f.close()
        else:
            text = 'bad'
        self.sendMes(message, text)
    def log(self, message):
        history = open('history.txt', 'a')
        print('Message {1} from {0}\n\n-----------------------------\n'.format(message.from_user.first_name, message.text))
        history.write( '@' + str(message.chat.username) + ' ' + str(message.chat.id) + ' ' + str(message.from_user.first_name) + ' ' + str(message.content_type) + ' - ' + str(message.text) + ' ' + time.ctime() + '\n')
        history.close()