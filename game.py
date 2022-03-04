from defender import Defender
from fleet import Fleet

class Game :
	
	def __init__(self, canvas) :
		self.player = Defender(canvas)
		self.fleet = Fleet(canvas, size=10)
		self.running = True


	def update(self, canvas, dt) :
		self.player.update(canvas, dt)
		self.fleet.update(canvas, dt)


