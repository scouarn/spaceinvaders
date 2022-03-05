from random import randint

import tkinter as tk


# generic game object
class GameObject :

	def __init__(self, canvas, x=0, y=0, r=10, c="red", image=None) :
		self.x = x
		self.y = y
		self.r = r
		self.c = c
		self.image = image

		self.vx = randint(-100, 100)
		self.vy = randint(-100, 100)

		self.sprite = canvas.create_image(
			self.x, self.y,
			image = self.image, 
			anchor = tk.NW
		)

		print(canvas.coords(self.sprite))


	def update(self, canvas, dt) :
		

		# collisions
		if self.x < 0 or self.x >= canvas.winfo_reqwidth() :
			self.vx = -self.vx

		if self.y < 0 or self.y >= canvas.winfo_reqheight() :
			self.vy = -self.vy

		# movement
		self.x += self.vx * dt
		self.y += self.vy * dt


		# update sprite position
		sx, sy = canvas.coords(self.sprite)
		dx = self.x - sx
		dy = self.y - sy
		canvas.move(self.sprite, dx, dy)



	def set_pos(self, x, y) :
		self.x = x
		self.y = y

	def get_pos(self, x, y) :
		return self.x, self.y

	def set_vel(self, vx, vy) :
		self.vx = vx
		self.vy = vy