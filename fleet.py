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
				type=self.rows-j-1
			)
			for i in range(self.cols)
			for j in range(self.rows)
		]



	def destroy(self) :
		super().destroy()

		for a in self.aliens :
			a.destroy()

		for b in self.bullets :
			b.destroy()
			

	def update(self, dt) :

		# attack
		self.timer -= dt
		if self.timer <= 0 :
			self.timer = self.interval

			a = random.choice(self.aliens)
			b = Bullet(self.canvas, a.get_x()+32, a.get_y(), 350, dosfx=False)
			self.bullets.append(b)



		for b in self.bullets :
			b.update(dt)
		
		for a in self.aliens :
			a.update(dt)



		# speed up and reverse direction
		collided = any(
			a.screen_collision() 
			for a in self.aliens
		)

		if collided :
			self.vx *= -self.acc

			for a in self.aliens :
				a.vx = self.vx
				a.y += self.vy