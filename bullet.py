from gameObject import GameObject

class Bullet(GameObject) :

	def __init__(self, canvas) :
		super().__init__(canvas, c="blue")

	def hit(self) :
		pass
