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
		imageSize = 45
		
		self.imgAwayTeam = size_image(imageSize, imageSize, os.path.join(pathname, game.awayImgPath))
		self.lblAwayImage = tk.Label(self, bg='black', image=self.imgAwayTeam)
		self.lblAwayText = tk.Label(self, font=('Arial', 18), fg='white', bg='black', text=game.awayTeam)
		
		self.imgHomeTeam = size_image(imageSize, imageSize, os.path.join(pathname, game.homeImgPath))
		self.lblHomeImage = tk.Label(self, bg='black', image=self.imgHomeTeam)
		self.lblHomeText = tk.Label(self, font=('Arial', 18), fg='white', bg='black', text=game.homeTeam)
		
		self.lblTime = tk.Label(self, font=('Arial', 18), fg='white', bg='black', text=game.startTime)
		
		self.height = imageSize * 2 #Image is bigger than the text
		
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
		
		games = leagueObj.todaysGames
		games.sort(key=lambda g: g.startTime, reverse=False)
		
		rowCount = 0
		columnCount = 0
		screenHeight = self.winfo_screenheight()
		heightUsed = 0
		
		paddingY = 5
		
		for game in games:
			gameFrame = GameFrame(self, game)
			self.frameList.append(gameFrame)
			
			#Determine how much screen space the widget will use			
			widgetHeight = gameFrame.height + (paddingY * 2) #Include vertical padding 
			
			if (heightUsed + widgetHeight) > screenHeight:
				heightUsed = widgetHeight
				rowCount = 0
				columnCount += 1
			else:
				heightUsed += widgetHeight
			
			gameFrame.grid(row=rowCount, column=columnCount, padx=10, pady=paddingY)
			
			rowCount += 1
	
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
		
		self.imgLogo = size_image(100, 100, os.path.join(pathname, 'images/' + leagueObj.league + '/logo.png'))
		self.lblLeague = tk.Label(self, font=('Arial', 48), fg='white', bg='black', text=' ' + leagueObj.league, image=self.imgLogo, compound=tk.LEFT)
		self.lblLeague.grid(row=0, column=0, sticky='n', pady=10)
		
		self.todaysGames = TodaysGamesFrame(self)
		self.todaysGames.grid(row=0, rowspan=2, column=1, sticky='ne')
		
		self.conferenceStandings = LeagueStandingsFrame(self)
		self.conferenceStandings.grid(row=1, column=0, sticky='n')
		
		#Set the column to take up all available space
		self.columnconfigure(0, weight=1)
		
		self.update_frame()
	
	def update_frame(self):
		self.todaysGames.update_frame(self.leagueObj)
		
		self.conferenceStandings.update_frame(self.leagueObj)
		
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
				
			#Update games every 3 hours
			elif (self.leagueObjects[league].lastGameUpdate + datetime.timedelta(hours = 3)) < datetime.datetime.now():
				self.leagueObjects[league].get_daily_games(datetime.date.today())
				
		#Update the game frames
		self.add_games_to_frame()
		
		self.after(self.updateFreq, self.update_frame)
		
		
class ConferenceFrame(tk.Frame):
	def __init__(self, parent, conference):
		tk.Frame.__init__(self, parent, bg='black')
		
		lblConferenceName = tk.Label(self, text=conference.name, bg='black', fg='white', font=('Arial', 18, 'bold'))
		lblConferenceName.grid(row=0, columnspan=5, pady=10)
		 
		pathname = os.path.dirname(__file__)
		rowCount = 1
		
		for team in conference.teams:
			lblRank = tk.Label(self, text=team.rank, bg='black', fg='white', font=('Arial', 16))
			lblRank.grid(row=rowCount, column=0, padx=2)
			
			team.teamImg = size_image(45, 45, os.path.join(pathname, team.teamImgPath))
			lblImage = tk.Label(self, bg='black', image=team.teamImg)
			lblImage.grid(row=rowCount, column=1, padx=2)
			
			lblTeam = tk.Label(self, text=team.teamAbbr, bg='black', fg='white', font=('Arial', 16))
			lblTeam.grid(row=rowCount, column=2, padx=2)
			
			lblRecord = tk.Label(self, text=self._get_record_string(team), bg='black', fg='white', font=('Arial', 16))
			lblRecord.grid(row=rowCount, column=3, padx=2)
			
			lblExtraInfo = tk.Label(self, bg='black', fg='white', font=('Arial', 16))
			if 'GB' in team.extraStats:
				lblExtraInfo.config(text=team.extraStats['GB'])
			else:
				lblExtraInfo.config(text=team.extraStats['PTS']) #NHL only one without GB
			lblExtraInfo.grid(row=rowCount, column=4, padx=2)
			
			rowCount = rowCount + 1
		
		
	def _get_record_string(self, teamInfo):
		recordString = teamInfo.wins + '-' + teamInfo.losses
		
		#Add ties and overtime losses if available (NFL and NHL)
		if 'T' in teamInfo.extraStats:
			ties = teamInfo.extraStats['T']
			if int(ties) > 0:
				recordString = recordString + '-' + ties
		elif 'OTL' in teamInfo.extraStats:
			recordString = recordString + '-' + teamInfo.extraStats['OTL']
		
		return recordString
		
		
class LeagueStandingsFrame(tk.Frame):
	def __init__(self, parent):
		tk.Frame.__init__(self, parent, bg='black')
		
		self.lastStandingsUpdate = None
		self.frameList = list()
		
	def update_standings(self, standings):
		#Destroy frames and clear lists
		for frame in self.frameList:
			frame.destroy()
			
		self.frameList.clear()
		
		columnCount = 0
		
		#Create frame for each conference
		for conference in standings:
			frame = ConferenceFrame(self, conference)
			self.frameList.append(frame)
			frame.grid(row=0, column=columnCount, sticky='n', padx=10)
			
			columnCount = columnCount + 1
	
	def update_frame(self, leagueObj):
		#Update if not yet set
		if self.lastStandingsUpdate == None:
			standings = leagueObj.get_conference_standings()			
			self.lastStandingsUpdate = datetime.datetime.now()
			
			self.update_standings(standings)
			
		#Update every 6 hours
		elif (self.lastStandingsUpdate + datetime.timedelta(hours = 6)) < datetime.datetime.now():
			standings = leagueObj.get_conference_standings()			
			self.lastStandingsUpdate = datetime.datetime.now()
			
			self.update_standings(standings)
		
