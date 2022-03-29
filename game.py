from defender import Defender
from fleet import Fleet
from explosion import Explosion

import tkinter as tk
import re


class Game :

	scores_file_name = "scores"

	sound_lose = "assets/lose.wav"
	sound_win  = "assets/win.wav"

	def __init__(self, canvas) :
		self.canvas = canvas

		self.fleet = Fleet(self.canvas)
		self.player = Defender(self.canvas)
		self.explosions = []

		self.done = False 
		self.state_function = self.state_game

		# game over if an alien goes under this height
		self.finish_line = self.canvas.get_height() * 0.8

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
			fill="white", 
			font=('Arial 20 bold italic')
		)


		self.current_score = 0
		self.add_score(0) # init score graphics



	def destroy(self) :
		self.fleet.destroy()
		self.player.destroy()

		self.canvas.delete(self.finish_line_gfx)
		self.canvas.delete(self.score_text)

		for e in self.explosions :
			e.destroy()


	def is_done(self) :
		return self.done


	def update(self, dt) :
		self.state_function(dt)


	def state_game(self, dt) :

		# update defender and fleet
		self.player.update(dt)
		self.fleet.update(dt)


		# update explosions
		for e in self.explosions :
			
			if not e.is_alive() :
				self.explosions.remove(e)
			else :
				e.update(dt)


		# check if player bullets hit aliens
		# many to many
		collisions = [(a, b)
			for a in self.fleet
			for b in self.player.bullets
			if a.collision(b)
		]

		# use sets and not lists so everything is
		# handled once

		# handle bullets
		for b in {b for _, b in collisions} :
			self.player.remove_bullet(b)

		# handle aliens
		for a in {a for a, _ in collisions} :
			self.add_score(a.get_value())
			self.boom(a.get_x(), a.get_y())
			self.fleet.remove(a)


		# check if an alien bullet hits the player
		# many to one
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
			self.transition_game_over()


		# check if the player is dead
		elif not self.player.is_alive() :
			self.transition_game_over()


		# check if all the aliens are dead
		elif len(self.fleet) == 0 :
			self.add_score(10000)
			self.transition_game_over(win=True)



	def boom(self, x, y) :
		e = Explosion(self.canvas, x, y)
		self.explosions.append(e)

		# show explosions behind other sprites
		self.canvas.lower(e.sprite)



	def transition_game_over(self, win=False) :

		self.state_function = self.state_game_over
		self.fleet.destroy() # remove clutter


		# choose the correct text and sound
		if win : 
			text = "YOU WIN !"
			sound = Game.sound_win

		else :
			text = "GAME OVER !"
			sound = Game.sound_lose

		# play sound
		self.canvas.stop_all()
		self.canvas.play_wav(sound)

		# display text
		game_over_text = self.canvas.create_text(
			self.canvas.get_width()/2,
			50, 
			text=text, 
			fill="white", 
			font=('Arial 32 bold')
		)


		# score table
		highscores_text = self.canvas.create_text(
			self.canvas.get_width()/2,
			100,
			fill="white", 
			font=('Arial 15'),
			justify="right",
			anchor=tk.N
			# empty content, filled on the first "update" call
		)


		scores = self.load_scores()

		def update_highscores() :
			values = list(scores.items())[:10]
			values.sort(key=lambda kv : kv[1], reverse=True)

			lines = [f"{k} : {v:06d}" for k, v in values]
			text = "\n".join(lines)

			self.canvas.itemconfig(
				highscores_text,
				text=text)


		def on_save() :
			# get player name from the textbox
			player = name_entry.get().upper()
			
			# compare current score to the highscores
			if player in scores :
				scores[player] = max(scores[player], self.current_score)		

			else :
				scores[player] = self.current_score

			self.save_scores(scores, player)
			update_highscores()

			# prevent user from entering same score twice
			save_button["state"] = "disabled"
			name_entry["state"] = "disabled"
			

		def on_replay() :
			name_entry.place_forget()
			save_button.place_forget()
			replay_button.place_forget()

			# !! widget.destroy() destroys the root window !!
			# name_entry.destroy()
			# save_button.destroy()
			# replay_button.destroy()

			self.canvas.delete(game_over_text)
			self.canvas.delete(highscores_text)

			self.done = True


		# init table
		update_highscores()


		# show menu
		name_entry = tk.Entry(self.canvas.tkcanvas)
		name_entry.insert(0, "your name")
		
		save_button = tk.Button(self.canvas.tkcanvas, text="SAVE SCORE", 
			command=on_save)

		replay_button = tk.Button(self.canvas.tkcanvas, text="PLAY AGAIN", 
			command=on_replay)

		x = self.canvas.get_width() / 2
		y = self.canvas.get_height() * 0.60
		w = 100
		h = 25
		a = tk.CENTER

		name_entry.place(   x=x, y=y,    width=w, height=h, anchor=a)
		save_button.place(  x=x, y=y+30, width=w, height=h, anchor=a)
		replay_button.place(x=x, y=y+60, width=w, height=h, anchor=a)




	def state_game_over(self, dt) :
		# nothing to do on game over
		pass



	def add_score(self, n) :
		self.current_score += n

		# also update the text
		self.canvas.itemconfig(
			self.score_text, 
			text=f"score: {self.current_score:06d}"
		)


	def load_scores(self) :
		try :
			with open(Game.scores_file_name, 'r') as fp :
				scores = eval(fp.read())

		# ignore if the file hasn't been created yet,
		# or if it's corrupted (python couldn't parse it)
		except (FileNotFoundError, SyntaxError) :
			scores = {}

		finally :
			return scores


	def save_scores(self, scores, player="PLAYER") :

		# the scores are stored in python dictionary string format
		scores_str = str(scores)  

		with open(Game.scores_file_name, "w") as fp :
			fp.write(scores_str)


