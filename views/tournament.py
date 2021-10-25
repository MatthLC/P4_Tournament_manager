import datetime

MODIFY_TOURNAMENT = {
    '1': '1. Nom du tournoi',
    '2': '2. Lieu du tournoi',
    '3': '3. Description du tournoi',
    '4': '4. Nombre de tours'
}


class TournamentView:
    def __init__(self):
        self.name = input('Saisir le nom du tournoi : ')
        self.localisation = input('Saisir le lieu : ')
        self.description = input('Description du tournoi : ')

        while True:
            print('Choisir le controle du temps :')
            print('1. Bullet ')
            print('2. Blitz')
            print('3. coup rapide')
            self.time_control = int(input('Choisir le controle du temps :'))

            if self.time_control in range(1, 4):
                break

        self.number_of_rounds = 4
        self.current_round = 0
        self.round_list = {}
        self.player_list = []
        self.tournament_started = str(datetime.datetime.now())
        self.tournament_finished = None
        self.current_matches = []
        self.matches_status = []
        self.matches_done = []
        self.winner_list = {}
        self.winner = []
        self.match_played_by_player = {}
        self.score = {}


class TournamentOverview:
    def overview(self, tournament):
        self.tournament = tournament
        print('Tournoi          : ' + str(self.tournament.name))
        print('Début du tournoi : ' + str(self.tournament.tournament_started))
        print('Fin du tournoi   : ' + str(self.tournament.tournament_finished))
        print('Lieu             : ' + str(self.tournament.localisation))
        print('Description      : ' + str(self.tournament.description))
        print('Nombre de joueur : ' + str(len(self.tournament.player_list)))
        print('Nombre de tour   : ' + str(self.tournament.number_of_rounds))
        print('Tour en cours    : ' + str(self.tournament.current_round))

    def modify(self):
        for item, value in MODIFY_TOURNAMENT.items():
            print(value)

        user_choice = input('Que souhaitez-vous modifier ? : ')
        user_value = input(f'[{MODIFY_TOURNAMENT[user_choice]}] : ')
        value_to_modify = [user_choice, user_value]

        return value_to_modify
