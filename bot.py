import logging, requests, telebot, wikipedia, json, time

class Tel_bot:   
    def __init__(self, token):
        """Constructor"""
        with open('config.json', 'r', encoding='utf-8') as fh: #открываем файл на чтение
            self.config = json.load(fh) #загружаем из файла данные в словарь 
        self.bot = telebot.TeleBot(self.config['Bot']['Token']) #подключаем бота
        print("-----------------------------\n\nConstruction complit!\n\n-----------------------------", end='')

    def send(self,id,message):
            self.bot.send_message(id,message)

    def command(self, message):
        keyboards = [telebot.types.ReplyKeyboardMarkup(True), telebot.types.ReplyKeyboardMarkup(True)]
        keyboards[0].row('/start', '/help')

        if message.text == '/test':
            text = 'test pass'
            self.send(message.chat.id, text, reply_markup=keyboards[0])
        else:
            try:
                text = message.text[1:] + '.txt'
                with open(text, 'r', encoding='utf-8') as fh: #открываем файл на чтение
                    self.send(message.chat.id, fh.read())   
            except:
                self.send(message.chat.id, 'Я не знаю такую команду(')

    def definition(self, message):
        wikipedia.set_lang("ru")
        try:
            self.send(message.chat.id, wikipedia.summary(message.text[9::], sentences=2))
        except:
            self.send(message.chat.id, 'Хмм...\n почему-то не могу выполнить запрос, попробуй написать по другому :(')

    def translate(self, message):
        lang = 'ru-en'
        langs = (('ru-en', 'ru-de',  'ru-uk'), ('на английский', 'на немецкий', 'на украинский'),(13, 11, 13))
        len_lang = 0

        for i in langs[1]:
            if message.text.endswith(i):
                lang = langs[0][langs[1].index(i)]
                len_lang = langs[2][langs[1].index(i)]
                break

        text = message.text[:8:-1]
        text = text[:len_lang:-1]
        reque = requests.get('https://translate.yandex.net/api/v1.5/tr.json/translate?',
                             data={'key': self.config['Translater']['key'], 'text': text, 'lang': lang})
        translated = reque.json()
        self.send(message.chat.id, translated["text"])

    def weather(self, message):
        try:
            res = requests.get("http://api.openweathermap.org/data/2.5/forecast",
                       params={'id': self.config['OpenWeather']['city_id'], 'units': 'metric', 'lang': 'ru', 'APPID': self.config['OpenWeather']['appid']})
            data = res.json()
            tim = time.strftime('%H')
            for i in range(22):
                if i >= int(tim) and i%3==0:
                    if len(str(i)) == 1:
                        tim = '0{0}'.format(str(i))
                    else:
                        tim = str(i)
                    break
                if i == 21:
                    tim = '00'
            for i in data['list']:
                if i['dt_txt'][11:13] == tim:
                    self.send(message.chat.id,'В ульяновске сейчас:\n{0:+3.0f} {1}'.format(i['main']['temp'],i['weather'][0]['description']))
                    break
        except:
            self.send(message.chat.id, 'Ой...\n Что-то пошло не так...')

    def sms(self, message):
        id=''
        id_b = True
        temp = ''
        for i in message[::-1]:
            if id_b:
                id += i
                if i == '@':
                    id_b = False
            else:
                temp += i
        message = ''
        temp = [i for i in temp]
        id = [i for i in id]
        temp.reverse()
        id.reverse()
        id = message.join(id)
        message = message.join(temp)
        print(message)
        print(id)

    def log(self, message):
        logging.basicConfig(level=logging.INFO, filename='log.log', format='%(asctime)s -%(message)s', datefmt='%d-%b-%y %H:%M:%S')
        logging.info(' @{0} chatID:{1}  username:{2} {3}  - massage: {4}'.format(str(message.chat.username), str(message.chat.id), str(message.from_user.first_name), str(message.content_type), str(message.text)))
        print('\n\nMessage {1} from {0}\n\n-----------------------------'.format(message.from_user.first_name, message.text), end='')
