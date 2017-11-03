import tkinter as tk
import datetime
from google_calendar.GoogleCalendar import *
import config

class CalendarFrame(tk.Frame):
	def __init__(self, parent):
		tk.Frame.__init__(self, parent, bg='black')
		self.calendarObj = GoogleCalendar()
		self.updateFreq = 1000 * 60 * config.calendar['updateFrequency']
		self.maxResults = config.calendar['maxResults']
		self.calFrame = tk.Frame(self)
		self.update_calendar_frame()
		
	def _format_date(self, date):
		if date.date() == datetime.date.today():
			return 'Today'
		else:
			dayOfMonth = self._remove_leading_zero(date.strftime('%d'))
			
			return date.strftime('%b ') + dayOfMonth
		
	def _format_time(self, startTime, endTime):
		start = self._remove_leading_zero(startTime.strftime('%I:%M%p'))
		end = self._remove_leading_zero(endTime.strftime('%I:%M%p'))
		
		#return '{0} - {1}'.format(start, end)
		return start
			
	def _remove_leading_zero(self, string):
		if string.startswith('0'):
			string = string[1:]
			
		return string
	
	def update_calendar_frame(self):
		calendarEvents = self.calendarObj.get_calendar_events(self.maxResults)
		
		self.calFrame.destroy()
		self.calFrame = tk.Frame(self, bg='black')
		self.calFrame.pack(fill='both', expand=True)
		
		#Print events to the frame
		rowCount = 0
		oneMonthFromNow = datetime.date.today() + datetime.timedelta(days=30)
		eventDate = None
		
		for event in calendarEvents:
			#Only add things that are less than 30 days away
			if event.startTime.date() <= oneMonthFromNow:
				#Add the day of the event above the event description
				if event.startTime.date() != eventDate:
					eventDate = event.startTime.date()
				
					lblDate = tk.Label(self.calFrame, fg='white', bg='black', 
								font=('Arial', 18), text=self._format_date(event.startTime))
					lblDate.grid(row=rowCount, sticky='w')			
					
					rowCount = rowCount + 1
				
				
				lblEvent = tk.Label(self.calFrame, fg='white', bg='black', font=('Arial', 18),
							text='   {0} - {1}'.format(self._format_time(event.startTime, event.endTime), event.summary))
					  
				lblEvent.grid(row=rowCount, sticky='w')
				rowCount = rowCount + 1
		
		#Update the frame after the specified time
		self.after(self.updateFreq, self.update_calendar_frame)
