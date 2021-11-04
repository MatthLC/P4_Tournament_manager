from models.database import Database, ACTOR_FORMAT, TOURNAMENT_FORMAT

from controllers.base import TournamentManager

from views.base import View


def main():
    actor_db = Database(name='actors', table_format=ACTOR_FORMAT)
    tournament_db = Database(name='tournaments', table_format=TOURNAMENT_FORMAT)

    view = View()

    control = TournamentManager(
        actors_database=actor_db,
        tournaments_database=tournament_db,
        view=view
    )

    control.run()


if __name__ == '__main__':
    main()
