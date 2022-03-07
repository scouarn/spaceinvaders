import tkinter as tk

from gameObject import GameObject

class Bullet(GameObject) :
	
	image = None

	def __init__(self, canvas, x, y, vy) :

		if Bullet.image is None :
			Bullet.image = tk.PhotoImage(file="assets/bullet1.png")

		super().__init__(canvas, x=x, y=y, image=Bullet.image)

		self.vy = vy
