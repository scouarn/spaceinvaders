import tkinter as tk


# generic game object
class GameObject :

	def __init__(self, canvas, x=0, y=0, r=10, c="red", image=None) :
		self.x = x
		self.y = y
		self.r = r
		self.c = c
		self.alive = True

		if image is None :
			self.width = self.height = 0

		else :
			self.width = image.width()
			self.height = image.height()

		self.vx = 0
		self.vy = 0

		self.sprite = canvas.create_image(
			self.x, self.y,
			image=image, 
			anchor=tk.NW
		)


	def update_sprite(self, canvas) :
		canvas.moveto(self.sprite, int(self.x), int(self.y))

	def destroy(self, canvas) :
		canvas.delete(self.sprite)

	def update(self, canvas, dt) :
		
		# movement
		self.x += self.vx * dt
		self.y += self.vy * dt

		self.update_sprite(canvas)

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
		y2 = self.y + self.height
		return y2 >= canvas.height()

	def screen_collision_E(self, canvas) :	
		x2 = self.x + self.width
		return x2 >= canvas.width()

	def screen_collision(self, canvas) :
		return self.screen_collision_N(canvas) or self.screen_collision_S(canvas) or self.screen_collision_E(canvas) or self.screen_collision_W(canvas)

	def collision(o1, o2) :
		H = o1.x + o1.width  >= o2.x and o1.x <= o2.x + o2.width
		V = o1.y + o1.height >= o2.y and o1.y <= o2.y + o2.height

		return H and V