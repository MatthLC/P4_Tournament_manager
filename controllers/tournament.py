from models.database import Database, ACTOR_FORMAT, TOURNAMENT_KEEP
from models.swisssystem import SwissSystem


class TournamentController:
	def __init__(
		self,
		actors_database,
		tournaments_database,
		view,
		tournament,
		score_board
	):
		self.actors_database = actors_database
		self.tournaments_database = tournaments_database
		self.view = view
		self.tournament = tournament
		self.score_board = score_board

	def show_all_tournament(self):
		show = self.tournaments_database.show(keep = TOURNAMENT_KEEP)
		self.view.display(show)

	def show_tournament_player(self):
		if self.tournament.player_list == []:
			print("Il n'y a pas de joueur pour le moment")
		else:
			print('\n Liste des participants du tournoi ' + self.tournament.name + ' : \n')
			show = self.actors_database.show(keep = None, id_list = self.tournament.player_list)
			self.view.display(show)

	def save_tournament(self):
		self.tournaments_database.update_db(self.tournament)

	def close_tournament(self):
		self.tournament.close()
		self.save_tournament()

	def add_player_to_tournament(self, players):
		self.players = players
		for item in self.players:
			player = self.actors_database.load(item)
			self.tournament.add_player(player.doc_id)
			self.save_tournament()

	def delete_player_from_tournament(self, players):
		self.players = players
		self.tournament.delete_player(self.players)
		self.save_tournament()

	def next_round(self):
		self.tournament.clear_round()
		self.tournament.current_round += 1
		self.round_system()
		

	def show_current_round(self):
		if self.tournament.current_round == 0:
			print("Il n'y a pas de round pour le moment.")
		else:
			self.view.display_rounds(
				matches = self.tournament.current_matches,
				matches_status = self.tournament.matches_status,
				current_round = self.tournament.current_round,
				view = self.actors_database,
				winner = self.tournament.winner
			)

	def round_system(self):
		if self.tournament.current_round == 1:
			self.tournament.current_matches = SwissSystem().first_round(
				self.actors_database.sort_by(
					item_list = self.tournament.player_list,
					sort_list = ['ranking']
				)
			)

			self.tournament.init_match_played_by_player()
			self.tournament.init_score()
			
		if self.tournament.current_round > 1:
			show = self.actors_database.show(keep = ['ranking'], id_list = self.tournament.player_list)
			show = list(show.to_dict().values())[0]
			
			self.tournament.current_matches = SwissSystem().other_round(
				score = self.tournament.score,
				ranking = show,
				match_played_by_player = self.tournament.match_played_by_player
			)


		for item in range(0,len(self.tournament.current_matches)):
			self.tournament.matches_status.append('En cours')
			self.tournament.winner.append('Match non terminé')

	def set_score(self, selected_match, result):
		self.selected_match = int(selected_match) - 1
		self.result = result
		self.result_player1 = self.score_board[self.result][0]
		self.result_player2 = self.score_board[self.result][1]
		self.display_winner = ''
		self.match = self.tournament.current_matches[self.selected_match]

		if result != '3':
			last_name = self.actors_database.matable_df.loc[self.match[int(self.result) - 1]].first_name
			first_name = self.actors_database.matable_df.loc[self.match[int(self.result) - 1]].last_name
			self.display_winner = first_name + ' ' + last_name

		if result == '3':
			self.display_winner = 'Egalité'

		self.tournament.apply_score(
			self.match,
			self.result_player1,
			self.result_player2,
			self.selected_match,
			self.display_winner
		)