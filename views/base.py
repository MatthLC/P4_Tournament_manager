
from views.actor import ActorView, ModifyRanking
from views.tournament import TournamentView, TournamentOverview
from views.round import RoundView
from views.menu import MenuView
from views.match import MatchView

import os

class View:

	def display(self, result):
		self.result = result

		print('\n')
		print(self.result)
		print('\n')

	def prompt_clear(self):
		clearConsole = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')
		clearConsole()
		MenuView().header()

	def prompt_for_menu(self, menu):
		self.menu = menu
		return MenuView().prompt_for_menu(self.menu)

	def prompt_for_menu_tournament(self, name):
		self.name = name
		return MenuView().prompt_for_menu_tournament(self.name)

	def prompt_for_tournament_load(self):
		return MenuView().prompt_for_tournament_load()

	def	prompt_select_tournament_player(self,name):
		self.name = name
		return MenuView().prompt_select_tournament_player(self.name)

	def prompt_for_actor(self):
		return ActorView()

	def prompt_new_ranking(self):
		return ModifyRanking().new_ranking()

	def prompt_modify_tournament(self):
		return TournamentOverview().modify()

	def prompt_for_tournament(self):
		return TournamentView()

	def display_tournament_overview(self, tournament):
		self.tournament = tournament
		TournamentOverview().overview(self.tournament)

	def display_rounds(self, matches, matches_status, current_round, view, winner):
		self.matches = matches
		self.matches_status = matches_status
		self.current_round = current_round
		self.view = view
		self.winner = winner

		RoundView().show_current_round(self.matches, self.matches_status, self.current_round, self.view, self.winner)

	def prompt_to_select_match(self):
		return input("Sélectionnez un match : ")

	def promp_to_set_score(self, matches, current_round, view, match_selected):
		self.matches = matches
		self.current_round= current_round
		self.view = view
		self.match_selected = match_selected

		return MatchView().set_score(self.matches, self.current_round, self.view, self.match_selected)
