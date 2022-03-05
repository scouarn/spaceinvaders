import tkinter as tk

from gameObject import GameObject
from bullet import Bullet

class Alien(GameObject) :
	
	image = None


	def __init__(self, canvas) :

		# load resources
		if Alien.image is None :
			Alien.image = tk.PhotoImage(file="assets/alien1.png")
			

		super().__init__(canvas, c="red", image=Alien.image)


		self.bullets = []
