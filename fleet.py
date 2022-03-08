import tkinter as tk
import random
import time

from gameObject import GameObject
from alien import Alien
from bullet import Bullet

class Fleet(GameObject) : 


	def __init__(self, canvas) :
		super().__init__(canvas)

		self.vx = 100
		self.vy = 16
		self.acc = 1.1
		
		self.rows = 4
		self.cols = 6
		self.spacing = 70


		self.bullets = []
		self.interval = 0.5
		self.timer = 0.0

		self.aliens = []

		xoff = 0
		yoff = 64
	
		for i in range(self.cols) :
			for j in range(self.rows) :
				x = xoff + i * self.spacing
				y = yoff + j * self.spacing

				a = Alien(canvas, x=x, y=y, type=j)
				a.set_vel(self.vx, 0)
				
				self.aliens.append(a)



	def destroy(self, canvas) :
		super().destroy(canvas)

		for a in self.aliens :
			a.destroy(canvas)

		for b in self.bullets :
			b.destroy(canvas)
			

	def update(self, canvas, dt) :

		self.timer -= dt
		if self.timer <= 0 :
			self.timer = self.interval

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

