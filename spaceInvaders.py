import time
import tkinter as tk

from game import Game


class SpaceInvaders :
	
	def __init__(self) :
		
		self.width = 800
		self.height = 800

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


		self.win.bind('<Escape>',  lambda ev : self.stop())
		self.win.bind('<Destroy>', lambda ev : self.stop())


		self.frameRate = 60
		self.running = False
		self.game = Game(self.canvas)

		self.win.bind('<KeyPress>', self.game.key_down)
		self.win.bind('<KeyRelease>', self.game.key_up)
	

	def stop(self) :
		# join with the game loop
		self.running = False


	def start(self) :

		self.lastTime = time.time()
		self.running = True

		game_over = False


		while self.running :
			now = time.time()
			dt = now - self.lastTime
			self.lastTime = now
			
			if not game_over :
				game_over = self.game.update(self.canvas, dt)

			self.win.update()

			now = time.time()
			dt = now - self.lastTime
			wait = 1/self.frameRate - dt

			if wait > 0 :
				time.sleep(1/self.frameRate)

		self.win.destroy()