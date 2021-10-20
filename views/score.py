import pandas as pd
import numpy as np

class ScoreView:
	def display_score(self, player_list, score, view):
		self.player_list = player_list
		self.score = score
		self.view = view
		self.table_all = self.view.db_table.all()
		self.matable_df = pd.DataFrame.from_dict(self.table_all)
		self.matable_df.index = np.arange(1,len(self.matable_df)+1)
	
		print('---------------------------------------------------')
		print('                    CLASSEMENT                     ')
		print('---------------------------------------------------')

		score_data = []
		i = 1
		for key_player, score in sorted(self.score.items(), key = lambda x: x[1], reverse = True):
			score_data.append(np.array([
				str(i) + '.  ',
				str(self.matable_df.loc[int(key_player)].first_name) + ' ' +
					str(self.matable_df.loc[int(key_player)].last_name),
				score[0]
			]))
			i += 1

		all_index = []
		for item in range(1,len(self.score) + 1):
			all_index.append(str(item))

		score_df = pd.DataFrame(
			score_data,
			index = all_index,
			columns = ['', 'joueur','score']
		).to_string(index = False)
	
		print(score_df)
		print('\n')