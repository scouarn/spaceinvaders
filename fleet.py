import tkinter as tk
import random
import time

from gameObject import GameObject
from alien import Alien
from bullet import Bullet

class Fleet(GameObject) : 


	def __init__(self, canvas) :
		super().__init__(canvas, c="purple")

		self.rows = 4
		self.cols = 6
		self.spacing = 70
		self.vx = 100
		self.vy = 16
		self.acc = 1.1

		self.images = [
			tk.PhotoImage(file="assets/alien1.png"),
			tk.PhotoImage(file="assets/alien2.png"),
			tk.PhotoImage(file="assets/alien3.png"),
			tk.PhotoImage(file="assets/alien4.png"),
		]

		self.bullets = []
		self.lastshot = time.time()
		self.interval = 0.5

		self.aliens = []

		xoff = 0
		yoff = 64
	
		for i in range(self.cols) :
			for j in range(self.rows) :
				x = xoff + i * self.spacing
				y = yoff + j * self.spacing

				image = self.images[j % len(self.images)]
				a = Alien(canvas, image=image)
				a.set_pos(x, y)
				a.set_vel(self.vx, 0)
				
				self.aliens.append(a)


	def update(self, canvas, dt) :

		now = time.time()
		if now - self.lastshot >= self.interval :
			self.lastshot = now

			a = random.choice(self.aliens)
			b = Bullet(canvas, a.x+32, a.y, 350)
			self.bullets.append(b)



		for b in self.bullets :
			b.update(canvas, dt)


		collided = False
		
		for a in self.aliens :
			a.update(canvas, dt)

			if a.screen_collision(canvas) :
				collided = True


		# speed up and reverse direction
		if collided :
			self.vx *= -self.acc

			for a in self.aliens :
				a.vx = self.vx
				a.y += self.vy

