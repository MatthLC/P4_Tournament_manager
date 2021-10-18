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
	'4' : 'Modifier un tournoi',
	'999' : 'Menu principal'
}

TOURNAMENT_IN_PROGRESS_MENU = {
	'1' : 'Résumé du tournoi',
	'2' : 'Afficher la liste des joueurs',
	'3' : 'Ajouter un joueur',
	'4' : 'Supprimer un joueur',
	'5' : 'Afficher le round en cours',
	'6' : 'Round suivant',
	'7' : "Saisir le résultat d'un match",
	'8' : 'Reporting',
	'9' : 'Cloturer le tournoi',
	'10' : 'Modifier le tournoi',
	'999' : 'Menu principal'
}


class MenuView:
	
	def header(self):
		print('---------------------------------------------------')
		print('               Tournament Manager                  ')
		print('---------------------------------------------------')
		print('\n')

	def print_menu(self, menu):
		self.menu = menu
		for key, menu_text in self.menu.items():
			print(key + ". " + menu_text)

	def prompt_for_menu(self, menu):
		self.menu = menu
		print('\n')
		print(" --------------------------------------------------")
		print("|Veuillez saisir un choix :                        |")
		print(" --------------------------------------------------")
		self.print_menu(self.menu)
		print(" --------------------------------------------------")
		return input("Votre choix : ")

	def prompt_for_menu_tournament(self, name):
		self.name = name
		print(" --------------------------------------------------")
		print("                Tournoi : " + self.name + "        ")
		print(" --------------------------------------------------")
		self.print_menu(TOURNAMENT_MENU)
		print(" --------------------------------------------------")
		return input('[Tournoi ' + self.name + '] Votre choix : ')

	def prompt_for_tournament_load(self):
		return input('Quel tournoi voulez-vous reprendre ? : ')

	def prompt_select_tournament_player(self, name):
		self.name = name
		return input('[Tournoi ' + self.name + '] Sélectionner les joueurs : ')

	


