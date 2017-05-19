import tkinter as tk

class BottomLineFrame(tk.Frame):
	def __init__(self, parent, itemsList):
		tk.Frame.__init__(self, parent, bg='white')
		
		self.cHeight = 50
		self.canvas = tk.Canvas(self, height=cHeight, bg='black')
		self.canvas.pack(fill='x', expand=True, pady=2, padx=2)
		
		#Items that will be drawn on the canvas
		self.divider = None
		self.header = None #Set header coords to (5, 12) when height is 50
		self.text = None
