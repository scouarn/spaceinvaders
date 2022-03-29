import tkinter as tk
import random

from gameObject import GameObject

class Explosion(GameObject) :
	
	image = None

	sounds = [
		"assets/explosion1.wav",
		"assets/explosion2.wav",
		"assets/explosion3.wav",
		"assets/explosion4.wav",
		"assets/explosion5.wav",
	]

	def __init__(self, canvas, x, y, dosfx=True, timer=1.0) :

		if Explosion.image is None :
			Explosion.image = tk.PhotoImage(file="assets/explo1.png")

		super().__init__(canvas, x=x, y=y, image=Explosion.image)

		self.timer = timer

		if dosfx :
			self.canvas.play_wav(random.choice(Explosion.sounds))


	def update(self, dt) :

		self.timer -= dt

		if self.timer <= 0 :
			self.alive = False
			self.destroy()


		self.update_sprite()

