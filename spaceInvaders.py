import time
import tkinter as tk

from game import Game


class SpaceInvaders :
	
	def __init__(self) :
		
		self.win = tk.Tk()
		self.win.title("Space Invaders")

		self.canvas = tk.Canvas(
			self.win, 
			width=800,
			height=600,
			background="black",
			highlightthickness=0,
		)

		# self.canvas.grid()
		# self.canvas.pack(fill="both", expand=False)
		# self.canvas.grid(stick="N S E W")
		self.canvas.place(relx=0.5, rely=0.5, anchor="center")



		self.fpsBox = tk.Label(self.win, text="FPS")
		self.fpsBox.place(x=0, y=0)

		self.canvas.bind('<Configure>', self.ev_resize)
		self.win.bind('<Escape>', lambda ev : self.stop())



		self.frameRate = 60
		self.running = False
		self.game = Game(self.canvas)


	def ev_resize(self, e) :
		# self.canvas.config(width=e.width, height=e.height)
		pass


	def stop(self) :
		# join with the game loop
		self.running = False


	def start(self) :

		self.lastTime = time.time()
		self.running = True


		while self.running :
			now = time.time()
			dt = now - self.lastTime
			self.lastTime = now
			
			self.fpsBox["text"] = f"FPS {round(1/dt)}"

			self.game.update(self.canvas, dt)
			self.win.update()

			now = time.time()
			dt = now - self.lastTime
			wait = 1/self.frameRate - dt

			if wait > 0 :
				time.sleep(1/self.frameRate)




		self.win.destroy()