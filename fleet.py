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


		self.aliens = [
			Alien(self.canvas, 
				x=i * self.spacing, 
				y=j * self.spacing + 64, 
				vx=self.vx, 
				type=self.rows-j-1 # weakest at the bottom
			)
			for i in range(self.cols)
			for j in range(self.rows)
		]


	def __iter__(self) :
		return iter(self.aliens)

	def __len__(self) :
		return len(self.aliens)

	def remove_bullet(self, b) :
		b.destroy()
		self.bullets.remove(b)		

	def remove(self, a) :
		a.destroy()
		self.aliens.remove(a)


	def destroy(self) :
		super().destroy()

		for a in self :
			a.destroy()

		for b in self.bullets :
			b.destroy()



	def update(self, dt) :

		# attack
		self.timer -= dt
		if self.timer <= 0 :
			self.timer = self.interval
			self.fire()

		for a in self :
			a.update(dt)

		for b in self.bullets :
			b.update(dt)
		

		# speed up and reverse direction
		if self.screen_collision() :

			self.vx *= -self.acc

			for a in self :
				a.set_vx(self.vx) 
				a.add_y(self.vy) 


	def fire(self) :

		# choose a random alien as firing position
		a = random.choice(self.aliens)

		x = a.get_x() + a.get_width() / 2
		y = a.get_y() + a.get_height()
		vy = 350
		
		self.bullets.append(
			Bullet(self.canvas, x, y, vy, dosfx=False)
		)


	def screen_collision(self) :
		return any(a.screen_collision() for a in self)

	def collision(self, obj) :
		return any(a.collision(obj) for a in self)
