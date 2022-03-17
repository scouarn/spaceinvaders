import tkinter as tk
import audio



class Canvas(tk.Tk) :

	def __init__(self, width, height, title) :

		super().__init__()

		self.title(title)
		self.width = width
		self.height = height
			
		self.tkframe = tk.Frame(self)
		self.tkframe.place(relx=0.5, rely=0.5, anchor="center")

		self.tkcanvas = tk.Canvas(
			self.tkframe, 
			width=self.width,
			height=self.height,
			background="black",
			highlightthickness=0,
		)

		self.tkcanvas.pack()


		# transmit messages directly to tkcanvas
		self.create_image = self.tkcanvas.create_image
		self.create_rectangle = self.tkcanvas.create_rectangle
		self.create_line = self.tkcanvas.create_line
		self.create_text = self.tkcanvas.create_text
		self.itemconfig = self.tkcanvas.itemconfig
		self.coords = self.tkcanvas.coords
		self.moveto = self.tkcanvas.moveto
		self.delete = self.tkcanvas.delete
		self.lower = self.tkcanvas.lower
		self.after = self.tkcanvas.after


	def destroy(self) :
		self.stop_all()
		super().destroy()


	def get_width(self) :
		return self.width

	def get_height(self) :
		return self.height

	def play_wav(self, fname) :
		audio.play_wav(fname)
	
	def stop_all(self) :
		audio.stop_all()