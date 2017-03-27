from PIL import Image, ImageTk

def size_image(width, height, imgPath):
	
	img = Image.open(imgPath)
	resizedImg = img.resize((width, height), Image.ANTIALIAS)
	
	tkImg = ImageTk.PhotoImage(resizedImg)
	return tkImg
