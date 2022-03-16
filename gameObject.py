import tkinter as tk


# generic game object
class GameObject :

	def __init__(self, canvas, x=0, y=0, vx=0, vy=0, image=None) :
		self.x = x
		self.y = y
		self.vx = vx
		self.vy = vy
		self.canvas = canvas

		if image is None :
			self.width = self.height = 0

		else :
			self.width = image.width()
			self.height = image.height()

		self.alive = True

		self.sprite = self.canvas.create_image(
			self.x, self.y,
			image=image, 
			anchor=tk.NW
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

		return False # True for game over

	def isAlive(self) :
		return self.alive

	def get_x(self) :
		return self.x

	def set_x(self, x) :
		self.x = x

	def get_y(self) :
		return self.y

	def set_x(self, y) :
		self.y = y

	def get_vx(self) :
		return self.vx

	def set_vx(self, vx) :
		self.vx = vx

	def get_vy(self) :
		return self.vy

	def set_x(self, vy) :
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


	def screen_collision(self) :
		return any([
			self.x < 0,
			self.y < 0,
			self.x + self.width >= self.canvas.width(),
			self.y + self.height >= self.canvas.height()
		])


	def collision(o1, o2) :
		return all([
			o1.x + o1.width >= o2.x,
			o1.y + o1.height >= o2.y,
			o1.x <= o2.x + o2.width,
			o1.y <= o2.y + o2.height,
		])