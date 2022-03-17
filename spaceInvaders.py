import time
import tkinter as tk

from game import Game
from canvas import Canvas




class SpaceInvaders :
	
	def __init__(self) :
		
		self.canvas = Canvas(800, 600, "Space Invaders")
		
		# escape to quit
		self.canvas.bind('<Escape>',  lambda ev : self.stop())
		self.canvas.bind('<Destroy>', lambda ev : self.stop())

		self.frameRate = 60
		self.running = False
		self.game = Game(self.canvas)


	def stop(self) :
		# join with the game loop
		self.running = False


	def frame(self) :

		# compute elapsed time
		now = time.time()
		dt = now - self.lastTime
		self.lastTime = now

		self.game.update(dt)

		# restart on game over
		if self.game.done :
			self.game.destroy()
			self.game = Game(self.canvas)

		if self.running :
			self.canvas.tkcanvas.after(1000 // self.frameRate, self.frame)

		else :
			self.canvas.destroy()

	def start(self) :

		self.lastTime = time.time()
		self.running = True
		self.canvas.tkcanvas.after(0, self.frame)
		self.canvas.mainloop()
		
