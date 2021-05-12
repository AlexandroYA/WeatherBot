import telebot
import config
bot = telebot.TeleBot(config.TOKEN)	
#СОЗДАНИЕ КЛАВИАТУРЫ
keyboard1 = telebot.types.ReplyKeyboardMarkup(True,True, True, True)
keyboard1.add("Нефтеюганск").add("Актировка ❄").add("Погода 🌥").add("Уведомление")
#ПОГОДА НЕФТЕЮГАНСК
def weather(message):
	from pyowm import OWM
	from pyowm.utils.config import get_default_config
	config_dict = get_default_config()
	config_dict['language'] = 'ru'  # Устанавливаю язык
	owm = OWM('0e8e832bc162b464e1a54f9b5af9c0e6',config_dict)
	mgr = owm.weather_manager()
	weather = mgr.weather_at_place('Нефтеюганск').weather
	Observation = mgr.weather_at_place('Нефтеюганск')
	temperature = weather.temperature()
	temp_celcius = weather.temperature('celsius')['temp']

	wind = Observation.weather.wind()["speed"]
	status = weather.detailed_status
	feel = weather.temperature('celsius')['feels_like']
	bot.send_message(message.chat.id , "Сейчас в городе Нефтеюганск "  + str(status) + ".Погода около " + str(temp_celcius) +"℃.Ощущается как " + str(feel) +"℃. Скорость ветра - " + str(wind) + " м/с")

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
	elif message.text.lower() == "помощь":
		bot.send_message(message.chat.id,'''
Как узнать погоду.
Для того чтобы узнать погоду, нужно нажать на клавишу "Погода 🌥" или написать боту слово "погода" (можно писать как большими буквами, так и маленькими), без кавычек.
Затем, ввести название города, в котором вы хотите узнать погоду (можно с маленькой буквы).Всё!

Клавиша "Нефтеюганск" отвечает за погодные данные в этом городе.
Клавиша "Актировка ❄" отвечает за актировки в городе Нефтеюганск.

Как работает уведомление.
Для того чтобы выставить уведомление, нужно нажать на клавишу "Уведомление" или написать боту слово "уведомление" (можно писать как большими буквами, так и маленькими), без кавычек.
Затем, после сообщения "Введите время:" от бота вы должны вписать число (в часах),то есть, через какое время вы хотите получить погодные данные.
Например: Вы вводите 5.25, это значит, что через 5 часов 25 минут вам придёт уведомление о погоде.0.01 это 1 минута, 1.00 это 1 час и тд.
Пока что уведомления расспространяются только на город Нефтеюганск и показываются ЕДИНОЖДЫ (только 1 раз).Потом нужно вводить время заново. 
Если случайно нажали на клавишу "Уведомление" (не хотели выставлять уведомления) напишите "-" боту.

Бот отвечает на фразы: "Привет", "Здравствуйте", "Пока", "До свидания", "Как дела", реагирует на текст и тд.Его даже можно похвалить, написав "Ты лучший".
 ''')
	elif message.text == "Уведомление" or message.text.lower() == "уведомление":
		bot.send_message(message.from_user.id , "Введите время: (пример - 0.02 это 2 минуты. 1.00 это 1 час)")
		bot.register_next_step_handler(message , number)
		
	elif message.text == "Актировка ❄":
		bot.send_sticker(message.chat.id , 'CAACAgQAAxkBAAICWmBrM1HNHi_BunJhqJCfeixr6AgPAAJSAANYbbUuT78Ij70qRAYeBA')
		bot.send_message(message.chat.id , "К сожалению, Актировки НЕТ.Занятия проводятся в обычном режиме.Удачи..")
	elif (message.text.lower() == 'привет' or message.text.lower() == 'здравствуйте' or message.text.lower() == 'здравствуй'):
		bot.send_message(message.chat.id, "Здравствуйте!")
	elif message.text.lower() == 'как дела?' or message.text.lower() == 'как дела':
		bot.send_message(message.chat.id , "Норм.")
	elif message.text.lower() == "песня":
		bot.send_message(message.chat.id , "Хит")
		audio = open("chin chan.mp3" , "rb")
		bot.send_audio(message.chat.id , audio )
		audio.close()
	elif (message.text.lower() == "александр" or message.text.lower() == "саша"):
		bot.send_message(message.chat.id , "Александр Явонов - мой создатель 🤖.Что я могу про него сказать..Гений")
	elif (message.text.lower() == "пока" or message.text.lower() == "до свидания"):
		bot.send_message(message.chat.id , "До связи!")
	elif message.text.lower() == 'ты лучший' or message.text.lower() == 'ты супер':
		bot.send_sticker(message.chat.id , "CAACAgIAAxkBAAIF_2BtqtWdZ7LvTNXZuWHRWpZHImQoAAL1AwACcBFhCNq3TDN6JU9hHgQ")
		bot.send_message(message.chat.id , "Спасибо!")
	else:
		bot.send_message(message.chat.id, "Я вас не понимаю 😬")

#РЕАКЦИЯ НА СТИКЕРЫ.
@bot.message_handler(content_types = ['sticker'])
def otvet(message):
	bot.send_message(message.chat.id , "Зачем мне стикер?!Думаешь МНЕ не все равно?")
#ПОГОДА ПО ВСЕМУ МИРУ
def place(message):
	place = message.text
	#ПАРСИНГ С САЙТА
	try:
		from pyowm import OWM
		from pyowm.utils.config import get_default_config
		from pyowm.commons.exceptions import NotFoundError
		config_dict = get_default_config()
		config_dict['language'] = 'ru'  # Устанавливаю язык
		owm = OWM('0e8e832bc162b464e1a54f9b5af9c0e6',config_dict)
		mgr = owm.weather_manager()
		weather = mgr.weather_at_place(place).weather
		Observation = mgr.weather_at_place(place)
		temperature = weather.temperature()
		temp_celcius = weather.temperature('celsius')['temp']
		wind = Observation.weather.wind()["speed"]
		status = weather.detailed_status
		feel = weather.temperature('celsius')['feels_like']
		bot.send_message(message.chat.id , "Сейчас в городе " + place + " " + str(status) + ".Погода около " + str(temp_celcius) + "℃.Ощущается как " + str(feel) + "℃ " + ".Скорость ветра - "  + str(wind) + " м/с")
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
			run = run + 1
	except ValueError:
		bot.send_message(message.chat.id , "Вы неправильно ввели время.Проделайте все действия заново.")

#ЗАПУСК БОТА
bot.polling(none_stop = True, interval = 0)