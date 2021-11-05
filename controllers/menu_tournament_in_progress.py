EXECUTE_TOURNAMENT_IN_PROGRESS_MENU = {
    '1': 'tournament_summary',
    '2': 'display_tournament_players',
    '3': 'add_player_to_tournament',
    '4': 'delete_player_from_tournament',
    '5': 'display_current_round',
    '6': 'next_round',
    '7': 'enter_result_of_match',
    '8': 'ranking_of_tournament',
    '9': 'close_tournament',
    '10': 'update_tournament_information',
    '999': 'back_to_main_menu'
}


class MenuTournamentInProgressController:
    def __init__(
        self,
        actors_database,
        tournaments_database,
        view,
        tournament,
        actor_controller,
        tournament_controller,
        reporting_controller
    ):

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

    def back_to_main_menu(self):
        pass

    """Display summry of tournament"""
    def tournament_summary(self):
        self.view.display_tournament_overview(self.tournament)

    """ Display list of players for selected tournament"""
    def display_tournament_players(self):
        self.tournament_controller.show_tournament_player()

    """ add player to tournament from actor list """
    def add_player_to_tournament(self):
        self.actor_controller.show_all_actors()
        self.selected_players = self.view.prompt_select_tournament_player(len(self.actors_database.table_all)).split()
        self.tournament_controller.add_player_to_tournament(self.selected_players)
        self.view.prompt_clear()
        self.tournament_controller.show_tournament_player()

    """ delete a player from current tournament """
    def delete_player_from_tournament(self):
        self.tournament_controller.show_tournament_player()
        self.selected_players = self.view.prompt_select_tournament_player(len(self.tournament.player_list)).split()
        self.tournament_controller.delete_players_from_tournament(self.selected_players)
        self.view.prompt_clear()
        self.tournament_controller.show_tournament_player()

    """ display the current round of tournament"""
    def display_current_round(self):
        if len(self.tournament.player_list) > 1:
            self.tournament_controller.show_current_round()
        else:
            pass

    """ When all matches requierements are complete, the user can initialize the next round"""
    def next_round(self):
        if len(self.tournament.player_list) > 1:
            if (
                    (
                        (
                            len(self.tournament.current_matches) == len(self.tournament.matches_done) and
                            self.tournament.current_round > 0
                        ) or
                        (self.tournament.current_round == 0)
                    ) and
                    (self.tournament.current_round < self.tournament.number_of_rounds)
            ):

                self.tournament_controller.next_round()
                self.tournament_controller.show_current_round()
                self.tournament_controller.save_tournament()

            elif (
                len(self.tournament.current_matches) == (len(self.tournament.matches_done)) and
                self.tournament.current_round == self.tournament.number_of_rounds
            ):
                print('\nLe nombre maximum de tour est déja atteint.\n')

            elif len(self.tournament.current_matches) != len(self.tournament.matches_done):
                print("Le round en cours n'est pas terminé.\n")
        else:
            pass

    """ select a match then let the user pick the winner or draw """
    def enter_result_of_match(self):
        self.tournament_controller.show_current_round()
        match_already_done = True
        while match_already_done:
            match_selected = self.view.prompt_to_select_match(len(self.tournament.matches_status))
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
        self.tournament_controller.set_score(selected_match=match_selected, result=result)
        self.tournament_controller.save_tournament()
        self.view.prompt_clear()
        self.tournament_controller.show_current_round()

    """ Display the ranking of the current tournament """
    def ranking_of_tournament(self):
        self.reporting_controller.display_score()

    """ set the ending date of the tournament """
    def close_tournament(self):
        self.tournament_controller.close_tournament()

    """ The user can update some information of the current tournament :
        - Name of the tournament
        - place of the tournament
        - Description
        - The number of rounds
    """

    def update_tournament_information(self):
        user_choice = self.view.prompt_modify_tournament()
        if user_choice[0] == '1':
            self.tournament.name = user_choice[1]
        if user_choice[0] == '2':
            self.tournament.localisation = user_choice[1]
        if user_choice[0] == '3':
            self.tournament.description = user_choice[1]
        if user_choice[0] == '4':
            self.tournament.number_of_rounds = user_choice[1]
