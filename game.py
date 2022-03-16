from defender import Defender
from fleet import Fleet
from explosion import Explosion
import audio

import tkinter as tk
import re


class Game :

	sound_lose = "assets/lose.wav"
	sound_win  = "assets/win.wav"

	def __init__(self, win, canvas) :
		self.canvas = canvas
		self.win = win

		self.fleet = Fleet(self.canvas)
		self.finish_line = self.canvas.height() * 0.8

		self.player = Defender(self.canvas)
		self.player.set_pos(
			self.canvas.width() / 2, 
			(self.finish_line + self.canvas.height() - Defender.image.height()) / 2)


		self.explosions = []

		self.leftKey  = False
		self.rightKey = False
		self.fireKey = False

		self.done = False # flag the parent object that it can delete/reset the game object
		self.game_over = False
		self.game_over_text = None
		self.replay_text = None



		self.win.bind("<KeyPress>", self.key_down)
		self.win.bind("<KeyRelease>", self.key_up)
	

		self.finish_line_gfx = self.canvas.create_line(
			0, 
			self.finish_line,
			self.canvas.width(), 
			self.finish_line, 
			fill="gray", 
			width=5
		)

		self.score_text = self.canvas.create_text(
			self.canvas.width() - 10,
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
		self.addScore(0)


	def destroy(self) :
		self.fleet.destroy()
		self.player.destroy()

		self.canvas.delete(self.finish_line_gfx)
		self.canvas.delete(self.game_over_text)
		self.canvas.delete(self.replay_text)
		self.canvas.delete(self.score_text)

		for e in self.explosions :
			e.destroy()

		self.win.unbind("<KeyPress>")
		self.win.unbind("<KeyRelease>")
		

	def update(self, dt) :

		# nothing to do on the game over screen
		if self.game_over :
			return

		# update defender and fleet
		self.player.update(dt, self.leftKey, self.rightKey, self.fireKey)
		self.fleet.update(dt)


		# update explosions
		for e in self.explosions :
			e.update(dt)

			if not e.isAlive() :
				self.explosions.remove(e)


		# check if player bullets hit aliens
		collisions = [(a, b)
			for a in self.fleet.aliens
			for b in self.player.bullets
			if a.collision(b)
		]

		# handle bullets
		for b in set(b for _, b in collisions) :
			b.destroy()
			self.player.bullets.remove(b)

		# handle aliens
		for a in set(a for a, _ in collisions) :
			a.destroy()
			self.fleet.aliens.remove(a)

			self.addScore(a.point_value)
			self.boom(a.get_x(), a.get_y())
			

		# check if an alien bullet hits the player
		collisions = [b 
			for b in self.fleet.bullets
			if self.player.collision(b)
		]

		for b in collisions :
			self.boom(self.player.get_x(), self.player.get_y())
			self.player.hit()
			b.destroy()
			self.fleet.bullets.remove(b)


		# check if an alien has reach the finish line
		if any(a.y + a.height >= self.finish_line for a in self.fleet.aliens) :
			self.do_game_over()


		# check if the player is dead
		elif not self.player.isAlive() :
			self.do_game_over()


		# check if all the aliens are dead
		elif not self.fleet.aliens :
			self.addScore(10000)
			self.do_game_over()



	def boom(self, x, y) :
		e = Explosion(self.canvas, x, y)
		self.explosions.append(e)

		# show explosions behind other sprites
		self.canvas.lower(e.sprite)


	def do_game_over(self, win=False) :
		self.game_over = True

		if win : 
			text = "GAME OVER !"
			sound = Game.soud_lose

		else :
			text = "YOU WIN !"
			sound = Game.sound_win

		audio.stop_all()
		audio.play_wav(sound)


		self.game_over_text = self.canvas.create_text(
			self.canvas.width()/2,
			self.canvas.height()/2, 
			text=text, 
			fill="white", 
			font=('Arial 32 bold')
		)

		self.replay_text = self.canvas.create_text(
			self.canvas.width()/2,
			self.canvas.height() * 0.75, 

			text="Press space to replay.", 
			fill="white", 
			font=('Arial 24 bold')
		)

		self.saveScore()


	def addScore(self, n) :
		self.current_score += n

		# uninitialized scores
		assert(self.player_name in self.scores)


		best_score = self.scores[self.player_name]

		if best_score < self.current_score :
			best_score = self.current_score
			self.scores[self.player_name] = self.current_score

		self.canvas.itemconfig(
			self.score_text, 
			text=f"score: {self.current_score:06d}\nbest : {best_score:06d}"
		)


	def loadScore(self, fname="scores") :

		try :
			with open(fname, 'r') as fp :
				self.scores = eval(fp.read())

		except FileNotFoundError :
			# ignore the procedure if the file doesn't exist
			pass


		if self.player_name not in self.scores :
			self.scores[self.player_name] = self.current_score


	def saveScore(self, fname="scores") :
		with open(fname, 'w') as fp :
			fp.write(str(self.scores))


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
