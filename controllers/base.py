import datetime

from controllers.actor import ActorController
from controllers.tournament import TournamentController
from controllers.reporting import ReportingController

from models.tournament import Tournament

from views.menu import MENU, ACTOR_MENU, TOURNAMENT_MENU, TOURNAMENT_IN_PROGRESS_MENU, REPORTING_MENU
from views.base import View


class Controller:
	def __init__(self, actors_database, tournaments_database, view):
		self.view = view
		self.actors_database = actors_database
		self.tournaments_database = tournaments_database
		self.tournament = ''
		self.actor_list = []
		self.score_board = {
			'1' : [1.0, 0.0],
			'2' : [0.0, 1.0],
			'3' : [0.5, 0.5]
		}	
		self.actor_controller = ActorController(
			actors_database = self.actors_database,
			tournaments_database = self.tournaments_database,
			view = self.view
		)

	def refresh_reporting_controller(self):
		self.reporting_controller = ReportingController(
			actors_database = self.actors_database,
			tournaments_database = self.tournaments_database,
			tournament = self.tournament,
			view = self.view
		)

	def refresh_tournament_controller(self):
		self.tournament_controller = TournamentController(
			actors_database = self.actors_database,
			tournaments_database = self.tournaments_database,
			view = self.view,
			tournament = self.tournament,
			score_board = self.score_board
		)
		
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
			winner_list = tournament_to_load['winner_list'],
			winner = tournament_to_load['winner'],
			match_played_by_player = tournament_to_load['match_played_by_player'],
			score = tournament_to_load['score']
		)
		
		self.refresh_tournament_controller()
		self.refresh_reporting_controller()

	def load_tournament_for_reporting(self):
		self.tournament_controller.show_all_tournament()
		tournament_to_display = self.view.prompt_for_tournament_to_display()
		self.load_tournament(tournament_to_display)

	def run(self):
		running = True
		self.view.prompt_clear()

		while running:
			self.refresh_tournament_controller()
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
						self.actor_controller.show_all_actor()

					elif user_choice_actor_menu == '2':
						self.actor_controller.add_actor()
						self.view.prompt_clear()

					elif user_choice_actor_menu == '3':
						self.actor_controller.show_all_actor()
						user_choice = self.view.prompt_new_ranking(top_rank = len(self.actors_database.table_all))
						self.actor_controller.modify_actor(user_choice)

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
						self.tournament_controller.show_all_tournament()

					elif user_choice_tournament_menu == '2':
						self.create_tournament()

					elif user_choice_tournament_menu == '3':
						self.tournament_controller.show_all_tournament()
						tournament_to_load = self.view.prompt_for_tournament_load()
						self.load_tournament(tournament_to_load)

						tournament_in_progress_menu = True

						while tournament_in_progress_menu:
							self.tournament_controller.save_tournament()
							if len(self.tournament.player_list) < 2 :
								user_choice_tournament_in_progress_menu = self.view.prompt_for_menu(
									menu = TOURNAMENT_IN_PROGRESS_MENU,
									part_of_menu = ['1','2','3','4','10','999']
								)
							else:
								user_choice_tournament_in_progress_menu = self.view.prompt_for_menu(
									TOURNAMENT_IN_PROGRESS_MENU
								)
							self.view.prompt_clear()

							if user_choice_tournament_in_progress_menu == '1':
								self.view.display_tournament_overview(self.tournament)

							elif user_choice_tournament_in_progress_menu == '2':
								self.tournament_controller.show_tournament_player()
								
							elif user_choice_tournament_in_progress_menu == '3':
								self.actor_controller.show_all_actor()
								self.selected_players = self.view.prompt_select_tournament_player(self.tournament.name).split()
								self.tournament_controller.add_player_to_tournament(self.selected_players)
								self.view.prompt_clear()
								self.tournament_controller.show_tournament_player()

							elif user_choice_tournament_in_progress_menu == '4':
								self.tournament_controller.show_tournament_player()
								self.selected_players = self.view.prompt_select_tournament_player(self.tournament.name).split()
								self.tournament_controller.delete_players_from_tournament(self.selected_players)
								self.view.prompt_clear()
								self.tournament_controller.show_tournament_player()

							
							elif user_choice_tournament_in_progress_menu == '5':
								if len(self.tournament.player_list) > 1 :
									self.tournament_controller.show_current_round()
								else:
									pass

							elif user_choice_tournament_in_progress_menu == '6':
								if len(self.tournament.player_list) > 1 :
									if (len(self.tournament.current_matches) ==(
										len(self.tournament.matches_done)) or
										self.tournament.current_round == 0 and 
										self.tournament.current_round < self.tournament.number_of_rounds
									):
										self.tournament_controller.next_round()
										self.tournament_controller.show_current_round()
										self.tournament_controller.save_tournament()

									if (len(self.tournament.current_matches) ==
										(len(self.tournament.matches_done)) and
										self.tournament.current_round == self.tournament.number_of_rounds
									):
										print('\nLe nombre maximum de tour est déja atteint.\n')

									if len(self.tournament.current_matches) != len(self.tournament.matches_done):
										print("Le round en cours n'est pas terminé.\n")
								else:
									pass

							elif user_choice_tournament_in_progress_menu == '7':
								self.tournament_controller.show_current_round()
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
								self.tournament_controller.set_score(selected_match = match_selected, result = result)
								self.tournament_controller.save_tournament()
								self.view.prompt_clear()
								self.tournament_controller.show_current_round()

							elif user_choice_tournament_in_progress_menu == '8':
								pass

							elif user_choice_tournament_in_progress_menu == '9':
								self.tournament_controller.close_tournament()

							elif user_choice_tournament_in_progress_menu == '10':
								user_choice = self.view.prompt_modify_tournament()
								if user_choice[0] == '1':
									pass
								if user_choice[0] == '2':
									pass
								if user_choice[0] == '3':
									self.tournament.description = user_choice[1]


							elif user_choice_tournament_in_progress_menu == '999':
								tournament_in_progress_menu = False
								tournament_menu = False

							else:
								print('Saisie incorrecte.')

					elif user_choice_tournament_menu == '999':
						tournament_menu = False
						
					else:
						print('Saisie incorrecte.')
			#Reporting
			elif user_choice == '3':
				
				reporting_menu = True

				while reporting_menu:

					user_choice_reporting_menu = self.view.prompt_for_menu(REPORTING_MENU)
					self.view.prompt_clear()

					if user_choice_reporting_menu == '1':
						self.reporting_controller.list_all_actors('first_name')

					elif user_choice_reporting_menu == '2':
						self.reporting_controller.list_all_actors('ranking')

					elif user_choice_reporting_menu == '3':
						self.reporting_controller.list_all_tournaments('name')

					elif user_choice_reporting_menu == '4':
						self.load_tournament_for_reporting()
						self.reporting_controller.display_all_player_from_tournament(
							tournament_player_list = self.tournament.player_list,
							sort_by = 'first_name'
						)

					elif user_choice_reporting_menu == '5':
						self.load_tournament_for_reporting()
						self.reporting_controller.display_all_player_from_tournament(
							tournament_player_list = self.tournament.player_list,
							sort_by = 'ranking'
						)

					elif user_choice_reporting_menu == '6':
						self.load_tournament_for_reporting()
						self.reporting_controller.display_all_round()
						
					elif user_choice_reporting_menu == '999':
						reporting_menu = False

					else:
						print('saisie incorrete.')
			
			elif user_choice == '999':
				running = False

			else:
				print('Saisie incorrecte.')
