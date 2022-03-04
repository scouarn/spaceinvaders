
# generic game object
class GameObject :

	def __init__(self, canvas, x=0, y=0, r=10, c="red") :
		self.x = x
		self.y = y
		self.r = r
		self.c = c

		self.ball = canvas.create_oval(
			self.x - self.r, self.y - self.r,
			self.x + self.r, self.y + self.r,
			fill=self.c, outline="Black", width=1
		)



	def update(self, canvas, dt) :
		pass

	def move(self, dx, dy) :
		self.x += dx
		self.y += dy

	def set_pos(self, x, y) :
		self.x = x
		self.y = y

	