import tkinter as tk
from weather.WeatherFeed import *
from PIL import Image, ImageTk
import datetime
import sys
import os
import config
from UtilMethods import size_image


class WeatherFrame(tk.Frame):
	def __init__(self, parent):
		tk.Frame.__init__(self, parent, bg='black')
		self.updateFreq = 1000 * 60 * 30 #30 minutes
		self.weatherFeed = WeatherFeed()
		
		self.weatherStatusFrame = CurrentWeatherFrame(self)
		self.weatherStatusFrame.pack(pady=15)
		
		self.forecastFrame = ForecastFrame(self)
		self.forecastFrame.pack()
		
		self.update_frame()
		
	def update_frame(self):
		#Update the current weather
		currentWeather = self.weatherFeed.get_current_weather()
		self.weatherStatusFrame.update_weather(currentWeather)	
		
		#Update the forecast
		dailyForecast = self.weatherFeed.get_upcoming_forecast(config.weather['forecastCount'])
		self.forecastFrame.update_forecast(dailyForecast)
		
		self.after(self.updateFreq, self.update_frame)

		
class CurrentWeatherFrame(tk.Frame):
	def __init__(self, parent):
		tk.Frame.__init__(self, parent, bg='black')
		self.pathname = os.path.dirname(__file__)
		
		self.weatherImgText = ''
		self.weatherImg = None
		self.windImg = size_image(30, 30, os.path.join(self.pathname, 'images/Wind.png'))

		self.varWind = tk.StringVar()
		self.varWind.set('')		
		self.lblWind = tk.Label(self, font=('Arial', 18), image=self.windImg, fg='white', bg='black', textvariable=self.varWind, compound=tk.LEFT)
		
		self.varTemp = tk.StringVar()
		self.varTemp.set('')	
		self.lblTemp = tk.Label(self, font=('Arial', 48), fg='white', bg='black', textvariable=self.varTemp)
		
		self.lblTemp.pack()
		self.lblWind.pack()
	
	def update_weather(self, status):
		degreeSymbol = '\u00b0'
		
		#Round the temp and wind values
		self.varTemp.set(' {0}{1}F'.format(round(status.currentTemp), degreeSymbol))
		self.varWind.set(' {0} {1} mph'.format(status.windDirection, round(status.windSpeed)))
		
		#Change the image if needed
		if status.image != self.weatherImgText:
			self.weatherImgText = status.image
			self.weatherImg = size_image(100, 100, os.path.join(self.pathname, 'images/' + status.image))
			self.lblTemp.config(image=self.weatherImg, compound=tk.LEFT)
		
		
class ForecastFrame(tk.Frame):
	def __init__(self, parent):
		tk.Frame.__init__(self, parent, bg='black')
		self.frameList = list()
		
		#Needed to keep images from getting destroyed by gc
		self.imageList = list()
		
	def create_day_frame(self, day):
		degreeSymbol = '\u00b0'
		frame = tk.Frame(self, bg='black')
		
		lblDate = tk.Label(frame, font=('Arial', 18), fg='white', bg='black', text=day.date.strftime('%a').upper())
		lblDate.grid(row=0)
		
		pathname = os.path.dirname(__file__)
		dayImg = size_image(30, 30, os.path.join(pathname, 'images/' + day.image))
		self.imageList.append(dayImg)
		
		lblImg = tk.Label(frame, bg='black', image=dayImg)
		lblImg.grid(row=1)
		
		lblMax = tk.Label(frame, font=('Arial', 18), fg='white', bg='black', text='{0}{1}'.format(round(day.maxTemp), degreeSymbol))
		lblMax.grid(row=2)
		
		lblMin = tk.Label(frame, font=('Arial', 18), fg='white', bg='black', text='{0}{1}'.format(round(day.minTemp), degreeSymbol))
		lblMin.grid(row=3)
		
		return frame
		
	def update_forecast(self, forecast):
		#Destroy each frame and then clear the list
		for frame in self.frameList:
			frame.destroy()
			
		self.frameList.clear()
		self.imageList.clear()
		
		#Create a frame for each day and add it to the list
		columnCount = 0
		
		for day in forecast:
			dayFrame = self.create_day_frame(day)
			self.frameList.append(dayFrame)
			dayFrame.grid(row=0, column=columnCount, padx=5)
			
			columnCount = columnCount + 1
