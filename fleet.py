

from gameObject import GameObject
from alien import Alien

class Fleet(GameObject) : 


	def __init__(self, canvas, size=10) :
		super().__init__(canvas, c="purple")

		
		
		self.size = size
		self.aliens = [Alien(canvas) for i in range(size)]


	def update(self, canvas, dt) :

		for a in self.aliens :
			a.update(canvas, dt)