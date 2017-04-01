import tkinter as tk
from PIL import Image, ImageTk
import datetime
from sports.SportsFeed import *
import os
from UtilMethods import size_image
import config

	
class GameFrame(tk.Frame):
	def __init__(self, parent, game):
		tk.Frame.__init__(self, parent, bg='black')
		
		pathname = os.path.dirname(__file__)
		
		self.imgAwayTeam = size_image(45, 45, os.path.join(pathname, game.awayImgPath))
		self.lblAwayImage = tk.Label(self, bg='black', image=self.imgAwayTeam)
		self.lblAwayText = tk.Label(self, font=('Arial', 18), fg='white', bg='black', text=game.awayTeam)
		
		self.imgHomeTeam = size_image(45, 45, os.path.join(pathname, game.homeImgPath))
		self.lblHomeImage = tk.Label(self, bg='black', image=self.imgHomeTeam)
		self.lblHomeText = tk.Label(self, font=('Arial', 18), fg='white', bg='black', text=game.homeTeam)
		
		self.lblTime = tk.Label(self, font=('Arial', 18), fg='white', bg='black', text=game.startTime)
		
		#Arrange into a grid
		self.lblAwayImage.grid(row=0, column=0)
		self.lblAwayText.grid(row=0, column=1)
		
		self.lblHomeImage.grid(row=1, column=0)
		self.lblHomeText.grid(row=1, column=1)
		
		self.lblTime.grid(row=0, column=2, rowspan=2, padx=15)
		
		
class TodaysGamesFrame(tk.Frame):
	def __init__(self, parent):
		tk.Frame.__init__(self, parent, bg='black')

		self.frameList = list()
		
		self.today = datetime.date.today()
		
	def update_todays_games(self, leagueObj):
		#Destroy frames and clear lists
		for frame in self.frameList:
			frame.destroy()
			
		self.frameList.clear()
		
		#Get games and create their frames
		games = leagueObj.todaysGames
		games.sort(key=lambda g: g.startTime, reverse=False)
		
		rowCount = 0
		columnCount = 0
		
		for game in games:
			gameFrame = GameFrame(self, game)
			self.frameList.append(gameFrame)
			gameFrame.grid(row=rowCount, column=columnCount, padx=10, pady=10)
			
			columnCount = (columnCount + 1) % 4
			if columnCount == 0:
				rowCount = rowCount + 1
	
	def update_frame(self, leagueObj):
		#Update if not yet set
		if leagueObj.lastGameUpdate == None or leagueObj.todaysGames == None:
			leagueObj.get_daily_games(self.today)
		
		#Update if the day has changed
		elif self.today != datetime.date.today():
			self.today = datetime.date.today()
			leagueObj.get_daily_games(self.today)
			
		#Update every 3 hours
		elif (leagueObj.lastGameUpdate + datetime.timedelta(hours = 3)) < datetime.datetime.now():
			leagueObj.get_daily_games(self.today)
			
		self.update_todays_games(leagueObj)
		
class LeagueFrame(tk.Frame):
	def __init__(self, parent, leagueObj):
		tk.Frame.__init__(self, parent, bg='black')
		self.leagueObj = leagueObj
		self.updateFreq = 1000 * 60 * 30 #30 minutes
		
		pathname = os.path.dirname(__file__)
		
		self.imgLogo = size_image(150, 150, os.path.join(pathname, 'images/' + leagueObj.league + '/logo.png'))
		self.lblLeague = tk.Label(self, font=('Arial', 48), fg='white', bg='black', text=' ' + leagueObj.league, image=self.imgLogo, compound=tk.LEFT)
		self.lblLeague.pack(pady=10, anchor='n')
		
		self.todaysGames = TodaysGamesFrame(self)
		self.todaysGames.pack(pady=10)
		
		self.update_frame()
	
	def update_frame(self):
		self.todaysGames.update_frame(self.leagueObj)
		
		self.after(self.updateFreq, self.update_frame)
		
		
class FavoriteTeamsFrame(tk.Frame):
	def __init__(self, parent, mlbObj, nflObj, nbaObj, nhlObj):
		tk.Frame.__init__(self, parent, bg='black')		
		self.updateFreq = 1000 * 60 * 30 #30 minutes
		
		self.leagueObjects = {'MLB': mlbObj, 'NFL': nflObj, 'NBA': nbaObj, 'NHL': nhlObj}
		
		self.gameList = list()
		
		self.update_frame()
		
	def add_games_to_frame(self):		
		#Destroy frames and clear list
		for frame in self.gameList:
			frame.destroy()
			
		self.gameList.clear()
		
		#Add the favorites
		for league in self.leagueObjects:
			favorites = config.favoriteTeams[league]
			
			#Order the games by their start time
			self.leagueObjects[league].todaysGames.sort(key=lambda g: g.startTime, reverse=False)
			
			#Loop through todays games
			for game in self.leagueObjects[league].todaysGames:
				if ((game.awayTeam in favorites) or (game.homeTeam in favorites)):
					gameFrame = GameFrame(self, game)
					
					gameFrame.pack(padx=10, pady=10)
					self.gameList.append(gameFrame)
			
	def update_frame(self):
		for league in self.leagueObjects:
			#Update games if not yet set
			if self.leagueObjects[league].lastGameUpdate == None:
				self.leagueObjects[league].get_daily_games(datetime.date.today())
			
			#Update games if the day has changed
			elif self.leagueObjects[league].lastGameUpdate.date() != datetime.date.today():
				self.leagueObjects[league].get_daily_games(datetime.date.today())
				
			#Update games every 4 hours
			elif (self.leagueObjects[league].lastGameUpdate + datetime.timedelta(hours = 4)) < datetime.datetime.now():
				self.leagueObjects[league].get_daily_games(datetime.date.today())
				
		#Update the game frames
		self.add_games_to_frame()
		
