import telebot
bot = telebot.TeleBot("1756808541:AAGWdleEfSOPAKDv___PCKya5gslfk0zCDU")	
#СОЗДАНИЕ КЛАВИАТУРЫ
keyboard1 = telebot.types.ReplyKeyboardMarkup(True,True, True, True)
keyboard1.add("Нефтеюганск").add("Актировка ❄").add("Погода 🌥").add("Уведомление")
#ПОГОДА НЕФТЕЮГАНСК
def weather(message):
	from pyowm import OWM
	from pyowm.utils.config import get_default_config
	from pyowm.utils import timestamps
	config_dict = get_default_config()
	config_dict['language'] = 'ru'
	owm = OWM('0e8e832bc162b464e1a54f9b5af9c0e6',config_dict)
	mgr = owm.weather_manager()
	observation = mgr.weather_at_place('Нефтеюганск')
	w = observation.weather
	t = w.temperature('celsius')
	#градусы
	t = t['temp']
	#ощущения
	feeling = w.temperature('celsius')['feels_like']
	#скорость ветра
	Speed = w.wind()['speed']
	#влажность
	humi = w.humidity
	#облачность
	Clouds = w.clouds
	#статус
	status = w.detailed_status
	#давление
	pr = w.pressure['press']
	#видимость
	vd = w.visibility_distance

	bot.send_message(message.chat.id,  f'''Сейчас в г.Нефтеюганск:
Температура около {t} ℃ 
Ощущается как {feeling} ℃ 
Статус:  {status} 
Скорость ветра: {Speed} м/с 
Облачность: {Clouds} % 
Влажность: {humi} %
Давление: {pr} мм.рт.ст 
Видимость: {vd} м.''')
def url(message):
    markup = telebot.types.InlineKeyboardMarkup()
    pogoda = telebot.types.InlineKeyboardButton(text='Яндекс.Погода', url='https://yandex.ru/pogoda/nefteugansk')
    markup.add(pogoda)
    bot.send_message(message.chat.id, "Если хотите, можете узнать погоду на сайте \"Яндекс.Погода\".", reply_markup = markup)

def admin(message):
    markup = telebot.types.InlineKeyboardMarkup()
    pogoda = telebot.types.InlineKeyboardButton(text='Администрация города', url='http://www.admugansk.ru/')
    markup.add(pogoda)
    bot.send_message(message.chat.id, "Узнайте актировку на сайте администрации г.Нефтеюганск.", reply_markup = markup)

place = ''
number = ''

#ПРИВЕТСТВИЕ
@bot.message_handler(commands = ['start'])
def welcome(message):
	bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAO_YGhfsT041mQbrlnxwB_TzOh8GUsAAicDAAK1cdoGD_Tez6DF3eweBA')
	bot.send_message(message.chat.id, 'Приветствую Вас, {}.Что Вам угодно? Прежде чем пользоваться ботом ознакомьтесь с его функциями, прописав "помощь".'.format(message.from_user.first_name), reply_markup = keyboard1)
