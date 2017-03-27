import requests
import json
from collections import namedtuple
import datetime
import pytz
import config


class SportsFeed(object):
	def __init__(self, league):
		self.BASE_URL = 'https://www.mysportsfeeds.com/api/feed/pull/'
		self.league = league
		self.lastGameUpdate = None
		self.todaysGames = None

	def get_daily_games(self, date):
		url = '{0}{1}/current/daily_game_schedule.json?fordate={2}'.format(
				self.BASE_URL, self.league, date.strftime('%Y%m%d'))	
		
		#Put the games into a list
		gameList = list()
		
		try:
			#Send request for json
			response = requests.get(url, auth=(config.sports['username'], config.sports['password']))

			games = json.loads(response.text, object_hook = lambda d: namedtuple('DailyGames', d.keys())(*d.values()))
		
			
			for game in games.dailygameschedule.gameentry:
				gameStartTime = self._subtract_hour(game.time)
				
				gameObj = SportsGame(game.awayTeam.Abbreviation, 
							game.homeTeam.Abbreviation, gameStartTime, self.league)	
				gameList.append(gameObj)
		except:
			pass
		
		self.lastGameUpdate = datetime.datetime.now()
		self.todaysGames = gameList
		
		#Return the list of games
		return gameList
		
	def get_season_start_and_end_year(self, date, regOrPost):
		'''This method may not be needed anymore. This was used to get the years needed for
		 the API call. The API now allows the current season to be requested'''
		#Determine start and end year based on when the league season starts
		if self.league == 'NFL':
			if date.month > 3:
				return '{0}-{1}'.format(date.year, date.year + 1)
			else:
				if regOrPost == 'regular':
					return '{0}-{1}'.format(date.year - 1, date.year)
				else:
					#During playoffs, the begin and end year are the same (current year)
					return '{0}-{1}'.format(date.year, date.year) 
		elif self.league == 'NBA':
			if date.month > 7:
				return '{0}-{1}'.format(date.year, date.year + 1)
			else:
				if regOrPost == 'regular':
					return '{0}-{1}'.format(date.year - 1, date.year)
				else:
					return '{0}-{1}'.format(date.year, date.year)
		elif self.league == 'NHL':
			if date.month > 7:
				return '{0}-{1}'.format(date.year, date.year + 1)
			else:
				if regOrPost == 'regular':
					return '{0}-{1}'.format(date.year - 1, date.year)
				else:
					return '{0}-{1}'.format(date.year, date.year)
		elif self.league == 'MLB':
			return '{0}-{1}'.format(date.year, date.year)
		else:
			return ''

	def _localize_time(self, time):
		'''Game times received from API are in Eastern Time. This converts
		the time to the timezone specified in the config file'''
		timeObj = datetime.datetime.strptime(time, '%I:%M%p').time()
		dtObj = datetime.datetime.combine(datetime.date.today(), timeObj)
		
		easternTimeZone = pytz.timezone('US/Eastern')
		localTimeZone = pytz.timezone(config.timezone)
		
		#Convert the time to the local time zone
		localTime = easternTimeZone.localize(dtObj).astimezone(localTimeZone)
		
		timeString = localTime.strftime('%I:%M %p')
		#Remove leading zeros from the time string
		if timeString.startswith('0'):
			timeString = timeString[1:]
		
		return timeString
	

class SportsGame(object):
	def __init__(self, awayTeam, homeTeam, startTime, league):
		#Change some of the abbreviations
		self.awayTeam = self.get_team_abbr(awayTeam, league)
		self.awayImgPath = 'images/' + league + '/' + self.awayTeam + '.png'
		
		self.homeTeam = self.get_team_abbr(homeTeam, league)		
		self.homeImgPath = 'images/' + league + '/' + self.homeTeam + '.png'
		
		self.startTime = startTime
		self.league = league
		
	def get_team_abbr(self, team, league):
		if league == 'NBA':
			if team == 'BRO':
				return 'BKN'
			elif team == 'OKL':
				return 'OKC'
			else:
				return team
		elif league == 'NHL':
			if team == 'FLO':
				return 'FLA'
			elif team == 'WPJ':
				return 'WPG'
			else:
				return team
		else:
			return team
