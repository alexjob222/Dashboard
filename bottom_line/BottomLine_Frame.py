import tkinter as tk
from bottom_line.BottomLine import *

class BottomLineFrame(tk.Frame):
	def __init__(self, parent, bottomLineItems):
		tk.Frame.__init__(self, parent, bg='white')
		
		self.cHeight = 60
		self.dividerWidth = 5
		self.dividerPadLeft = 10
		self.rectHeight = self.cHeight + 5
		self.textY = 18
		self.scrollSpeed = 8
		self.scrollFreq = 65
		
		self.canvas = tk.Canvas(self, height=self.cHeight, bg='black')
		self.canvas.pack(fill='x', expand=True, pady=2, padx=2)
		
		self.bottomLine = BottomLine(bottomLineItems)
		
		#Items that will be drawn on the canvas
		#Draw header last so it will be the top most element
		self.text = self.canvas.create_text(0, self.textY, fill='white', anchor='nw', font='Arial 18 bold', text='')
		self.headerBackground = self.canvas.create_rectangle(0, 0, 10, self.rectHeight, fill='black')
		self.divider = self.canvas.create_rectangle(0, 0, self.dividerWidth, self.rectHeight, fill='white')
		self.header = self.canvas.create_text(5, self.textY, fill='white', anchor='nw', font='Arial 18 bold', text='')
		
		self.display_next_item()
		
	def display_next_item(self):
		nextItem = self.bottomLine.get_next_item()
		
		self.canvas.itemconfig(self.header, text=nextItem.header)
		self.canvas.itemconfig(self.text, text=nextItem.details)
		
		#Put divider to the right of the header, and the text to the right of the divider
		dividerStart = self._get_item_right_side(self.header) + self.dividerPadLeft
		self.canvas.coords(self.divider, dividerStart, 0, (dividerStart + self.dividerWidth), self.rectHeight)
		
		dividerEnd = self._get_item_right_side(self.divider)
		self.canvas.coords(self.text, (dividerEnd + 10), self.textY)
		
		#Resize the header background
		self.canvas.coords(self.headerBackground, 0, 0, dividerEnd, self.rectHeight)
		
		self.after(2.5 * 1000, self.scroll_text)
	
	def scroll_text(self):
		self.canvas.move(self.text, -(self.scrollSpeed), 0)
		
		#If the right side of the text is no longer showing, get the next item to display
		dividerEnd = self._get_item_right_side(self.divider)
		textEnd = self._get_item_right_side(self.text)
		
		if textEnd < dividerEnd:
			self.display_next_item()
		else:
			self.after(self.scrollFreq, self.scroll_text)
		
	def _get_item_right_side(self, item):
		bounds = self.canvas.bbox(item) #Returns a tuple like (x1, y1, x2, y2)
		
		return bounds[2]
		