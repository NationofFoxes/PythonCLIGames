class Game:
	# required parameters

	# player number options
	available_player_num = [2]  # REQUIRED FOR ALL GAMES

	# parameters unique to this game

	n = 9
	cells = {
		"A": " ",
		"B": " ",
		"C": " ",
		"D": " ",
		"E": " ",
		"F": " ",
		"G": " ",
		"H": " ",
		"I": " ",
	}
	player_options = "XO"

	# required methods

	def __init__(self, state, users):  # REQUIRED FOR ALL GAMES
		if state["is_started"] == "true":  # REQUIRED FOR ALL GAMES
			self.state_to_obj(state)  # REQUIRED FOR ALL GAMES

	def initialize(self, users):  # REQUIRED FOR ALL GAMES
		# setup game object
		self.players = []
		for i, user in enumerate(users):
			symbol = self.player_options[i]
			self.players += [{"symbol": symbol, "id": user.user_id}]

		self.current_player = self.players[0]

		# get display and state from object
		display = self.obj_to_display()  # REQUIRED FOR ALL GAMES
		state = self.obj_to_state()  # REQUIRED FOR ALL GAMES
		return display, state  # REQUIRED FOR ALL GAMES

	def state_to_obj(self, state):  # REQUIRED FOR ALL GAMES
		self.cells = state["cells"]
		self.players = state["players"]
		self.current_player = state["current_player"]
		return

	def is_valid_move(self, my_move):  # REQUIRED FOR ALL GAMES
		spot = my_move.upper()
		is_valid = spot in self.cells.keys() and self.cells[spot] == " "
		return is_valid  # REQUIRED FOR ALL GAMES

	def move(self, my_move):  # REQUIRED FOR ALL GAMES
		# make move
		spot = my_move.upper()
		self.cells[spot] = self.current_player["symbol"]

		# get display and state from object
		new_display = self.obj_to_display()  # REQUIRED FOR ALL GAMES
		new_state = self.obj_to_state()  # REQUIRED FOR ALL GAMES
		return new_display, new_state  # REQUIRED FOR ALL GAMES

	def obj_to_display(self):  # REQUIRED FOR ALL GAMES
		display = "\n\nSPOT NAMES   GAME BOARD\n\n"
		left = ""
		right = "    "
		for i, spot in enumerate(self.cells.keys()):
			left += spot + " "
			right += self.cells[spot] + " "
			if (i + 1) % 3:
				left += "| "
				right += "| "
			elif i != self.n-1:
				display += left + right
				display += "\n---------     ---------\n"
				left = ""
				right = "    "
			else:
				display += left + right + "\n\n"
		return display  # REQUIRED FOR ALL GAMES

	def obj_to_state(self):  # REQUIRED FOR ALL GAMES
		for i, player in enumerate(self.players):
			if player["id"] == self.current_player["id"]:
				next_player_index = (i + 1) % len(self.players)
		next_player = self.players[next_player_index]

		state = {
			"cells": self.cells,
			"players": self.players,
			"current_player": next_player,
			"is_started": "true",
		}
		return state  # REQUIRED FOR ALL GAMES

	# methods unique to this game

