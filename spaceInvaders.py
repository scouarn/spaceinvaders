import time
import tkinter as tk

from game import Game


class SpaceInvaders(tk.Tk) :
	
	def __init__(self) :
		super().__init__()


		self.title("Space Invaders")

		self.canvas = tk.Canvas(self, background="black")


		self.fpsBox = tk.Label(self, text="FPS")
		self.fpsBox.place(x=0, y=0)

		self.canvas.pack(fill="both", expand=True)

		self.frameRate = 60
		self.running = False
		self.game = Game(self.canvas)



	def destroy(self) :
		# override super().destroy(),
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
			self.update()


			time.sleep(1/self.frameRate)


		super().destroy()