from views.menu import MENU, ACTOR_MENU, TOURNAMENT_MENU, TOURNAMENT_IN_PROGRESS_MENU, REPORTING_MENU

EXECUTE_MAIN_MENU = {
	'1' : 'display_actors',
	'2' : 'add_actor',
	'3' : 'set_new_rank',
	'999' : 'back_to_main_menu'
}

class MenuController:
	def __init__(self, actors_database, tournaments_database, view, tournament, actor_controller, tournament_controller, reporting_controller):
		self.actors_database = actors_database
		self.tournaments_database = tournaments_database
		self.tournament = tournament
		self.view = view
		self.actor_controller = actor_controller
		self.tournament_controller = tournament_controller
		self.reporting_controller = reporting_controller

	def execute_menu(self, menu, argument):
		self.menu = menu
		self.argument = argument
		try:
			method_name = self.menu.get(self.argument, lambda: print('Saisie incorrecte.'))
			method_to_call = getattr(self, method_name, lambda: print('Saisie incorrecte.'))
			return method_to_call()
		except TypeError:
			print('Saisie incorrecte.')

	#Actors Menu
	"""Display all actors registered"""
	def display_actors(self):
		self.actor_controller.show_all_actor()

	"""Add actor to the tournament manager"""
	def add_actor(self):
		self.actor_controller.add_actor()
		self.view.prompt_clear()

	"""Update actor's Rank"""
	def set_new_rank(self):
		self.actor_controller.show_all_actor()
		user_choice = self.view.prompt_new_ranking(top_rank = len(self.actors_database.table_all))
		self.actor_controller.modify_actor(user_choice)

	def back_to_main_menu(self):
		pass
		
	



	