EXECUTE_REPORTING_MENU = {
    '1': 'display_actors_in_alpha_order',
    '2': 'display_actors_in_rank_order',
    '3': 'display_all_tournaments',
    '4': 'display_tournament_players_in_alpha_order',
    '5': 'display_tournament_players_in_rank_order',
    '6': 'display_all_rounds_matches_of_tournament',
    '7': 'display_ranking_of_tournament',
    '999': 'back_to_main_menu'
}


class MenuReportingController:
    def __init__(
        self,
        actors_database,
        tournaments_database,
        view, tournament,
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

    def refresh_controller(self):
        self.tournament = self.tournament_controller.tournament
        self.reporting_controller.tournament = self.tournament_controller.tournament

    def display_actors_in_alpha_order(self):
        self.reporting_controller.list_all_actors('first_name')

    def display_actors_in_rank_order(self):
        self.reporting_controller.list_all_actors('ranking')

    def display_all_tournaments(self):
        self.reporting_controller.list_all_tournaments('name')

    def display_tournament_players_in_alpha_order(self):
        self.tournament_controller.load_tournament_for_reporting()
        self.refresh_controller()
        self.reporting_controller.display_all_player_from_tournament(
            tournament_player_list=self.tournament.player_list,
            sort_by='first_name'
        )

    def display_tournament_players_in_rank_order(self):
        self.tournament_controller.load_tournament_for_reporting()
        self.refresh_controller()
        self.reporting_controller.display_all_player_from_tournament(
            tournament_player_list=self.tournament.player_list,
            sort_by='ranking'
        )

    def display_all_rounds_matches_of_tournament(self):
        self.tournament_controller.load_tournament_for_reporting()
        self.refresh_controller()
        self.reporting_controller.display_all_round()

    def display_ranking_of_tournament(self):
        self.tournament_controller.load_tournament_for_reporting()
        self.refresh_controller()
        self.reporting_controller.display_score()
