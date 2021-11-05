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

    def show_all_actors(self):
        self.view.display(self.actors_database.show())

    def add_actor(self):
        while True:
            actor_input = self.view.prompt_for_actor(top_rank=len(self.actors_database.table_all))
            verify_if_already_exist = self.actors_database.search_db(
                column1='first_name',
                value1=actor_input.first_name,
                column2='last_name',
                value2=actor_input.last_name
            )

            if len(verify_if_already_exist) == 0:
                print(verify_if_already_exist)
                self.actors_database.insert_db(actor_input)
                break
            else:
                print('\nLe participant existe déjà!\n')

    def modify_actor(self, user_choice):
        self.user_choice = user_choice
        new_rank = {'ranking': int(user_choice[1])}
        self.db_table = self.actors_database.db_table
        self.actual_rank = self.db_table.get(doc_id=int(user_choice[0]))['ranking']
        self.query = self.actors_database.db_query

        if int(user_choice[1]) > self.actual_rank:
            for rank in range(int(self.actual_rank) + 1, int(user_choice[1]) + 1):
                actor_to_update = self.db_table.get(self.query.ranking == rank).doc_id
                rank_to_update = self.db_table.get(self.query.ranking == rank)['ranking'] - 1
                self.actors_database.modify_db(dictionnary={'ranking': int(rank_to_update)}, id_list=actor_to_update)

        if int(user_choice[1]) < self.actual_rank:
            for rank in range(int(self.actual_rank) - 1, int(user_choice[1]) - 1, -1):
                actor_to_update = self.db_table.get(self.query.ranking == rank).doc_id
                rank_to_update = self.db_table.get(self.query.ranking == rank)['ranking'] + 1
                self.actors_database.modify_db(dictionnary={'ranking': int(rank_to_update)}, id_list=actor_to_update)

        self.actors_database.modify_db(dictionnary=new_rank, id_list=user_choice[0])
        self.view.prompt_clear()
        self.show_all_actors()
