class ActorView:
    def __init__(self, top_rank):
        # identity of actor
        self.first_name = input('Saisir le prénom du joueur : ')
        self.last_name = input('Saisir le nom de famille du joueur : ')

        # Sex of actor
        while True:
            self.sex = input('Saisir le sexe H/F : ').upper()
            if self.sex in ['H', 'F']:
                break
            else:
                print('Veuillez choisir entre H ou F.')

        # Birthday of actor
        """
        check_date = False
        while check_date == False:
        """
        while True:
            self.birthday = input('Saisir la date de naissance au format DD/MM/YY : ')

            if len(self.birthday) > 7 and self.birthday.count('/') == 2:
                try:
                    if (
                        int(self.birthday[0: 2]) in range(0, 32) and
                        self.birthday[2] == "/" and
                        int(self.birthday[3: 5]) in range(0, 13) and
                        self.birthday[5] == "/" and
                        int(self.birthday[6: 8]) in range(0, 100)
                    ):
                        break
                except ValueError:
                    print('Date invalide.')
            else:
                print('Veuillez respecter le format de la date.')

        # Ranking of actor
        self.ranking = int(top_rank) + 1


class ModifyRanking:
    def new_ranking(self, top_rank):
        self.top_rank = int(top_rank)
        id_rank = []

        while True:
            id_selected = input('Sélectionnez un participant : ')
            try:
                if int(id_selected) in range(1, self.top_rank + 1):
                    break
            except ValueError:
                print('Veuillez saisir un nombre compris entre 1 et ' + str(self.top_rank))

        print('Classement maximum : ' + str(self.top_rank))

        while True:
            ranking = input('Saisir le nouveau classement :  ')
            try:
                if int(ranking) in range(1, self.top_rank + 1):
                    break
            except ValueError:
                print('Veuillez saisir un nombre compris entre 1 et ' + str(self.top_rank))

        id_rank.append(id_selected)
        id_rank.append(ranking)

        return id_rank
