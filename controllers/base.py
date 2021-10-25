from controllers.actor import ActorController
from controllers.tournament import TournamentController
from controllers.reporting import ReportingController
from controllers.menu_actor import MenuController, EXECUTE_MAIN_MENU
from controllers.menu_reporting import MenuReportingController, EXECUTE_REPORTING_MENU
from controllers.menu_tournament_in_progress import MenuTournamentInProgressController, EXECUTE_TOURNAMENT_IN_PROGRESS_MENU

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

		self.tournament_controller = TournamentController(
			actors_database = self.actors_database,
			tournaments_database = self.tournaments_database,
			view = self.view,
			tournament = self.tournament,
			score_board = self.score_board
		)

		self.reporting_controller = ReportingController(
			actors_database = self.actors_database,
			tournaments_database = self.tournaments_database,
			tournament = self.tournament_controller.tournament,
			view = self.view
		)

		self.menu_actor_controller = MenuController(
			actors_database = self.actors_database,
			tournaments_database = self.tournaments_database,
			tournament = self.tournament_controller.tournament,
			view = self.view,
			actor_controller = self.actor_controller,
			tournament_controller = self.tournament_controller,
			reporting_controller = self.reporting_controller
		)

		self.menu_reporting_controller = MenuReportingController(
			actors_database = self.actors_database,
			tournaments_database = self.tournaments_database,
			tournament = self.tournament_controller.tournament,
			view = self.view,
			actor_controller = self.actor_controller,
			tournament_controller = self.tournament_controller,
			reporting_controller = self.reporting_controller
		)

		self.menu_tournament_in_progress_controller = MenuTournamentInProgressController(
			actors_database = self.actors_database,
			tournaments_database = self.tournaments_database,
			tournament = self.tournament_controller.tournament,
			view = self.view,
			actor_controller = self.actor_controller,
			tournament_controller = self.tournament_controller,
			reporting_controller = self.reporting_controller
		)

	def refresh_controller(self):
		self.menu_actor_controller.tournament = self.tournament_controller.tournament
		self.reporting_controller.tournament = self.tournament_controller.tournament
		self.menu_reporting_controller.tournament = self.tournament_controller.tournament
		self.menu_tournament_in_progress_controller.tournament = self.tournament_controller.tournament
	
	def run(self):
		self.view.prompt_clear()

		while True:
			self.refresh_controller()
			user_choice = self.view.prompt_for_menu(MENU)
			self.view.prompt_clear()

			#Main MENU
			#Participants
			if user_choice == '1':
				actor_menu = True

				while actor_menu:
					self.refresh_controller()
					user_choice_actor_menu = self.view.prompt_for_menu(ACTOR_MENU)
					self.view.prompt_clear()
					self.menu_actor_controller.execute_menu(EXECUTE_MAIN_MENU, user_choice_actor_menu)

					if user_choice_actor_menu == '999':
						actor_menu = False

			#Tournois
			elif user_choice == '2':

				while True:
					self.refresh_controller()
					user_choice_tournament_menu = self.view.prompt_for_menu(TOURNAMENT_MENU)
					self.view.prompt_clear()
					
					if user_choice_tournament_menu == '1':
						self.tournament_controller.show_all_tournament()

					elif user_choice_tournament_menu == '2':
						self.tournament_controller.create_tournament()
					
					elif user_choice_tournament_menu == '3':
						self.tournament_controller.show_all_tournament()
						tournament_to_load = self.view.prompt_for_tournament_load(len(self.tournaments_database.table_all))
						self.tournament_controller.load_tournament(tournament_to_load)
						
						tournament_in_progress_menu = True

						while tournament_in_progress_menu:
							self.refresh_controller()
							
							self.tournament_controller.save_tournament()
							if len(self.tournament_controller.tournament.player_list) < 2 :
								user_choice_tournament_in_progress_menu = self.view.prompt_for_menu(
									menu = TOURNAMENT_IN_PROGRESS_MENU,
									part_of_menu = ['1','2','3','4','10','999']
								)
							else:
								user_choice_tournament_in_progress_menu = self.view.prompt_for_menu(
									TOURNAMENT_IN_PROGRESS_MENU
								)

							self.view.prompt_clear()
							self.menu_tournament_in_progress_controller.execute_menu(
								EXECUTE_TOURNAMENT_IN_PROGRESS_MENU,
								user_choice_tournament_in_progress_menu
							)
							
							if user_choice_tournament_in_progress_menu == '999':
								tournament_in_progress_menu = False
								tournament_menu = False

					elif user_choice_tournament_menu == '999':
						break
					
					else:
						print('Saisie incorrecte.')
					
			#Reporting
			elif user_choice == '3':
				
				reporting_menu = True

				while reporting_menu:
					self.refresh_controller()
					user_choice_reporting_menu = self.view.prompt_for_menu(REPORTING_MENU)
					self.view.prompt_clear()

					self.menu_reporting_controller.execute_menu(EXECUTE_REPORTING_MENU, user_choice_reporting_menu)

					if user_choice_reporting_menu == '999':
						reporting_menu = False
			
			elif user_choice == '999':
				break
			else:
				print('Saisie incorrecte.')
