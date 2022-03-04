from gameObject import GameObject
from bullet import Bullet

class Defender(GameObject) :
	
	def __init__(self, canvas) :
		super().__init__(canvas)

		self.bullets = []


	def fire(self) :
		pass


	def update(self, canvas, dt) :
		for b in self.bullets :
			b.update(canvas, dt)