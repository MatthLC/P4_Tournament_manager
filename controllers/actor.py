class ActorController:
	def __init__(
		self,
		actors_database,
		tournaments_database,
		view
	):
		self.actors_database = actors_database
		self.tournaments_database = tournaments_database
		self.view = view
	
	def show_all_actor(self):
		self.view.display(self.actors_database.show())

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

	def modify_actor(self):
			self.show_all_actor()
			user_choice = self.view.prompt_new_ranking()
			new_rank = {'ranking': int(user_choice[1])}
			self.actors_database.modify_db(dictionnary = new_rank , id_list = user_choice[0])
			self.view.prompt_clear()
			self.show_all_actor()