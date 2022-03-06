import tkinter as tk

from gameObject import GameObject

class Explosion(GameObject) :
	
	image = None

	def __init__(self, canvas, x, y) :

		if Explosion.image is None :
			Explosion.image = tk.PhotoImage(file="assets/explo1.png")

		super().__init__(canvas, x=x, y=y, image=Explosion.image)

		self.timer = 1.0



	def update(self, canvas, dt) :

		self.timer -= dt

		if self.timer <= 0 :
			self.alive = False


		self.update_sprite(canvas)
