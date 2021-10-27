from models.database import TOURNAMENT_KEEP
from models.swisssystem import SwissSystem
from models.tournament import Tournament


class TournamentController:
    def __init__(
        self,
        actors_database,
        tournaments_database,
        view,
        tournament,
        score_board
    ):
        self.actors_database = actors_database
        self.tournaments_database = tournaments_database
        self.view = view
        self.tournament = tournament
        self.score_board = score_board

    def create_tournament(self):
        while True:
            tournament_input = self.view.prompt_for_tournament()
            verify_if_already_exist = self.tournaments_database.search_db(
                column1='name',
                value1=tournament_input.name
            )

            if len(verify_if_already_exist) == 0:
                self.tournaments_database.insert_db(tournament_input)
                self.load_tournament(
                    self.tournaments_database.db_table.get(doc_id=len(self.tournaments_database.db_table)).doc_id
                )
                break
            else:
                print('\nle tournoi existe déjà !\n')

    def load_tournament(self, tournament_id):
        self.tournament_id = tournament_id
        tournament_to_load = self.tournaments_database.load(tournament_id)

        self.tournament = Tournament(
            name=tournament_to_load['name'],
            localisation=tournament_to_load['localisation'],
            time_control=tournament_to_load['time_control'],
            description=tournament_to_load['description'],
            number_of_rounds=tournament_to_load['number_of_rounds'],
            current_round=tournament_to_load['current_round'],
            player_list=tournament_to_load['player_list'],
            tournament_started=tournament_to_load['tournament_started'],
            tournament_finished=tournament_to_load['tournament_finished'],
            round_list=tournament_to_load['round_list'],
            current_matches=tournament_to_load['current_matches'],
            matches_done=tournament_to_load['matches_done'],
            matches_status=tournament_to_load['matches_status'],
            winner_list=tournament_to_load['winner_list'],
            winner=tournament_to_load['winner'],
            match_played_by_player=tournament_to_load['match_played_by_player'],
            score=tournament_to_load['score']
        )

    def load_tournament_for_reporting(self):
        self.show_all_tournament()
        tournament_to_display = self.view.prompt_for_tournament_to_display(
            max_number=len(self.tournaments_database.table_all)
        )
        self.load_tournament(tournament_to_display)

    def show_all_tournament(self):
        if len(self.tournaments_database.table_all) == 0:
            print("Il n'y pas de tournoi pour le moment.")
        if len(self.tournaments_database.table_all) > 0:
            tournament_db = self.tournaments_database.show(keep=TOURNAMENT_KEEP)
            self.view.display(tournament_db)

    def show_tournament_player(self, sort_list=[]):
        self.sort_list = sort_list

        if not self.tournament.player_list:
            print("Il n'y a pas de joueur pour le moment")
        else:
            print('\n Liste des participants du tournoi ' + self.tournament.name + ' : \n')
            show = self.actors_database.show(keep=None, id_list=self.tournament.player_list, sort_list=self.sort_list)
            self.view.display(show)

    def save_tournament(self):
        self.tournaments_database.update_db(self.tournament)

    def close_tournament(self):
        self.tournament.close()
        self.save_tournament()

    def add_player_to_tournament(self, players):
        self.players = players
        for item in self.players:
            player = self.actors_database.load(item)
            self.tournament.add_player(player.doc_id)
            self.save_tournament()

    def delete_players_from_tournament(self, players):
        self.players = players
        self.tournament.delete_player(self.players)
        self.save_tournament()

    def next_round(self):
        self.tournament.clear_round()
        self.tournament.current_round += 1
        self.round_system()

    def show_current_round(self):
        if self.tournament.current_round == 0:
            print("Il n'y a pas de round pour le moment.")
        else:
            self.view.display_rounds(
                matches=self.tournament.current_matches,
                current_round=self.tournament.current_round,
                view=self.actors_database,
                winner=self.tournament.winner
            )

    def round_system(self):
        if self.tournament.current_round == 1:
            self.tournament.current_matches = SwissSystem().first_round(
                self.actors_database.sort_by(
                    item_list=self.tournament.player_list,
                    sort_list=['ranking']
                )
            )

            self.tournament.init_match_played_by_player()
            self.tournament.init_score()

        if self.tournament.current_round > 1:
            show = self.actors_database.show(keep=['ranking'], id_list=self.tournament.player_list)
            show = list(show.to_dict().values())[0]

            self.tournament.current_matches = SwissSystem().other_round(
                score=self.tournament.score,
                ranking=show,
                match_played_by_player=self.tournament.match_played_by_player
            )

        for item in range(0, len(self.tournament.current_matches)):
            self.tournament.matches_status.append('En cours')
            self.tournament.winner.append('Match non terminé')

        self.tournament.round_list[str(self.tournament.current_round)] = self.tournament.current_matches.copy()
        self.tournament.winner_list[str(self.tournament.current_round)] = self.tournament.winner.copy()

    def set_score(self, selected_match, result):
        self.selected_match = int(selected_match) - 1
        self.result = result
        self.result_player1 = self.score_board[self.result][0]
        self.result_player2 = self.score_board[self.result][1]
        self.display_winner = ''
        self.match = self.tournament.current_matches[self.selected_match]

        if result != '3':
            last_name = self.actors_database.matable_df.loc[int(self.match[int(self.result) - 1])].first_name
            first_name = self.actors_database.matable_df.loc[int(self.match[int(self.result) - 1])].last_name
            self.display_winner = first_name + ' ' + last_name

        if result == '3':
            self.display_winner = 'Egalité'

        self.tournament.apply_score(
            self.match,
            self.result_player1,
            self.result_player2,
            self.selected_match,
            self.display_winner
        )
