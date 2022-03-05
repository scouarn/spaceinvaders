import tkinter as tk


# generic game object
class GameObject :

	def __init__(self, canvas, x=0, y=0, r=10, c="red", image=None) :
		self.x = x
		self.y = y
		self.r = r
		self.c = c
		self.image = image

		self.vx = 0
		self.vy = 0

		self.sprite = canvas.create_image(
			self.x, self.y,
			image = self.image, 
			anchor = tk.NW
		)


	def update(self, canvas, dt) :
		
		# movement
		self.x += self.vx * dt
		self.y += self.vy * dt

		# update sprite position
		canvas.moveto(self.sprite, self.x, self.y)
		
		return False # True for game over


	def set_pos(self, x, y) :
		self.x = x
		self.y = y

	def get_pos(self) :
		return self.x, self.y

	def set_vel(self, vx, vy) :
		self.vx = vx
		self.vy = vy

	def get_vel(self) :
		return self.vx, self.vy

	def screen_collision_N(self, canvas) :
		return self.y < 0

	def screen_collision_W(self, canvas) :	
		return self.x < 0

	def screen_collision_S(self, canvas) :
		y2 = self.y + self.image.height()
		return y2 >= canvas.height()

	def screen_collision_E(self, canvas) :	
		x2 = self.x + self.image.width()
		return x2 >= canvas.width()

	def screen_collision(self, canvas) :
		return self.screen_collision_N(canvas) or self.screen_collision_S(canvas) or self.screen_collision_E(canvas) or self.screen_collision_W(canvas)