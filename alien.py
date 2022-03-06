
from gameObject import GameObject
from bullet import Bullet

class Alien(GameObject) :
	
	def __init__(self, canvas, image=None) :

		super().__init__(canvas, c="red", image=image)


		self.bullets = []
