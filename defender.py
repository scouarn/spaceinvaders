import tkinter as tk

from gameObject import GameObject
from bullet import Bullet

class Defender(GameObject) :
	
	image = None

	def __init__(self, canvas) :

		# load resources
		if Defender.image is None :
			Defender.image = tk.PhotoImage(file="assets/def1.png")

		super().__init__(canvas, c="red", image=Defender.image)


		self.bullets = []


	def fire(self) :
		pass
