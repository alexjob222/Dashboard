import requests
import json
from collections import namedtuple
import datetime
import pytz
import config


def get_team_abbr(team, league):
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

class SportsFeed(object):
	def __init__(self, league):
		self.BASE_URL = 'https://www.mysportsfeeds.com/api/feed/pull/'
		self.league = league
		self.lastGameUpdate = None
		self.todaysGames = None
		self.conferenceStandings = None

	def get_daily_games(self, date):
		url = '{0}{1}/current/daily_game_schedule.json?fordate={2}'.format(
				self.BASE_URL, self.league, date.strftime('%Y%m%d'))	
		
		#Put the games into a list
		gameList = list()
		
		try:
			#Send request for json
			response = requests.get(url, auth=(config.sports['username'], config.sports['password']))
			
			if response.text:
				games = json.loads(response.text, 
							object_hook = lambda d: namedtuple('DailyGames', d.keys())(*d.values()))
			
				#Create an object for each game
				for game in games.dailygameschedule.gameentry:
					gameStartTime = self._localize_time(game.time)
					
					gameObj = SportsGame(game.awayTeam.Abbreviation, 
								game.homeTeam.Abbreviation, gameStartTime, self.league)	
					gameList.append(gameObj)
					
		except Exception as e:
			print(datetime.datetime.now().strftime('%c') + ' - daily games - ' + str(e))
		
		self.lastGameUpdate = datetime.datetime.now()
		self.todaysGames = gameList
		
		#Return the list of games
		return gameList
		
	
	def get_conference_standings(self):
		#The list of team stats desired in the response
		stats = 'W,L,'
		if self.league == 'NHL':
			stats += 'Pts,OTL'
		elif self.league == 'NFL':
			stats += 'T'
		else:
			stats += 'GB'
			
		url = '{0}{1}/current/conference_team_standings.json?teamstats={2}'.format(
				self.BASE_URL, self.league, stats)
		
		conferenceList = list()
		
		try:
			response = requests.get(url, auth=(config.sports['username'], config.sports['password']))
			
			if response.text:
				#Parse the json into objects
				data = json.loads(response.text)
				for conf in data['conferenceteamstandings']['conference']:
					confName = conf['@name']
					
					teamList = list()
					
					for team in conf['teamentry']:
						teamAbbr = team['team']['Abbreviation']
						rank = team['rank']
						wins = team['stats']['Wins']['#text']
						losses = team['stats']['Losses']['#text']
						extraStats = {}
						
						if self.league == 'NHL':
							extraStats['OTL'] = team['stats']['OvertimeLosses']['#text']
							extraStats['PTS'] = team['stats']['Points']['#text']
						elif self.league == 'NFL':
							extraStats['Ties'] = team['stats']['Ties']['#text']
						else:
							extraStats['GB'] = team['stats']['GB']['#text']
							
						teamInfo = TeamStandingInfo(self.league, teamAbbr, rank, wins, losses, extraStats)
						teamList.append(teamInfo)
						
					conference = Conference(confName, teamList)
					conferenceList.append(conference)
											
		except Exception as e:
			print(datetime.datetime.now().strftime('%c') + ' - standings - ' + str(e))
			
		self.conferenceStandings = conferenceList
		return conferenceList
		

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
		self.awayTeam = get_team_abbr(awayTeam, league)
		self.awayImgPath = 'images/' + league + '/' + self.awayTeam + '.png'
		
		self.homeTeam = get_team_abbr(homeTeam, league)		
		self.homeImgPath = 'images/' + league + '/' + self.homeTeam + '.png'
		
		self.startTime = startTime
		self.league = league
		
		
class TeamStandingInfo(object):
	def __init__(self, league, teamAbbr, rank, wins, losses, extraStats):
		self.teamAbbr = get_team_abbr(teamAbbr, league)
		self.teamImgPath = 'images/' + league + '/' + self.team + '.png'
		self.rank = rank
		self.wins = wins
		self.losses = losses
		self.extraStats = extraStats
		

class Conference(object):
	def __init__(self, name, teams):
		self.name = name
		self.teams = teams
		
	
