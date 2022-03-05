import tkinter as tk

from gameObject import GameObject
from bullet import Bullet

class Defender(GameObject) :
	
	def_image = None

	def __init__(self, canvas) :

		# load resources
		if Defender.def_image is None :
			Defender.def_image = tk.PhotoImage(file="assets/def1.png")

		super().__init__(canvas, c="red", image=Defender.def_image)


		self.bullets = []


	def fire(self) :
		pass
