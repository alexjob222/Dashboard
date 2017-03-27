import datetime
import tkinter as tk

class Clock(tk.Frame):
	def __init__(self, parent):
		tk.Frame.__init__(self, parent, bg='black')		
		self.varTime = tk.StringVar()
		self.varTime.set('')
		
		self.varDate = tk.StringVar()
		self.varDate.set('')
		
		self.varAmPm = tk.StringVar()
		self.varAmPm.set('')
		
		self.lblTime = tk.Label(self, font=('Arial', 48), fg='white', bg='black', textvariable=self.varTime)
		self.lblTime.grid(row=0, sticky='sw')
		
		self.lblDate = tk.Label(self, font=('Arial', 18), fg='white', bg='black', textvariable=self.varDate)
		self.lblDate.grid(row=1, columnspan=2, sticky='w')
		
		self.lblAmPm = tk.Label(self, font=('Arial', 18), fg='white', bg='black', textvariable=self.varAmPm)
		self.lblAmPm.grid(row=0, column=1)
		
		self.tick()
		
	def tick(self):
		currentTime = datetime.datetime.now()
		timeText = currentTime.strftime('%I:%M')
		
		#Remove leading 0 from the time
		if timeText.startswith('0'):
			timeText = timeText[1:]
		
		self.varTime.set(timeText)
		self.varAmPm.set(currentTime.strftime('%p'))
		
		#Remove the leading 0 from the day of the month
		dayOfMonth = currentTime.strftime('%d')
		if dayOfMonth.startswith('0'):
			dayOfMonth = dayOfMonth[1:]
		
		self.varDate.set(currentTime.strftime('%a, %B ') + dayOfMonth)
		
		self.after(200, self.tick)
		
