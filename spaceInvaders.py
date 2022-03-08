import time
import tkinter as tk

from game import Game


class SpaceInvaders :
	
	def __init__(self) :
		
		self.width = 800
		self.height = 600

		self.win = tk.Tk()
		self.win.title("Space Invaders")

		self.canvas = tk.Canvas(
			self.win, 
			width=self.width,
			height=self.height,
			background="black",
			highlightthickness=0,
		)

		self.canvas.place(relx=0.5, rely=0.5, anchor="center")

		# !!! custom methods for self.canvas so it can relay self.width
		# when self.canvas.width() is called
		self.canvas.width  = lambda : self.width
		self.canvas.height = lambda : self.height

		# escape to quit
		self.win.bind('<Escape>',  lambda ev : self.stop())
		self.win.bind('<Destroy>', lambda ev : self.stop())

		self.frameRate = 60
		self.running = False
		self.game = Game(self.win, self.canvas)


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


			self.game.update(self.canvas, dt)

			# reset game
			if self.game.done :
				self.game.destroy(self.win, self.canvas)
				self.game = Game(self.win, self.canvas)


			self.win.update()

			# limit fps
			dt = time.time() - self.lastTime
			wait = 1/self.frameRate - dt

			if wait > 0 :
				time.sleep(wait)

		self.win.destroy()