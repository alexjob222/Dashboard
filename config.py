timezone = 'US/Central'

#Weather settings - API used: http://openweathermap.org
weather = {
	'cityID': '<City ID>',
	'unitFormat': 'imperial',
	'language': 'en',
	'apiKey': '<API Key>',
	'forecastCount': 5
}

#Calendar settings
calendar = {
	'maxResults': 10,
	'updateFrequency': 30 #In minutes
}

#Sports settings - API used: https://www.mysportsfeeds.com/
sports = {
	'username': '<username>',
	'password': '<password>', #definitely not the best way to store a password, but I'm lazy....
	
	#These have not been incorporated into the project yet...
	'showNFL': True,
	'showNBA': True,
	'showNHL': True,
	'showMLB': True
}

favoriteTeams = {
	#Add the team abbreviations to its respective league
	#Leave empty if no favorites for that league
	'NFL': ['<Team Abbr>'],
	
	'NBA': ['<Team Abbr>'],
	
	'NHL': ['<Team Abbr>'],
	
	'MLB': ['<Team Abbr>']	
}
