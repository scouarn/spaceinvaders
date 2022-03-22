import tkinter as tk


# generic game object
class GameObject :

	def __init__(self, canvas, x=0, y=0, vx=0, vy=0, image=None) :
		self.x = x
		self.y = y
		self.vx = vx
		self.vy = vy
		self.acc = 0
		self.canvas = canvas
		self.alive = True

		if image is None :
			self.width = self.height = 0

		else :
			self.width = image.width()
			self.height = image.height()


		self.sprite = self.canvas.create_image(
			self.x, self.y,
			image=image, 
			anchor=tk.NW # top left
		)



	def update_sprite(self) :
		if self.sprite is not None :
			self.canvas.moveto(self.sprite, int(self.x), int(self.y))


	def destroy(self) :
		self.canvas.delete(self.sprite)
		self.sprite = None

	def update(self, dt) :
		
		# movement
		self.x += self.vx * dt
		self.y += self.vy * dt

		self.update_sprite()



	def screen_collision(self) :
		return any([
			self.x < 0, # left
			self.y < 0, # top
			self.x + self.width >= self.canvas.get_width(), # right
			self.y + self.height >= self.canvas.get_height() # bottom
		])


	def collision(o1, o2) :
		return all([
			# horizontal overlap
			o1.x + o1.width >= o2.x,
			o1.x <= o2.x + o2.width,

			# vertical overlap
			o1.y + o1.height >= o2.y,
			o1.y <= o2.y + o2.height,
		])


	def is_alive(self) :
		return self.alive

	def get_x(self) :
		return self.x

	def set_x(self, x) :
		self.x = x

	def add_x(self, dx) :
		self.x += dx

	def get_y(self) :
		return self.y

	def set_y(self, y) :
		self.y = y

	def add_y(self, dy) :
		self.y += dy

	def get_vx(self) :
		return self.vx

	def set_vx(self, vx) :
		self.vx = vx

	def get_vy(self) :
		return self.vy

	def set_vy(self, vy) :
		self.vy = vy
	
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

	def get_width(self) :
		return self.width

	def get_height(self) :
		return self.height
