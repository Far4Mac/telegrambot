import json
import constants
import urllib

with open('city.list.json') as data_file:
    cities = json.load(data_file)

def get_city_id(location):
    for city in cities:
        if location.capitalize() == city['name']:
            return city['id']
    return False

def get_weather(city):
    url = 'http://api.openweathermap.org/data/2.5/weather?id={}&appid={}'
    city_id = get_city_id(city)
    if city_id:
        link = urllib.urlopen(url.format(city_id, constants.apikey))
        weather = json.loads(link.read())
        result = 'Weather: ' + str(weather['weather'][0][u'description']) + \
                  '\nTemperature: ' + str(kelvin_to_celsius(weather[u'main'][u'temp'])) +  \
                  '\nWind speed: ' + str(weather[u'wind'][u'speed']) + \
                  '\nClouds: ' + str(weather[u'clouds'][u'all'])
        return result
    else:
        return 'error'

def get_weather_daily(city, days):
    url = 'http://api.openweathermap.org/data/2.5/forecast/daily?id={}&cnt={}&appid={}'
    city_id = get_city_id(city)
    if city_id:
        result = ''
        link = urllib.urlopen(url.format(city_id, days, constants.apikey))
        weather = json.loads(link.read())
        for i,day in enumerate(weather[u'list']):
            result += 'Day ' + str(i) + \
                '\nWeather: ' + day[u'weather'][0][u'description'] + \
                '\nTemperature: ' + str(kelvin_to_celsius(day[u'temp'][u'day'])) +  \
                '\nWind speed: ' + str(day[u'speed']) + \
                '\nClouds: ' + str(day[u'clouds']) + '\n\n'
        return result
    else:
        return 'error'

def kelvin_to_celsius(temp):
    return temp - 273.15