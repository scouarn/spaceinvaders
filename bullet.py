import tkinter as tk

from gameObject import GameObject

class Bullet(GameObject) :
	
	image = None

	def __init__(self, canvas, x, y, vy) :

		if Bullet.image is None :
			Bullet.image = tk.PhotoImage(file="assets/bullet.png")

		super().__init__(canvas, image=Bullet.image)
		
		self.x = x
		self.y = y
		self.vy = vy
