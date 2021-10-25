MENU = {
	'1' : 'Participants',
	'2' : 'Tournois',
	'3' : 'reporting',
	'999' : 'Quitter'
}

ACTOR_MENU = {
	'1' : 'Afficher la liste des participants',
	'2' : 'Ajouter un participant',
	'3' : 'Mettre à jour le classement',
	'999' : 'Menu principal'
}

TOURNAMENT_MENU = {
	'1' : 'Afficher la liste des tournois',
	'2' : 'Créer un tournoi',
	'3' : 'Continuer un tournoi en cours',
	'999' : 'Menu principal'
}

TOURNAMENT_IN_PROGRESS_MENU = {
	'1' : 'Résumé du tournoi',
	'2' : 'Afficher la liste des joueurs',
	'3' : 'Ajouter un joueur',
	'4' : 'Supprimer un joueur',
}

TOURNAMENT_IN_PROGRESS_MENU = {
	'1' : 'Résumé du tournoi',
	'2' : 'Afficher la liste des joueurs',
	'3' : 'Ajouter un joueur',
	'4' : 'Supprimer un joueur',
	'5' : 'Afficher le round en cours',
	'6' : 'Round suivant',
	'7' : "Saisir le résultat d'un match",
	'8' : 'Classement du tournoi',
	'9' : 'Cloturer le tournoi',
	'10' : 'Modifier le tournoi',
	'999' : 'Menu principal'
}

REPORTING_MENU = {
	'1' : 'Liste des participants par ordre alphabétique',
	'2' : 'Liste des participants par classement',
	'3' : 'Liste de tous les tournois',
	'4' : "Liste des joueurs d'un tournoi par ordre alphabétique",
	'5' : "Liste des joueurs d'un tournoi par classement",
	'6' : "liste de tous les tours / matchs d'un tournoi",
	'7' : "Afficher le classement d'un tournoi",
	'999' : 'Menu principal'
}


class MenuView:
	
	def header(self):
		print('---------------------------------------------------')
		print('               Tournament Manager                  ')
		print('---------------------------------------------------')
		print('\n')

	def print_menu(self, menu, part_of_menu=[]):
		self.menu = menu
		self.part_of_menu = part_of_menu
		if self.part_of_menu == []:
			self.part_of_menu = self.menu.keys()

		for key, menu_text in self.menu.items():
			if key in self.part_of_menu:
				print(key + ". " + menu_text)

	def prompt_for_menu(self, menu, part_of_menu):
		self.menu = menu
		self.part_of_menu = part_of_menu
		print('\n')
		print(" --------------------------------------------------")
		print("|Veuillez saisir un choix :                        |")
		print(" --------------------------------------------------")
		self.print_menu(menu = self.menu, part_of_menu = self.part_of_menu)
		print(" --------------------------------------------------")
		return input("Votre choix : ")

	def prompt_for_menu_tournament(self, name):
		self.name = name
		print(" --------------------------------------------------")
		print("                Tournoi : " + self.name + "        ")
		print(" --------------------------------------------------")
		self.print_menu(menu = TOURNAMENT_MENU)
		print(" --------------------------------------------------")
		return input('[Tournoi ' + self.name + '] Votre choix : ')

	def prompt_to_select(self, max_number):
		self.max_number = max_number
		check_value = False
		while check_value == False:
			user_choice = input('Faites votre choix : ')
			try:
				if int(user_choice) in range(1, int(self.max_number) + 1):
					check_value = True
				else:
					print('Saisir un nombre entre 1 et ' + str(self.max_number))
			except ValueError:
				print('Saisie incorrecte.')
		return user_choice


