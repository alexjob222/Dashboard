from __future__ import print_function
import httplib2
import os
import datetime

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
	

class GoogleCalendar(object):
	def __init__(self):
		self.SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
		self.CLIENT_SECRET_FILE = "calendar_client_id.json"
		self.APPLICATION_NAME = 'MyDashboard'

	def _get_calendar_credentials(self):
		file_dir = os.path.dirname(__file__)
		credential_dir = os.path.join(file_dir, '.credentials')
		if not os.path.exists(credential_dir):
			os.makedirs(credential_dir)
		
		credential_path = os.path.join(credential_dir, 'calendar-info.json')
		
		store = Storage(credential_path)
		credentials = store.get()
		
		if not credentials or credentials.invalid:
			flags = tools.argparser.parse_args(args=[])
		
			flow = client.flow_from_clientsecrets(self.CLIENT_SECRET_FILE, self.SCOPES)
			flow.user_agent = self.APPLICATION_NAME
			credentials = tools.run_flow(flow, store, flags)
			
			print('Storing credentials to ' + credential_path)
			
		return credentials

	def _parse_from_ISO(self, dateString):
		parsedDate = datetime.datetime.strptime(dateString[:-6], '%Y-%m-%dT%H:%M:%S')
		
		return parsedDate
	
	def get_calendar_events(self, maxEvents):
		eventList = list()

		try:
			credentials = self._get_calendar_credentials()
			http = credentials.authorize(httplib2.Http())
			service = discovery.build('calendar', 'v3', http=http)
			
			now = datetime.datetime.utcnow().isoformat() + 'Z'
			
			#Get upcoming events
			eventsResult = service.events().list(
				calendarId = 'primary', timeMin = now, maxResults = maxEvents,
				singleEvents = True, orderBy = 'startTime').execute()
			events = eventsResult.get('items', [])
			
			#Put the events into a list
			for event in events:
				start = event['start'].get('dateTime', event['start'].get('date'))
				end = event['end'].get('dateTime', event['end'].get('date'))
				
				calEvent = CalendarEvent(self._parse_from_ISO(start), self._parse_from_ISO(end), event['summary'])
				eventList.append(calEvent)
		except Exception as e:
			print(datetime.datetime.now().strftime('%c') + ' - calendar - ' + str(e))
		
		return eventList

		
		
class CalendarEvent(object):
	def __init__(self, startTime, endTime, summary):
		self.startTime = startTime
		self.endTime = endTime
		self.summary = summary
		

