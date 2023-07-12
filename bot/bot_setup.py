import telebot
import os
from dotenv import load_dotenv
from telebot import types
from weather.get_weather import Weather

load_dotenv()
bot = telebot.TeleBot(os.getenv('bot_token'))


class Bot:
    def __init__(self, start_argument):
        self.start_argument = start_argument
        self.path = 'data/city_list.txt'

    def bot_start(self, start_message, btn1_message, btn2_message):
        @bot.message_handler(commands=[self.start_argument])
        def start_bot(message):
            if btn1_message is not None and btn2_message is not None:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                btn1 = types.KeyboardButton(btn1_message, request_contact=True)
                btn2 = types.KeyboardButton(btn2_message, request_location=True)
                markup.add(btn1, btn2)
                message = bot.send_message(message.from_user.id, start_message, reply_markup=markup)
            else:
                message = bot.send_message(message.from_user.id, start_message)
            return message

    def check_city(self, text):
        with open(self.path, 'r') as f:
            data = f.read()
            if text in data:
                message = text
            else:
                message = False
            return message

    def bot_reply(self, reply_answer):
        @bot.message_handler(content_types=['text'])
        def bot_answer(message):
            check_city_from_message = self.check_city(message.text)
            if check_city_from_message is not False:
                weather = Weather(check_city_from_message)
                bot.send_message(message.from_user.id, weather.get_temperature())
            else:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                btn1 = types.KeyboardButton('Show weather for your location', request_location=True)
                btn2 = types.KeyboardButton('Show the weather in your city')
                markup.add(btn1, btn2)
                bot.send_message(message.from_user.id, reply_answer, reply_markup=markup)
    def weather_send(self):
        @bot.message_handler(content_types=['location'])
        def send_weather_by_location(message):
            location = _return_usere_location(message)
            weather = Weather(location)
            bot.send_message(message.from_user.id, weather.get_temperature())

        def _return_usere_location(message):
            user_longitude = message.location.longitude
            user_latitude = message.location.latitude
            return str(user_latitude) + ',' + str(user_longitude)


    def bot_pull(self):
        bot.polling(none_stop=True, interval=0)  # обязательная для работы бота часть
