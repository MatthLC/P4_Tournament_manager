from models.database import TOURNAMENT_KEEP

class ReportingController:
	def __init__(self, actors_database, tournaments_database, tournament, view):
		self.actors_database = actors_database
		self.tournaments_database = tournaments_database
		self.tournament = tournament
		self.view = view

	def list_all_actors(self, sort_by):
		self.sort_by = sort_by
		print(self.actors_database.show(keep = None, id_list = [], sort_list = [self.sort_by]))

	def list_all_tournaments(self, sort_by):
		self.sort_by = sort_by
		print(self.tournaments_database.show(keep = TOURNAMENT_KEEP, id_list = [], sort_list = [self.sort_by]))

	def display_all_player_from_tournament(self, tournament_player_list, sort_by):
		self.tournament_player_list = tournament_player_list
		self.sort_by = sort_by
		print(self.actors_database.show(keep = None, id_list = self.tournament_player_list, sort_list = [self.sort_by]))

	def display_all_round(self):
		for key_round, matches in self.tournament.round_list.items():
			self.view.display_rounds(
				matches = matches,
				current_round = key_round,
				view = self.actors_database,
				winner = self.tournament.winner_list[key_round]
			)
		
		