import tkinter as tk
from bottom_line.BottomLine import *

class BottomLineFrame(tk.Frame):
	def __init__(self, parent, bottomLineItems):
		tk.Frame.__init__(self, parent, bg='white')
		
		self.cHeight = 60
		self.dividerWidth = 5
		self.dividerPadLeft = 10
		
		self.canvas = tk.Canvas(self, height=self.cHeight, bg='black')
		self.canvas.pack(fill='x', expand=True, pady=2, padx=2)
		
		self.bottomLine = BottomLine(bottomLineItems)
		
		#Items that will be drawn on the canvas
		self.header = self.canvas.create_text(5, 15, fill='white', anchor='nw', font='Arial 18 bold', text='') #Set header coords to (5, 12) when height is 50
		self.divider = self.canvas.create_rectangle(0, 0, self.dividerWidth, (self.cHeight + 1), fill='white')
		self.text = self.canvas.create_text(0, 0, fill='white', anchor='w', font='Arial 18', text='')
