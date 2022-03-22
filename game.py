from defender import Defender
from fleet import Fleet
from explosion import Explosion

import tkinter as tk
import re


class Game :

	sound_lose = "assets/lose.wav"
	sound_win  = "assets/win.wav"

	def __init__(self, canvas) :
		self.canvas = canvas

		self.fleet = Fleet(self.canvas)
		self.finish_line = self.canvas.get_height() * 0.8

		self.player = Defender(self.canvas)
		self.player.set_pos(
			self.canvas.get_width() / 2, 
			(self.finish_line + self.canvas.get_height() - Defender.image.height()) / 2)


		self.explosions = []

		# relevent keys beeing held down
		self.keys = {
			'left': False, 
			'right' : False, 
			'fire' : False
		}


		self.done = False # past the game over screen
		self.game_over = False
		self.game_over_text = None
		self.replay_text = None

		# unbind on destroy
		self.canvas.bind("<KeyPress>", self.key_down)
		self.canvas.bind("<KeyRelease>", self.key_up)
		
		# gray line at the bottom
		self.finish_line_gfx = self.canvas.create_line(
			0, 
			self.finish_line,
			self.canvas.get_width(), 
			self.finish_line, 
			fill="gray", 
			width=5
		)

		# set empty at the start
		self.score_text = self.canvas.create_text(
			self.canvas.get_width() - 10,
			10, 
			anchor=tk.NE,
			text="", 
			fill="white", 
			font=('Mono 20 bold italic')
		)

		# placeholder name
		self.player_name = "PLAYER1"
		self.current_score = 0
		self.load_scores()

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

		self.canvas.unbind("<KeyPress>")
		self.canvas.unbind("<KeyRelease>")

		
	def is_done(self) :
		return self.done

	def update(self, dt) :

		# nothing to do on the game over screen 
		if self.game_over :
			return

		# update defender and fleet
		self.player.update(dt, self.keys)
		self.fleet.update(dt)


		# update explosions
		for e in self.explosions :
			
			if not e.is_alive() :
				self.explosions.remove(e)
			else :
				e.update(dt)


		# check if player bullets hit aliens
		collisions = [(a, b)
			for a in self.fleet
			for b in self.player.bullets
			if a.collision(b)
		]

		# use sets so one thing isn't
		# removed multiple times

		# handle bullets
		for b in {b for _, b in collisions} :
			self.player.remove_bullet(b)

		# handle aliens
		for a in {a for a, _ in collisions} :
			self.addScore(a.get_value())
			self.boom(a.get_x(), a.get_y())
			self.fleet.remove(a)
			

		# check if an alien bullet hits the player
		collisions = [b 
			for b in self.fleet.bullets
			if self.player.collision(b)
		]

		for b in collisions :
			self.boom(self.player.get_x(), self.player.get_y())
			self.player.hit()
			self.fleet.remove_bullet(b)


		# check if one or more alien has reach the finish line
		if any(a.y + a.height >= self.finish_line 
			for a in self.fleet) :
			self.do_game_over()


		# check if the player is dead
		elif not self.player.is_alive() :
			self.do_game_over()


		# check if all the aliens are dead
		elif len(self.fleet) == 0 :
			self.addScore(10000)
			self.do_game_over(win=True)



	def boom(self, x, y) :
		e = Explosion(self.canvas, x, y)
		self.explosions.append(e)

		# show explosions behind other sprites
		self.canvas.lower(e.sprite)


	def do_game_over(self, win=False) :
		self.game_over = True

		if win : 
			text = "YOU WIN !"
			sound = Game.sound_win

		else :
			text = "GAME OVER !"
			sound = Game.sound_lose

		self.canvas.stop_all()
		self.canvas.play_wav(sound)


		self.game_over_text = self.canvas.create_text(
			self.canvas.get_width()/2,
			self.canvas.get_height()/2, 
			text=text, 
			fill="white", 
			font=('Arial 32 bold')
		)

		self.replay_text = self.canvas.create_text(
			self.canvas.get_width()/2,
			self.canvas.get_height() * 0.75, 

			text="Press space to replay.", 
			fill="white", 
			font=('Arial 24 bold')
		)

		self.save_scores()



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


	def load_scores(self, fname="scores") :
		try :
			with open(fname, 'r') as fp :
				self.scores = eval(fp.read())

		except FileNotFoundError :
			self.scores = {}

		finally :
			if self.player_name not in self.scores :
				self.scores[self.player_name] = self.current_score


	def save_scores(self, fname="scores") :
		with open(fname, 'w') as fp :
			fp.write(str(self.scores))


	def key_down(self, e) :
		
		if e.keysym == "space" :
			self.keys['fire'] = True

			# replay/exit on key down and not on key held
			if self.game_over :
				self.done = True

		elif e.keysym == "Left" :
			self.keys['left'] = True
			
		elif e.keysym == "Right" :
			self.keys['right'] = True
			

	def key_up(self, e) :

		if e.keysym == "space" :
			self.keys['fire'] = False

		elif e.keysym == "Left" :
			self.keys['left'] = False
			
		elif e.keysym == "Right" :
			self.keys['right'] = False