#РЕАКЦИЯ НА ТЕКСТ.
@bot.message_handler(content_types = ['text'])
def answer(message):
	if message.text == "Погода 🌥" or  message.text.lower() == "погода":
		bot.send_message(message.from_user.id , "Погоду в каком городе вы хотите узнать?")
		bot.register_next_step_handler(message , place)
	elif message.text.lower() == "нефтеюганск" :
		weather(message)
		url(message)
	elif message.text.lower() == "помощь":
		bot.send_message(message.chat.id,'''
Как узнать погоду.
Для того чтобы узнать погоду нужно нажать на клавишу "Погода 🌥" или написать боту слово "погода" (можно писать как большими буквами, так и маленькими) без кавычек. Затем, ввести название города, в котором вы хотите узнать погоду (можно с маленькой буквы или на английском языке).Всё!

Нефтеюганск и Актировки.
Клавиша "Нефтеюганск" или слово "Нефтеюганск", написанное боту (большими или маленькими буквами) без кавычек, отвечают за погодные данные в этом городе.
Клавиша "Актировка ❄" или слово "Актировка", написанное боту (большими или маленькими буквами) без кавычек, отвечают за актировки в городе Нефтеюганск.

Как работают уведомления.
Для того чтобы выставить уведомление, нужно нажать на клавишу "Уведомление" или написать боту слово "уведомление" (можно писать как большими буквами, так и маленькими) без кавычек. Затем, после сообщения "Введите время:" от бота вы должны вписать число (в часах),то есть, через какое время вы хотите получить погодные данные. Например: Вы вводите 5.25, это значит, что через 5 часов 25 минут вам придёт уведомление о погоде. Еще примеры: 0.01 это 1 минута, 1.00 или 1 это 1 час и тд. Пока что уведомления распространяются только на город Нефтеюганск и показываются ЕДИНОЖДЫ (только 1 раз).Потом нужно проделывать все действия заново.  Если случайно нажали на клавишу "Уведомление" (не хотели выставлять уведомления) напишите "-" боту.

Бот отвечает на фразы: "Привет", "Здравствуйте", "Пока", "До свидания", "Как дела", реагирует на текст, стикеры, может отправить вам песню и тд.Его даже можно похвалить, написав "Ты лучший" или "Ты супер".
 ''')
	elif message.text == "Уведомление" or message.text.lower() == "уведомление":
		bot.send_message(message.from_user.id , "Введите время: (пример: 0.02 это 2 минуты. 2.00 или 2 это 2 часа)")
		bot.register_next_step_handler(message , number)
	elif message.text == "Актировка ❄" or message.text.lower()== 'актировка':
		admin(message)
	elif (message.text.lower() == 'привет' or message.text.lower() == 'здравствуйте' or message.text.lower() == 'здравствуй'):
		bot.send_message(message.chat.id, "Здравствуйте!")
	elif message.text.lower() == 'как дела?' or message.text.lower() == 'как дела':
		bot.send_message(message.chat.id , "Это новый Каддилак!")
	elif message.text.lower() == "песня":
		bot.send_message(message.chat.id , "Хит")
		audio = open("chin chan.mp3" , "rb")
		bot.send_audio(message.chat.id , audio )
		audio.close()
	elif (message.text.lower() == "александр" or message.text.lower() == "саша" or message.text.lower() == 'автор') :
		bot.send_message(message.chat.id , "Александр Явонов - мой создатель 👦.Что я могу про него сказать..Гений")
	elif (message.text.lower() == "пока" or message.text.lower() == "до свидания"):
		bot.send_message(message.chat.id , "До связи!")
	elif message.text.lower() == 'ты лучший' or message.text.lower() == 'ты супер':
		bot.send_sticker(message.chat.id , "CAACAgIAAxkBAAIF_2BtqtWdZ7LvTNXZuWHRWpZHImQoAAL1AwACcBFhCNq3TDN6JU9hHgQ")
		bot.send_message(message.chat.id , "Спасибо!")
	elif message.text.lower()== 'ты пидр':
		bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAIbVGCuiS7k-NsJd-UNOzHtAp8YGTlLAALZdQEAAWOLRgzB7X6CN74_WB8E' )
	else:
		bot.send_sticker(message.chat.id, 'CAACAgQAAxkBAAIbo2CukS6YjiohsrYRkYa6picrvWvhAAJmAAP44AQCLDkxgUcZcAgfBA')
		bot.send_message(message.chat.id, "У меня el problema..Я вас не понимаю 😬")

#РЕАКЦИЯ НА СТИКЕРЫ.
@bot.message_handler(content_types = ['sticker'])
def otvet(message):
	photo = open("1.jpg","rb")
	bot.send_photo(message.chat.id, photo)
	photo.close()
