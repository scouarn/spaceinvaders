from defender import Defender
from fleet import Fleet
from explosion import Explosion

import tkinter as tk
import re


class Game :


	def __init__(self, win, canvas) :
		self.fleet = Fleet(canvas)
		self.finish_line = canvas.height() * 0.8

		self.player = Defender(canvas)
		self.player.set_pos(
			canvas.width() / 2, 
			(self.finish_line + canvas.height() - + Defender.image.height()) / 2)


		self.explosions = []

		self.leftKey  = False
		self.rightKey = False
		self.fireKey = False

		self.done = False # flag the parent object that it can delete/reset the game object
		self.game_over = False
		self.game_over_text = None
		self.replay_text = None



		win.bind("<KeyPress>", self.key_down)
		win.bind("<KeyRelease>", self.key_up)
	

		self.finish_line_gfx = canvas.create_line(
			0, self.finish_line,
			canvas.width(), self.finish_line, 
			fill="gray", 
			width=5
		)

		self.score_text = canvas.create_text(
			canvas.width() - 10,
			10, 
			anchor=tk.NE,
			text='', 
			fill="white", 
			font=('Mono 20 bold italic')
		)

		self.player_name = "PLAYER1"
		self.current_score = 0
		self.scores = {}
		self.loadScore()

		# init score graphics
		self.addScore(canvas, 0)


	def destroy(self, win, canvas) :
		self.fleet.destroy(canvas)
		self.player.destroy(canvas)

		canvas.delete(self.finish_line_gfx)
		canvas.delete(self.game_over_text)
		canvas.delete(self.replay_text)
		canvas.delete(self.score_text)

		for e in self.explosions :
			e.destroy(canvas)

		win.unbind("<KeyPress>")
		win.unbind("<KeyRelease>")
		

	def update(self, canvas, dt) :

		# nothing to do on the game over screen
		if self.game_over :
			return

		# update defender and fleet
		self.player.update(canvas, dt, self.leftKey, self.rightKey, self.fireKey)
		self.fleet.update(canvas, dt)

		# update explosions
		for e in self.explosions :
			e.update(canvas, dt)

			if not e.alive :
				self.explosions.remove(e)


		# check if player bullets hit aliens
		for a in self.fleet.aliens :
			for b in self.player.bullets :

				if a.collision(b) :
					a.destroy(canvas)
					b.destroy(canvas)

					self.boom(canvas, a.x, a.y)
					self.addScore(canvas, a.point_value)
					
					self.fleet.aliens.remove(a)
					self.player.bullets.remove(b)

					# the alien has been removed,
					# skip to the next one
					break 


		# check if an alien bullet hits the player
		for b in self.fleet.bullets :
			if self.player.collision(b) :
				self.boom(canvas, self.player.x, self.player.y)
				self.player.hit(canvas)
				b.destroy(canvas)
				self.fleet.bullets.remove(b)


		# check if an alien has reach the finish line
		# if any([a.y + a.height >= self.finish_line for a in self.fleet.aliens]) :
			# self.do_game_over(canvas)
			# return
		for a in self.fleet.aliens :
			if a.y + a.height >= self.finish_line :
				self.do_game_over(canvas)
				return


		# check if the player is dead
		if not self.player.alive :
			self.do_game_over(canvas)
			return

		# check if all the aliens are dead
		if len(self.fleet.aliens) == 0 :
			self.addScore(canvas, 10000)
			self.do_game_over(canvas, text="YOU WIN !")
			return


	def boom(self, canvas, x, y) :
		e = Explosion(canvas, x, y)
		self.explosions.append(e)

		# show explosions behind other sprites
		canvas.lower(e.sprite)


	def do_game_over(self, canvas, text="GAME OVER !") :
		self.game_over = True

		self.game_over_text = canvas.create_text(
			canvas.width()/2,
			canvas.height()/2, 
			text=text, 
			fill="white", 
			font=('Arial 32 bold')
		)

		self.replay_text = canvas.create_text(
			canvas.width()/2,
			canvas.height() * 0.75, 

			text="Press space to replay.", 
			fill="white", 
			font=('Arial 24 bold')
		)

		self.saveScore()


	def addScore(self, canvas, n) :
		self.current_score += n

		# uninitialized scores
		assert(self.player_name in self.scores)


		best_score = self.scores[self.player_name]

		if best_score < self.current_score :
			best_score = self.current_score
			self.scores[self.player_name] = self.current_score

		canvas.itemconfig(
			self.score_text, 
			text=f"score: {self.current_score:06d}\nbest : {best_score:06d}"
		)


	def loadScore(self, fname="scores") :


		try :
			fp = open(fname, 'r')

			for l in fp.readlines() :
				if m := re.match(r"([a-zA-Z0-1]+):(\d+)", l) :
					score = int(m.group(2))
					player = m.group(1)

					# keep the biggest score if it already exists
					if player not in self.scores or self.scores[player] < score :
						self.scores[player] = score 

			fp.close()


		# ignore the procedure if the file doesn't exist
		except FileNotFoundError :
			pass

		if self.player_name not in self.scores :
			self.scores[self.player_name] = self.current_score

	def saveScore(self, fname="scores") :

		with open(fname, 'w') as fp :
			for k, v in self.scores.items() :
				fp.write(f"{k}:{v}\n")


	def key_down(self, e) :
		
		if e.keysym == "space" :
			self.fireKey = True

			# replay/exit
			if self.game_over :
				self.done = True


		elif e.keysym == "Left" :
			self.leftKey = True
			
		elif e.keysym == "Right" :
			self.rightKey = True
			

	def key_up(self, e) :

		if e.keysym == "space" :
			self.fireKey = False

		elif e.keysym == "Left" :
			self.leftKey = False
			
		elif e.keysym == "Right" :
			self.rightKey = False
