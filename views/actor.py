class ActorView:
	def __init__(self):
		#identity of actor
		self.first_name = input ('Saisir le prénom du joueur : ')
		self.last_name = input ('Saisir le nom de famille du joueur : ')

		#Sex of actor
		check_sex = False
		while check_sex == False:
			self.sex = input('Saisir le sexe H/F : ').upper()
			if self.sex in ['H','F']:
				check_sex = True
			else:
				print('Veuillez choisir entre H ou F.')

		#Birthday of actor
		check_date = False
		while check_date == False:
			self.birthday = input ('Saisir la date de naissance au format DD/MM/YY : ')

			if len(self.birthday) > 7 and self.birthday.count('/') == 2:
				try:
					if (int(self.birthday[0:2]) in range(0,32) and 
						self.birthday[2] == "/" and
						int(self.birthday[3:5]) in range(0,13) and 
						self.birthday[5] == "/"	and
						int(self.birthday[6:8]) in range(0,100)):
						check_date = True
				except ValueError:
					print('Date invalide.')
			else:
				print('Veuillez respecter le format de la date.')
		
		#Ranking of actor
		check_ranking = False
		while check_ranking == False:
			try:
				self.ranking = int(input ('Saisir le classement du joueur : '))
				check_ranking = True
			except ValueError:
				print('Veuillez saisir un nombre.')
	
class ModifyRanking:
	def new_ranking(self):
		id_rank = []

		id_selected = input('Sélectionnez un participant : ')
		ranking = input('Saisir le nouveau classement :  ')

		id_rank.append(id_selected)
		id_rank.append(ranking)

		return id_rank



	
