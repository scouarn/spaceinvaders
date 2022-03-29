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

		self.running = False
		self.game = Game(self.canvas)


	def stop(self) :
		self.running = False


	def frame_event(self) :

		# compute elapsed time
		now = time.time()
		dt = now - self.lastTime
		self.lastTime = now

		self.game.update(dt)

		# restart on game over
		if self.game.is_done() :
			self.game.destroy()
			self.game = Game(self.canvas)

		if self.running :
			# max at 60 fps
			self.canvas.after(1000 // 60, self.frame_event)

		else :
			self.canvas.destroy()


	def start(self) :

		self.lastTime = time.time()
		self.running = True
		self.canvas.after(0, self.frame_event)
		self.canvas.mainloop()
		
