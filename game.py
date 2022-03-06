from defender import Defender
from fleet import Fleet
from explosion import Explosion

class Game :


	def __init__(self, canvas) :
		self.fleet = Fleet(canvas)
		self.finish_line = canvas.height() - 100

		self.player = Defender(canvas)
		self.player.set_pos(
			canvas.width() / 2, 
			(self.finish_line + canvas.height() - + Defender.image.height()) / 2)

		self.explosions = []

		self.leftKey  = False
		self.rightKey = False
		self.fireKey = False


		canvas.create_line(
			0, self.finish_line,
			canvas.width(), self.finish_line, 
			fill="gray", 
			width=5
		)



	def update(self, canvas, dt) :

		self.player.update(canvas, dt, self.leftKey, self.rightKey, self.fireKey)
		self.fleet.update(canvas, dt)

		for e in self.explosions :
			e.update(canvas, dt)

			if not e.alive :
				e.destroy(canvas)
				self.explosions.remove(e)


		# check if player bullets hit aliens
		for a in self.fleet.aliens :
			for b in self.player.bullets :

				if a.collision(b) :
					a.destroy(canvas)
					b.destroy(canvas)

					self.fleet.aliens.remove(a)
					self.player.bullets.remove(b)

					self.boom(canvas, a.x, a.y)



		# check if an alien has past the "finish line"
		if any([a.y + a.height >= self.finish_line for a in self.fleet.aliens]) :
			self.game_over(canvas)
			return True

		# check if an alien bullet hits the player
		for b in self.fleet.bullets :
			if self.player.collision(b) :
				self.boom(canvas, self.player.x, self.player.y)
				self.player.hit(canvas)
				b.destroy(canvas)
				self.fleet.bullets.remove(b)


		# check if the player is dead
		if not self.player.alive :
			self.game_over(canvas)
			return True

		# check if all the aliens are dead
		if len(self.fleet.aliens) == 0 :
			self.game_over(canvas, text="YOU WIN !")
			return True


		return False


	def boom(self, canvas, x, y) :
		e = Explosion(canvas, x, y)
		self.explosions.append(e)
		canvas.lower(e.sprite)


	def game_over(self, canvas, text="GAME OVER !") :
		canvas.create_text(
			canvas.width()/2,
			canvas.height()/2, 
			text=text, 
			fill="white", 
			font=('Arial 32 bold')
		)



	def key_down(self, e) :
		
		if e.keysym == "space" :
			self.fireKey = True

		elif e.keysym == "Left" :
			self.leftKey = True
			
		elif e.keysym == "Right" :
			self.rightKey = True
			

	def key_up(self, e) :

		if e.keysym == "space" :
			self.fireKey = False

		elif e.keysym == "Left" :
			self.leftKey = False
			
		elif e.keysym == "Right" :
			self.rightKey = False
