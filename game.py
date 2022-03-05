from defender import Defender
from fleet import Fleet

class Game :
	
	def __init__(self, canvas) :
		self.fleet = Fleet(canvas)

		self.player = Defender(canvas)
		self.player.set_pos(0, 516)


	def update(self, canvas, dt) :

		if self.player.update(canvas, dt) :
			self.game_over(canvas)
			return True

		if self.fleet.update(canvas, dt) :
			self.game_over(canvas)
			return True


	def game_over(self, canvas) :
		canvas.create_text(
			canvas.width()/2,
			canvas.height()/2, 
			text="GAME OVER !", 
			fill="white", 
			font=('Arial 24 bold')
		)
