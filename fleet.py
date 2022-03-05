

from gameObject import GameObject
from alien import Alien

class Fleet(GameObject) : 


	def __init__(self, canvas) :
		super().__init__(canvas, c="purple")

		self.rows = 4
		self.cols = 8
		self.spacing = 64
		self.vx = 100
		self.vy = 16
		self.finish_line = 500

		self.aliens = []

		for i in range(self.cols) :
			for j in range(self.rows) :
				x = i * self.spacing
				y = j * self.spacing

				a = Alien(canvas)
				a.set_pos(x, y)
				a.set_vel(self.vx, 0)
				
				self.aliens.append(a)

		canvas.create_line(
			0, self.finish_line,
			800, self.finish_line, 
			fill="gray", 
			width=5
		)




	def update(self, canvas, dt) :

		collided = False
		game_over = False

		for a in self.aliens :
			a.update(canvas, dt)

			if a.screen_collision(canvas) :
				collided = True

			if a.get_pos()[1] >= self.finish_line :
				game_over = True	



		if game_over :
			return True


		if collided :
			for a in self.aliens :
				vx, vy = a.get_vel()
				a.set_vel(-vx, vy)

				x, y = a.get_pos()
				a.set_pos(x, y + self.vy)


		return False