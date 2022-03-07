import tkinter as tk

from gameObject import GameObject

class Alien(GameObject) :

	images = None

	def __init__(self, canvas, x=0, y=0, type=0) :
		self.type = type # integer : not the built in type function

		if Alien.images is None :
			Alien.images = [
				tk.PhotoImage(file="assets/alien1.png"),
				tk.PhotoImage(file="assets/alien2.png"),
				tk.PhotoImage(file="assets/alien3.png"),
				tk.PhotoImage(file="assets/alien4.png"),
			]


		super().__init__(canvas, x=x, y=y, image=Alien.images[self.type % len(Alien.images)])