#ПОГОДА ПО ВСЕМУ МИРУ
def place(message):
	place = message.text
	#ПАРСИНГ С САЙТА
	try:
		from pyowm.commons.exceptions import NotFoundError
		from pyowm import OWM
		from pyowm.utils.config import get_default_config
		config_dict = get_default_config()
		config_dict['language'] = 'ru'
		owm = OWM('0e8e832bc162b464e1a54f9b5af9c0e6',config_dict)
		mgr = owm.weather_manager()
		observation = mgr.weather_at_place(place)
		w = observation.weather
		t = w.temperature('celsius')
		#градусы
		t = t['temp']
		#ощущения
		feeling = w.temperature('celsius')['feels_like']
		#скорость ветра
		Speed = w.wind()['speed']
		#влажность
		humi = w.humidity
		#облачность
		Clouds = w.clouds
		#статус
		status = w.detailed_status
		#давление
		pr = w.pressure['press']
		#видимость
		vd = w.visibility_distance
		bot.send_message(message.chat.id,  f'''Сейчас в г.{place}:
Температура около {t} ℃ 
Ощущается как {feeling} ℃ 
Статус:  {status} 
Скорость ветра: {Speed} м/с 
Облачность: {Clouds} % 
Влажность: {humi} %
Давление: {pr} мм.рт.ст 
Видимость: {vd} м.''')
		try:
			if place == "Санкт-Петербург" or place == "Санкт Петербург" or place == "Питер":
				markup = telebot.types.InlineKeyboardMarkup()
				pogoda = telebot.types.InlineKeyboardButton(text='Яндекс.Погода', url='https://yandex.ru/pogoda/saint-petersburg')
				markup.add(pogoda)
				bot.send_message(message.chat.id, "Если хотите, можете узнать погоду на сайте \"Яндекс.Погода\".", reply_markup = markup)
			elif place.lower() == "новый афон":
				markup = telebot.types.InlineKeyboardMarkup()
				pogoda = telebot.types.InlineKeyboardButton(text='Яндекс.Погода', url='https://yandex.ru/pogoda/new-athos')
				markup.add(pogoda)
				bot.send_message(message.chat.id, "Если хотите, можете узнать погоду на сайте \"Яндекс.Погода\".", reply_markup = markup)

			else:	
				from textblob import TextBlob 
				blob = TextBlob(place)
				translation = blob.translate(to='en')
				markup = telebot.types.InlineKeyboardMarkup()
				pogoda = telebot.types.InlineKeyboardButton(text='Яндекс.Погода', url='https://yandex.ru/pogoda/' + str(translation))
				markup.add(pogoda)
				bot.send_message(message.chat.id, "Если хотите, можете узнать погоду на сайте \"Яндекс.Погода\".", reply_markup = markup)
		except:
			markup = telebot.types.InlineKeyboardMarkup()
			pogoda = telebot.types.InlineKeyboardButton(text='Яндекс.Погода', url='https://yandex.ru/pogoda/' + str(place))
			markup.add(pogoda)
			bot.send_message(message.chat.id, "Если хотите, можете узнать погоду на сайте \"Яндекс.Погода\".", reply_markup = markup)

	except NotFoundError:
		bot.send_message(message.chat.id , "Город не найден.Попробуйте проделать все действия заново и проверьте правильность введённых данных.")

#РАБОТА С УВЕДОМЛЕНИЯМИ
def number(message):
	try:
		number = float(message.text)
		bot.send_message(message.chat.id , "Уведомления успешно включены ✔")
		hour = number // 1
		hour = hour * 3600
		minutes = number % 1
		minutes = minutes * 6000
		total =int(hour + minutes)
		import time
		run = 0
		while run < 1:
			time.sleep(total)
			weather(message)
			url(message)
			run = run + 1
			
	except ValueError:
		bot.send_message(message.chat.id , "Вы неправильно ввели время.Проделайте все действия заново.")

#ЗАПУСК БОТА
bot.polling(none_stop = True, interval = 0)
