#!/usr/bin/python3

import tkinter as tk
import config

from Clock_Frame import *
from weather import Weather_Frame
from google_calendar import Calendar_Frame
from sports import Sports_Frame, SportsFeed
from bottom_line import BottomLine_Frame


class AppFrames(object):
	def __init__(self):
		self.mainWindow = tk.Tk()
		self.mainWindow.bind('<Left>', self.frame_left)
		self.mainWindow.bind('<Right>', self.frame_right)
		self.mainWindow.bind('<Escape>', self.exit_fullscreen)
		self.mainWindow.bind('<Enter>', self.enter_fullscreen)
		
		self.nbaFeed = SportsFeed.SportsFeed('NBA')
		self.nhlFeed = SportsFeed.SportsFeed('NHL')
		self.nflFeed = SportsFeed.SportsFeed('NFL')
		self.mlbFeed = SportsFeed.SportsFeed('MLB')
		
		self.currentFrameIndex = 0
		self.appFrames = list()

		#Create the frame with the main information
		self.mainFrame = self.create_main_frame()
		
		self.mainFrame.rowconfigure(0, weight=1)
		self.mainFrame.rowconfigure(1, weight=1)
		self.mainFrame.columnconfigure(0, weight=1)

		self.appFrames.append(self.mainFrame)

		#Create the sports frames		
		self.nbaFrame = Sports_Frame.LeagueFrame(self.mainWindow, self.nbaFeed)
		self.appFrames.append(self.nbaFrame)
				
		self.nhlFrame = Sports_Frame.LeagueFrame(self.mainWindow, self.nhlFeed)
		self.appFrames.append(self.nhlFrame)
				
		self.nflFrame = Sports_Frame.LeagueFrame(self.mainWindow, self.nflFeed)
		self.appFrames.append(self.nflFrame)
				
		self.mlbFrame = Sports_Frame.LeagueFrame(self.mainWindow, self.mlbFeed)
		self.appFrames.append(self.mlbFrame)
		
		#Add the frames to the window
		for frame in self.appFrames:
			frame.grid(row=0, column=0, sticky='nsew')
		
		#Set the frames to expand to window width
		self.mainWindow.rowconfigure(0, weight=1)
		self.mainWindow.columnconfigure(0, weight=1)
		
		self.appFrames[0].tkraise()
		
		self.mainWindow.attributes("-fullscreen", True)
		self.mainWindow.mainloop()
		
	def create_main_frame(self):
		mainFrame = tk.Frame(self.mainWindow, bg='black')
		
		#Items for the left side of the screen
		leftFrame = tk.Frame(mainFrame, bg='black')
		
		clock = Clock(leftFrame)
		clock.pack(pady=15, anchor='w')
		
		calendar = Calendar_Frame.CalendarFrame(leftFrame)
		calendar.pack(pady=50)
		
		leftFrame.grid(row=0, column=0, padx=15, sticky='nw')
		
		#Items for the right side of the screen
		rightFrame = tk.Frame(mainFrame, bg='black')
		
		weather = Weather_Frame.WeatherFrame(rightFrame)
		weather.pack(anchor='ne')
		
		favoriteTeams = Sports_Frame.FavoriteTeamsFrame(rightFrame, self.mlbFeed, self.nflFeed, self.nbaFeed, self.nhlFeed)
		favoriteTeams.pack(pady=35, anchor='e')
		
		rightFrame.grid(row=0, column=1, padx=15, sticky='ne')
		
		bottomLineProviders = [self.nbaFeed, self.nhlFeed, self.nflFeed, self.mlbFeed]
		bottomLineFrame = BottomLine_Frame.BottomLineFrame(mainFrame, bottomLineProviders)
		
		bottomLineFrame.grid(row=1, columnspan=2, sticky='wse')
		
		return mainFrame
		

	def frame_right(self, event):
		self.currentFrameIndex = (self.currentFrameIndex + 1) % len(self.appFrames)
		self.appFrames[self.currentFrameIndex].tkraise()
		
	def frame_left(self, event):
		self.currentFrameIndex = (self.currentFrameIndex - 1) % len(self.appFrames)
		self.appFrames[self.currentFrameIndex].tkraise()
		
	def exit_fullscreen(self, event):
		self.mainWindow.attributes("-fullscreen", False)
		
	def enter_fullscreen(self, event):
		self.mainWindow.attributes("-fullscreen", True)
		
if __name__ == '__main__':
	app = AppFrames()
