from models.tournament import Tournament
from models.database import Database, ACTOR_FORMAT, TOURNAMENT_KEEP
from models.swisssystem import SwissSystem
from views.menu import MENU, ACTOR_MENU, TOURNAMENT_MENU, TOURNAMENT_IN_PROGRESS_MENU
import datetime

from views.base import View


score_board = {
	'1' : [1.0, 0.0],
	'2' : [0.0, 1.0],
	'3' : [0.5, 0.5]
}

class Controller:
	def __init__(self, actors_database, tournaments_database, round_database, match_database, view):
		self.view = view
		self.actors_database = actors_database
		self.tournaments_database = tournaments_database
		self.tournament = ''
		self.actor_list = []

	def add_actor(self):
		check_actor = False
		while check_actor == False:
			actor_input = self.view.prompt_for_actor()
			verify_if_already_exist = self.actors_database.search_db(
				column1 = 'first_name',
				value1 = actor_input.first_name,
				column2 = 'last_name',
				value2 = actor_input.last_name
			)
			
			if len(verify_if_already_exist) == 0:
				print(verify_if_already_exist)
				self.actors_database.insert_db(actor_input)
				check_actor = True
			else:
				print('\nLe participant existe déjà!\n')

	def show_all_actor(self):
		self.view.display(self.actors_database.show())


	def modify_actor(self):
		pass
	# Tournaments

	def save_tournament(self):
		self.tournaments_database.update_db(self.tournament)

	def show_all_tournament(self):
		show = self.tournaments_database.show(keep = TOURNAMENT_KEEP)
		print('\n')
		print(show)
		print('\n')

	def create_tournament(self):
		check_tournament = True
		while check_tournament == True:
			tournament_input = self.view.prompt_for_tournament()
			verify_if_already_exist = self.tournaments_database.search_db(
				column1 = 'name',
				value1 = tournament_input.name,
			)

			if len(verify_if_already_exist) == 0:
				self.tournaments_database.insert_db(tournament_input)
				self.load_tournament(self.tournaments_database.db_table.get(doc_id=len(self.tournaments_database.db_table)).doc_id)
				check_tournament = False
			else:
				print('\nle tournoi existe déjà !\n')

	def load_tournament(self, tournament_id):
		self.tournament_id = tournament_id	
		tournament_to_load = self.tournaments_database.load(tournament_id)
		
		self.tournament = Tournament(
			name = tournament_to_load['name'],
			localisation = tournament_to_load['localisation'],
			time_control = tournament_to_load['time_control'],
			description = tournament_to_load['description'],
			number_of_rounds = tournament_to_load['number_of_rounds'],
			current_round = tournament_to_load['current_round'],
			player_list = tournament_to_load['player_list'],
			tournament_started = tournament_to_load['tournament_started'],
			tournament_finished = tournament_to_load['tournament_finished'],
			round_list = tournament_to_load['round_list'],
			current_matches = tournament_to_load['current_matches'],
			matches_done = tournament_to_load['matches_done'],
			matches_status = tournament_to_load['matches_status'],
			winner = tournament_to_load['winner'],
			match_played_by_player = tournament_to_load['match_played_by_player'],
			score = tournament_to_load['score']
		)
		
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

	def show_tournament_player(self):
		if self.tournament.player_list == []:
			print("Il n'y a pas de joueur pour le moment")
		else:
			print('\n Liste des participants du tournoi ' + self.tournament.name + ' : \n')
			show = self.actors_database.show(keep = None, id_list = self.tournament.player_list)
			print('\n')
			print(show)
			print('\n')

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
		self.result_player1 = score_board[self.result][0]
		self.result_player2 = score_board[self.result][1]
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

	def run(self):
		running = True
		self.view.prompt_clear()

		while running:
			user_choice = self.view.prompt_for_menu(MENU)
			self.view.prompt_clear()
			
			#Main MENU
			#Participants
			if user_choice == '1':
				actor_menu = True

				while actor_menu:

					user_choice_actor_menu = self.view.prompt_for_menu(ACTOR_MENU)
					self.view.prompt_clear()

					if user_choice_actor_menu == '1':
						self.show_all_actor()

					elif user_choice_actor_menu == '2':
						self.add_actor()
						self.view.prompt_clear()

					elif user_choice_actor_menu == '3':
						pass

					elif user_choice_actor_menu == '999':
						actor_menu = False

					else:
						print('Saisie incorrecte.')

			#Tournois
			if user_choice == '2':

				tournament_menu = True

				while tournament_menu:

					user_choice_tournament_menu = self.view.prompt_for_menu(TOURNAMENT_MENU)
					self.view.prompt_clear()

					if user_choice_tournament_menu == '1':
						self.show_all_tournament()

					elif user_choice_tournament_menu == '2':
						
						self.create_tournament()

					elif user_choice_tournament_menu == '3':
						self.show_all_tournament()
						tournament_to_load = self.view.prompt_for_tournament_load()
						self.load_tournament(tournament_to_load)

						tournament_in_progress_menu = True

						while tournament_in_progress_menu:
							user_choice_tournament_in_progress_menu = self.view.prompt_for_menu(TOURNAMENT_IN_PROGRESS_MENU)
							self.view.prompt_clear()

							if user_choice_tournament_in_progress_menu == '1':
								print(self.tournament.tournament_started)
								print(self.tournament.name)
								self.view.display_tournament_overview(self.tournament)

							elif user_choice_tournament_in_progress_menu == '2':
								self.show_tournament_player()
								
							elif user_choice_tournament_in_progress_menu == '3':
								self.show_all_actor()
								self.selected_players = self.view.prompt_select_tournament_player(self.tournament.name).split()
								self.add_player_to_tournament(self.selected_players)
								self.view.prompt_clear()
								self.show_tournament_player()

							elif user_choice_tournament_in_progress_menu == '4':
								self.show_tournament_player()
								self.selected_players = self.view.prompt_select_tournament_player(self.tournament.name).split()
								self.delete_player_from_tournament(self.selected_players)
								self.view.prompt_clear()
								self.show_tournament_player()

							elif user_choice_tournament_in_progress_menu == '5':
								self.show_current_round()

							elif user_choice_tournament_in_progress_menu == '6':
								if len(self.tournament.current_matches) == len(self.tournament.matches_done) or self.tournament.current_round == 0:
									self.next_round()
									self.show_current_round()
									self.save_tournament()

								elif self.tournament.current_round == self.tournament.number_of_rounds:
									print('\nLe nombre maximum de tour est déja atteint.\n')

								else:
									print("Le round en cours n'est pas terminé.\n")

							elif user_choice_tournament_in_progress_menu == '7':
								self.show_current_round()
								match_already_done = True
								while match_already_done:
									match_selected = self.view.prompt_to_select_match()
									if self.tournament.matches_status[int(match_selected)-1] == 'En cours':
										match_already_done = False
									else:
										print('\nCe match est déja terminé.\n')

								result = self.view.promp_to_set_score(
									self.tournament.current_matches,
									self.tournament.current_round,
									self.actors_database,
									match_selected
								)
								self.set_score(selected_match = match_selected, result = result)
								self.save_tournament()
								self.view.prompt_clear()
								self.show_current_round()

							elif user_choice_tournament_in_progress_menu == '8':
								pass

							elif user_choice_tournament_in_progress_menu == '9':
								pass

							elif user_choice_tournament_in_progress_menu == '10':
								self.close_tournament()

							elif user_choice_tournament_in_progress_menu == '999':
								tournament_in_progress_menu = False
								tournament_menu = False

							else:
								print('Saisie incorrecte.')

					elif user_choice_tournament_menu == '4':
						pass

					elif user_choice_tournament_menu == '999':
						tournament_menu = False
						
					else:
						print('Saisie incorrecte.')
			#Reporting
			elif user_choice == '3':
				pass
			
			elif user_choice == '999':
				running = False

			else:
				print('Saisie incorrecte.')
