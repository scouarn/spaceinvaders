import tkinter as tk
import random

from audio import play_wav
from gameObject import GameObject

class Bullet(GameObject) :
	
	image = None

	sounds = [
		"assets/laser1.wav",
		"assets/laser2.wav",
		"assets/laser3.wav",
	]

	def __init__(self, canvas, x, y, vy, dosfx=True) :

		if Bullet.image is None :
			Bullet.image = tk.PhotoImage(file="assets/bullet1.png")

		super().__init__(canvas, x=x, y=y, image=Bullet.image)

		self.vy = vy

		if dosfx :
			play_wav(random.choice(Bullet.sounds))
