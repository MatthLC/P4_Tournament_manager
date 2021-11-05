import pandas as pd
import numpy as np


class MatchView:
    def set_score(self, matches, current_round, view, match_selected):
        self.match_selected = match_selected
        self.match = matches[int(self.match_selected) - 1]
        self.current_round = current_round
        self.view = view
        self.table_all = self.view.db_table.all()
        self.matable_df = pd.DataFrame.from_dict(self.table_all)
        self.matable_df.index = np.arange(1, len(self.matable_df) + 1)

        print('---------------------------------------------------')
        print('                And the winner is ?                ')
        print(
            '1. ' +
            str(self.matable_df.loc[int(self.match[0])].first_name) +
            ' ' +
            str(self.matable_df.loc[int(self.match[0])].last_name)
        )
        print(
            '2. ' +
            str(self.matable_df.loc[int(self.match[1])].first_name) +
            ' ' +
            str(self.matable_df.loc[int(self.match[1])].last_name)
        )
        print('3. Egalité')
        print('---------------------------------------------------')
        print('\n')

        while True:
            user_choice = input('Résultat du match : ')
            try:
                if int(user_choice) in range(1, 4):
                    break
                else:
                    print('Saisir un match entre 1 et 3')
            except ValueError:
                print('Saisie incorrecte.')

        return user_choice
