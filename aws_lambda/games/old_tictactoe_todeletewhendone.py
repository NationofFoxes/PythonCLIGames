import random


class Game:
	#n = 9
	#cells = {
	#	'A': ' ',
	#	'B': ' ',
	#	'C': ' ',
	#	'D': ' ',
	#	'E': ' ',
	#	'F': ' ',
	#	'G': ' ',
	#	'H': ' ',
	#	'I': ' ',
	#}
	lineups = ['ABC', 'DEF', 'GHI', 'ADG', 'BEH', 'CFI', 'AEI', 'CEG']
	players = 'XO'
	player = True
	num_players = 2
	move_num = 1


	@property
	def is_game_over(self):
		for lineup in self.lineups:
			if (
				self.cells[lineup[0]] != ' ' and
				self.cells[lineup[0]] == self.cells[lineup[1]] and
				self.cells[lineup[1]] == self.cells[lineup[2]]
			):
				return True
		return False

	def switch_players(self):
		self.player = not self.player

	def play(self):

		while not self.is_game_over:
			to_print += self
			if self.num_players == 2 or int(self.player) == players_order:
				spot = input(f'PLAYER {self.player_symbol}\'s TURN. ENTER SPOT A-I: ').upper()
			else:
				spot = self.npc_move()
			if self.is_valid(spot):
				self.make_move(spot)
				self.switch_players()
				self.move_num += 1
			else:
				to_print += '\n\nINVALID MOVE!')

		self.switch_players()
		print(self, end='')
		print(f'GAME OVER\n{self.player_symbol} WINS!')
