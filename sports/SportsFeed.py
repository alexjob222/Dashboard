import requests
import json
from collections import namedtuple
import datetime
import pytz
import config


def get_team_abbr(team, league):
	'''I didn't like some of the abbreviations returned from the API,
	so this method returns the abbreviations that I am used to seeing'''
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
			print(datetime.datetime.now().strftime('%c') + ' - daily games - ' + 
					self.league + ' - ' + str(e))
		
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
						
						#The team stats for NHL are nested in another 'stats' object
						#Pretty sure this is a bug with the API, but still need a workaround 
						wins = team['stats']['Wins']['#text'] if self.league != 'NHL' else team['stats']['stats']['Wins']['#text']
						losses = team['stats']['Losses']['#text'] if self.league != 'NHL' else team['stats']['stats']['Losses']['#text']
						extraStats = {}
						
						if self.league == 'NHL':
							extraStats['OTL'] = team['stats']['stats']['OvertimeLosses']['#text']
							extraStats['PTS'] = team['stats']['stats']['Points']['#text']
						elif self.league == 'NFL':
							extraStats['T'] = team['stats']['Ties']['#text']
							extraStats['GB'] = '0.0' #GB not included in the NFL pull
						else:
							extraStats['GB'] = team['stats']['GB']['#text']
							
						teamInfo = TeamStandingInfo(self.league, teamAbbr, rank, wins, losses, extraStats)
						teamList.append(teamInfo)
						
					conference = Conference(confName, teamList)
					conferenceList.append(conference)
											
		except Exception as e:
			print(datetime.datetime.now().strftime('%c') + ' - standings - ' + 
					self.league + ' - ' + str(e))
			
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
		self.teamImgPath = 'images/' + league + '/' + self.teamAbbr + '.png'
		self.rank = rank
		self.wins = wins
		self.losses = losses
		self.extraStats = extraStats
		
		#This variable is needed to store the image generated by the frame that reads from this class
		#If it isn't stored, it gets disposed instantly and doesn't show up on the frame
		self.teamImg = None
		

class Conference(object):
	def __init__(self, name, teams):
		self.name = self._set_conference_name(name)
		self.teams = teams
		
		#The feed returns a 'GB' field, but it isn't actually calculated. Guess I'll do it myself...
		self.set_games_back()
		
	def _set_conference_name(self, name):
		if name == 'Eastern':
			return 'East'
		elif name == 'Western':
			return 'West'
		else:
			return name
			
	def set_games_back(self):
		if not self.teams or 'GB' not in self.teams[0].extraStats:
			return
			
		#Find the team ranked first in the standings
		firstPlaceWins = 0.0
		firstPlaceLosses = 0.0
		
		for team in self.teams:
			if int(team.rank) == 1:
				firstPlaceWins = float(team.wins)
				firstPlaceLosses = float(team.losses)
				
				#Factor in ties - they count as half of a win AND half of a loss
				if 'T' in team.extraStats:
					ties = int(team.extraStats['T'])
					
					firstPlaceWins += (ties * 0.5)
					firstPlaceLosses += (ties * 0.5)
				
				break
		
		#Calculate the games back for each team
		for team in self.teams:
			wins = float(team.wins)
			losses = float(team.losses)
			
			if 'T' in team.extraStats:
				ties = int(team.extraStats['T'])
				wins += (ties * 0.5)
				losses += (ties * 0.5)
				
			gamesBack = (abs(firstPlaceWins - wins) + abs(firstPlaceLosses - losses)) / 2
			
			#Add as a string to keep consistent - API returns all string values
			team.extraStats['GB'] = str(gamesBack)
		
	
