import time
import tkinter as tk

from gameObject import GameObject
from bullet import Bullet

class Defender(GameObject) :
	
	image = None

	def __init__(self, canvas, hp=3) :

		# load resources
		if Defender.image is None :
			Defender.image = tk.PhotoImage(file="assets/def1.png")

		super().__init__(canvas, image=Defender.image)


		self.vx = 200

		self.lives = []

		for i in range(hp) :
			s = canvas.create_image(
				i * self.width, 0,
				image=Defender.image, 
				anchor=tk.NW
			)

			self.lives.append(s)

		self.reload_bar = canvas.create_rectangle(
			0, 0, 0, 0, # set later
			fill='white'
		)


		self.bullets = []
		self.interval = 1.0
		self.timer = 0.0



	def destroy(self, canvas) :
		super().destroy(canvas)

		for l in self.lives :
			canvas.delete(l)

		for b in self.bullets :
			b.destroy(canvas)

		canvas.delete(self.reload_bar)

		

	def update(self, canvas, dt, Lkey, Rkey, Fkey) :

		if Lkey and self.x > 0 :
			self.x -= self.vx * dt

		if Rkey and self.x + self.width < canvas.width() :
			self.x += self.vx * dt

		# handle shooting
		self.timer -= dt
		if Fkey and self.timer <= 0 :
			self.timer = self.interval
			b = Bullet(canvas, self.x+32, self.y, -350)
			self.bullets.append(b)


		# update reload bar
		x = 1.0 - self.timer / self.interval
		canvas.coords(
			self.reload_bar, 
			0, canvas.height()-10, 
			x * canvas.width(), canvas.height()
		)

		color = 'orange' if self.timer > 0 else 'green'
		canvas.itemconfig(self.reload_bar, fill=color)

		# update bullets
		for b in self.bullets :
			b.update(canvas, dt)

			if b.screen_collision(canvas) :
				b.destroy(canvas)
				self.bullets.remove(b)

		self.update_sprite(canvas)


	def hit(self, canvas) :

		if self.lives :
			L = self.lives.pop()
			canvas.delete(L)

		else :
			self.alive = False

