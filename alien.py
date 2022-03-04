from gameObject import GameObject
from bullet import Bullet

class Alien(GameObject) :
	
	def __init__(self, canvas) :
		super().__init__(canvas)

		self.bullets = []


	def draw(self, canvas) :
		super().draw(canvas)
		
		for b in self.bullets :
			b.draw(canvas)


	def update(self, canvas, dt) :

		for b in self.bullets :
			b.update(canvas, dt)