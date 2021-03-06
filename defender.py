import time
import tkinter as tk

from gameObject import GameObject
from bullet import Bullet

class Defender(GameObject) :
	
	image = None

	def __init__(self, canvas, hp=3) :

		# load resources
		if Defender.image is None :
			Defender.image = tk.PhotoImage(file="assets/def1.png")

		x = canvas.get_width() / 2
		y = (canvas.get_height() - Defender.image.height() * 1.5)

		super().__init__(canvas, x=x, y=y, image=Defender.image)


		self.vx = 200

		# top left lives icons
		self.lives = [
			self.canvas.create_image(
				i * self.width, 0,
				image=Defender.image, 
				anchor=tk.NW
			)
			for i in range(hp)
		]


		self.bullets = []
		self.interval = 1.0
		self.timer = 0.0
		self.reload_bar = self.canvas.create_rectangle(
			0, 0, 0, 0, # set later
			fill='white'
		)


		# will be unbound on destroy
		self.canvas.bind("<KeyPress>", self.key_down)
		self.canvas.bind("<KeyRelease>", self.key_up)

		# true if the key is held
		# updated on key event
		self.keys = {
			"left"  : False, 
			"right" : False, 
			"fire"  : False
		} 



	def destroy(self) :
		super().destroy()

		for l in self.lives :
			self.canvas.delete(l)

		for b in self.bullets : 
			b.destroy()

		self.canvas.delete(self.reload_bar)
		self.canvas.unbind("<KeyPress>")
		self.canvas.unbind("<KeyRelease>")

	
	def remove_bullet(self, b) :
		b.destroy()
		self.bullets.remove(b)		


	def update(self, dt) :

		# move left
		if self.keys["left"] and self.x > 0 :
			self.x -= self.vx * dt

		# move right
		if self.keys["right"] and self.x + self.width < self.canvas.get_width() :
			self.x += self.vx * dt

		# handle shooting
		self.timer -= dt
		if self.keys["fire"] and self.timer <= 0 :
			self.timer = self.interval
			self.fire()

		# update reload bar
		x = 1.0 - self.timer / self.interval
		self.canvas.coords(
			self.reload_bar, 
			0, 
			self.canvas.get_height()-10, 
			x * self.canvas.get_width(), 
			self.canvas.get_height()
		)

		# green full bar
		color = "orange" if self.timer > 0 else "green"
		self.canvas.itemconfig(self.reload_bar, fill=color)


		# update bullets
		for b in self.bullets :
			b.update(dt)

			if b.screen_collision() :
				self.remove_bullet(b)


		self.update_sprite()



	def fire(self) :
		
		# bullet pos and vel
		x = self.get_x() + self.get_width() / 2
		y = self.get_y() - self.get_height()
		vy = -350 # go up
		
		self.bullets.append(
			Bullet(self.canvas, x, y, vy, dosfx=True)
		)
 

	def hit(self) :

		if self.lives :
			L = self.lives.pop()
			self.canvas.delete(L)

		else : # dead when no more lives
			self.alive = False



	def key_down(self, e) :
		
		if e.keysym == "space" :
			self.keys["fire"] = True

		elif e.keysym == "Left" :
			self.keys["left"] = True
			
		elif e.keysym == "Right" :
			self.keys["right"] = True
			

	def key_up(self, e) :

		if e.keysym == "space" :
			self.keys["fire"] = False

		elif e.keysym == "Left" :
			self.keys["left"] = False
			
		elif e.keysym == "Right" :
			self.keys["right"] = False
