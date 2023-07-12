import os
from dotenv import load_dotenv
import requests

load_dotenv()


class WeatherResponse:
    def __init__(self, response):
        self.body = response.json()

    def _get_current(self):
        return self.body['current']

    def _get_location(self):
        return self.body["location"]

    def get_region(self):
        return self._get_location()["region"]

    def get_current(self):
        return self._get_location()["region"]

    def get_weather_text(self):
        return self._get_current()['condition']['text']

    def get_temp_in_celsius(self):
        return self._get_current()['temp_c']


class Weather:
    def __init__(self, querry):
        self.querry = querry
        self.lang = 'ru'
        self._api = os.getenv('api')
        self._token = os.getenv('weather_token')

    def get_temperature(self):
        response = requests.get(self._get_url())
        return self._format_response(response)

    def _get_url(self):
        return f'{self._api}?key={self._token}&q={self.querry}&aqi=no&lang={self.lang}'

    def _format_response(self, response):
        if response.status_code == 200:
            weather_response = WeatherResponse(response)
            message = f'The Weather in {weather_response.get_region()} is {weather_response.get_temp_in_celsius()}°C ' \
                      f'and situation is {weather_response.get_weather_text()} '
        else:
            message = response.text
        return message
