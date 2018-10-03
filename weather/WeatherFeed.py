import requests
import json
from collections import namedtuple
import datetime
import config

class WeatherFeed(object):

	def __init__(self):
		self.cityID = config.weather['cityID']
		self.unitFmt = config.weather['unitFormat']
		self.language = config.weather['language']
		self.apiKey = config.weather['apiKey']
		self.baseURL = 'http://api.openweathermap.org/data/2.5/'

		
	def get_current_weather(self):
		url = '{0}weather?id={1}&{2}'.format(self.baseURL, 
				self.cityID, self._get_url_end())
				
		try:
			response = requests.get(url)
			
			status = json.loads(response.text, object_hook = lambda d: namedtuple('CurrentWeather', d.keys())(*d.values()))
			w = status.weather[0]
			sunrise = datetime.datetime.fromtimestamp(status.sys.sunrise)
			sunset = datetime.datetime.fromtimestamp(status.sys.sunset)
			
			#Build the return object
			currentWeather = WeatherStatus(w.description, 
					self.get_weather_img(w.id, w.icon), status.main.temp,
					status.wind.speed, self._get_wind_direction(status.wind.deg),
					sunrise, sunset)
					
			return currentWeather
		except Exception as e:
			print(datetime.datetime.now().strftime('%c') + ' - current weather - ' + str(e))
			return None
		
		
	def get_upcoming_forecast(self, dayCount):
		if dayCount < 1 or dayCount > 16:
			raise ValueError("dayCount must be between 1 and 16 (inclusive)")
		
		fList = list()
		url = '{0}forecast/daily?id={1}&cnt={2}&{3}'.format(
				self.baseURL, self.cityID, dayCount, self._get_url_end())
		
		try:
			response = requests.get(url)
			
			forecast = json.loads(response.text, object_hook = lambda d: namedtuple('Forecast', d.keys())(*d.values()))
			
			#Create an object for each day and add it to the list
			for day in forecast.list:
				w = day.weather[0]
			
				obj = Forecast(datetime.datetime.fromtimestamp(day.dt),
					day.temp.min, day.temp.max, day.temp.day, day.temp.night,
					w.description, self.get_weather_img(w.id, w.icon),
					day.speed, self._get_wind_direction(day.deg))
					
				fList.append(obj)
		except Exception as e:
			print(datetime.datetime.now().strftime('%c') + ' - forecast - ' + str(e))
		
		return fList
		
		
	def get_weather_img(self, weatherID, weatherIcon):
		#Weather codes/meanings can be found here: http://openweathermap.org/weather-conditions
		
		if weatherID >= 200 and weatherID < 300:
			return 'Storm.png'
		elif weatherID >= 300 and weatherID < 600:
			return 'Rain.png'
		elif weatherID >= 600 and weatherID < 700:
			return 'Snow.png'
		elif weatherID >= 700 and weatherID < 800:
			if weatherID == 781:
				return 'Tornado.png'
			else:
				return 'Haze.png'
		elif weatherID >= 800 and weatherID < 900:
			if weatherID == 800:
				if weatherIcon.endswith('d'):
					return 'Sun.png'
				else:
					return 'Moon.png'
			elif weatherID == 801:
				if weatherIcon.endswith('d'):
					return 'PartlySunny.png'
				else:
					return 'PartlyMoon.png'
			else:
				return 'Cloud.png'
		elif weatherID >= 900 and weatherID < 903:
			return 'Tornado.png'
		elif weatherID == 905:
			return 'Wind.png'
		elif weatherID == 906:
			return 'Hail.png'
		else:
			return 'Newspaper.png'
			
	
	def _get_url_end(self):
		return 'units={0}&lang={1}&APPID={2}'.format(
				self.unitFmt, self.language, self.apiKey)
				
		
	def _get_wind_direction(self, degrees):
		if 11.25 <= degrees and degrees < 33.75:
			return 'NNE'
		elif 33.75 <= degrees and degrees < 56.25:
			return 'NE'
		elif 56.25 <= degrees and degrees < 78.75:
			return 'ENE'
		elif 78.75 <= degrees and degrees < 101.25:
			return 'E'
		elif 101.25 <= degrees and degrees < 123.75:
			return 'ESE'
		elif 123.75 <= degrees and degrees < 146.25:
			return 'SE'
		elif 146.25 <= degrees and degrees < 168.75:
			return 'SSE'
		elif 168.75 <= degrees and degrees < 191.25:
			return 'S'
		elif 191.25 <= degrees and degrees < 213.75:
			return 'SSW'
		elif 213.75 <= degrees and degrees < 236.25:
			return 'SW'
		elif 236.25 <= degrees and degrees < 258.75:
			return 'WSW'
		elif 258.75 <= degrees and degrees < 281.25:
			return 'W'
		elif 281.25 <= degrees and degrees < 303.75:
			return 'WNW'
		elif 303.75 <= degrees and degrees < 326.25:
			return 'NW'
		elif 326.25 <= degrees and degrees < 348.75:
			return 'NNW'
		else:
			return 'N'
			
			
class WeatherStatus(object):
	def __init__(self, description, image, currentTemp, windSpeed, windDirection, sunrise, sunset):
		self.description = description
		self.image = image
		self.currentTemp = currentTemp
		self.windSpeed = windSpeed
		self.windDirection = windDirection
		self.sunrise = sunrise
		self.sunset = sunset
		
class Forecast(object):
	def __init__(self, date, minTemp, maxTemp, dayTemp, nightTemp, description, image, windSpeed, windDirection):
		self.date = date
		self.minTemp = minTemp
		self.maxTemp = maxTemp
		self.dayTemp = dayTemp
		self.nightTemp = nightTemp
		self.description = description
		self.image = image
		self.windSpeed = windSpeed
		self.windDirection = windDirection
		

	
