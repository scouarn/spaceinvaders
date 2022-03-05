import tkinter as tk

from gameObject import GameObject
from bullet import Bullet

class Alien(GameObject) :
	
	alien1_image = None

	def __init__(self, canvas) :

		# load resources
		if Alien.alien1_image is None :
			Alien.alien1_image = tk.PhotoImage(file="assets/alien1.png")

		super().__init__(canvas, c="red", image=Alien.alien1_image)


		self.bullets = []
