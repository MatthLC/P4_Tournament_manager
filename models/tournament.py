import datetime

class Tournament():
	def __init__(
		self,
		name,
		localisation,
		time_control,
		description,
		number_of_rounds,
		current_round,
		player_list,
		tournament_started,
		tournament_finished,
		round_list,
		current_matches,
		matches_done,
		matches_status,
		winner,
		match_played_by_player,
		score
	):
		self.name = name
		self.localisation = localisation
		self.time_control = time_control
		self.description = description
		self.number_of_rounds = number_of_rounds
		self.current_round = current_round
		self.player_list = player_list
		self.tournament_started = tournament_started
		self.tournament_finished = tournament_finished
		self.round_list = round_list
		self.current_matches = current_matches
		self.matches_done = matches_done
		self.matches_status = matches_status
		self.winner = winner
		self.match_played_by_player = match_played_by_player
		self.score = score

	def init_match_played_by_player(self):
		for player in self.player_list:
			self.match_played_by_player[int(player)] = []

	def init_score(self):
		for player in self.player_list:
			self.score[player] = [0]

	def add_player(self, players):
		self.player_list.append(players)

	def close(self):
		self.tournament_finished = str(datetime.datetime.now())

	def delete_player(self, players):
		self.players = players
		i = 0
		for item in self.players:
			del self.player_list[int(item) - 1 - i]
			i += 1

	def clear_round(self):
		self.current_matches.clear()
		self.matches_done.clear()
		self.matches_status.clear()
		self.winner.clear()

	def apply_score(self, match, result_player1, result_player2, selected_match, display_winner):
		self.match = match
		self.result_player1 = result_player1
		self.result_player2 = result_player2
		self.selected_match = selected_match
		self.display_winner = display_winner
		
		self.matches_done.append((
			[self.match[0], self.result_player1],
			[self.match[1], self.result_player2]
		))
		
		self.matches_status[self.selected_match] = 'Terminé'
		self.winner[self.selected_match] = self.display_winner
		self.match_played_by_player[self.match[0]].append(self.match[1])
		self.match_played_by_player[self.match[1]].append(self.match[0])
		self.score[self.match[0]][0] += self.result_player1
		self.score[self.match[1]][0] += self.result_player2
		