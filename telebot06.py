import dotenv
from os import environ
from OWM import TOWM
import telebot
from telebot import types
from random import randint


dotenv.load_dotenv('.env')
bot_token = environ['bot_token']
owm_token = environ['owm']
owm = TOWM(owm_token)
bot = telebot.TeleBot(bot_token)


@bot.message_handler(commands=['start'])
def start(message: types.Message):
	username = message.from_user.username
	msg = f"<b>Здравствуй</b>, <i>{username}!</i>\nВведите /help - для справки"
	bot.send_message(message.chat.id, msg, parse_mode='html')

@bot.message_handler(commands=['help'])
def help(message: types.Message):
	text_help = 'Введите одну из слудующих команд:\n' \
	            '<b>Основные команды:</b>\n' \
	            '/start - Для начала работы\n' \
	            '/weather <i>Название Города</i> - прогноз погоды\n' \
	            '/погода <i>Название Города</i> - прогноз погоды\n' \
	            '\n<b>Дополнительные команды:</b>\n' \
	            '/coin - Подбросить монетку\n' \
	            '/whoami - Вывести имя пользователя\n' \
	            '/website - Вывести исформацию о вебсайте разработчика\n' \
	            '/about - Подробная информация о боте\n' \
	            '/qr - Получить ссылку на страничку разработчика\n' \
	            '/help - Вывести справку о доступных командах'
	bot.send_message(message.chat.id, text_help, parse_mode='html')


@bot.message_handler(commands=['weather', 'погода'])
def weather(message: types.Message):
	command = message.text
	city = command.split(maxsplit=1)[1]
	weather = owm.get_weather(city)
	bot.send_message(message.chat.id, weather)

@bot.message_handler(commands=['whoami'])
def whoami(message: types.Message):
	first_name = message.from_user.first_name
	last_name = message.from_user.last_name
	username = message.from_user.username
	user_id = message.from_user.id
	whoami_msg = f"first name: {first_name}\n" \
	             f"last name: {last_name}\n" \
	             f"user name: {username}\n" \
	             f"id: {user_id}"
	bot.send_message(message.chat.id, whoami_msg)

@bot.message_handler(commands=['qr'])
def qr(message: types.Message):
	pic = open('z-qr.png', 'rb')
	bot.send_photo(message.chat.id, pic)


@bot.message_handler(commands=['website'])
def website(message: types.Message):
	markup = types.InlineKeyboardMarkup()
	website = types.InlineKeyboardButton("Посетить веб сайт", url="https://ds-portfolio.netlify.app")
	markup.add(website)
	bot.send_message(message.chat.id, '<a href="https://ds-portfolio.netlify.app">Website</a>', parse_mode='html', reply_markup=markup)

@bot.message_handler(commands=['about'])
def about(message: types.Message):
	text = 'Created by: <b>EPluribusNEO</b>\n' \
	       'WebSite: <a href="https://ds-portfolio.netlify.app">Website</a>\n' \
	       'GitHub: <a href="https://github.com/EpluribusNEO">GitHub</a>\n' \
	       'Date: 18 November 2022\n' \
	       '\nВведите /help для получения справки по командам.'
	markup = types.InlineKeyboardMarkup()
	github = types.InlineKeyboardButton("GitHub", url="https://github.com/EpluribusNEO")
	website = types.InlineKeyboardButton("Website", url="https://ds-portfolio.netlify.app")
	markup.add(website, github)
	bot.send_message(message.chat.id, text, parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['photo'])
def get_user_photo(message: types.Message):
	bot.send_message(message.chat.id, 'Классная фотка!')

@bot.message_handler(content_types=['sticker'])
def get_sticker(message: types.Message):
	bot.send_message(message.chat.id, "вы отправили стикер")


@bot.message_handler(commands=['coin'])
def coin(message: types.Message):
	if randint(0, 100000) % 2 == 0:
		coin_status = "Орёл"
	else:
		coin_status = "Решка"
	bot.send_message(message.chat.id, f"<b>{coin_status}</b>", parse_mode='html')


bot.polling(non_stop=True)
