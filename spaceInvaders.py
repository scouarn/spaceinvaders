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


	def start(self) :

		self.lastTime = time.time()
		self.running = True


		while self.running :

			# compute elapsed time
			now = time.time()
			dt = now - self.lastTime
			self.lastTime = now


			self.game.update(dt)

			# handle post game over
			if self.game.done :
				self.game.destroy()
				self.game = Game(self.canvas)


			self.canvas.update()

			# limit fps
			dt = time.time() - self.lastTime
			wait = 1/self.frameRate - dt

			if wait > 0 :
				time.sleep(wait)


		self.canvas.destroy()