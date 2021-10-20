import pandas as pd
import numpy as np

class RoundView:
	def show_current_round(self, matches, current_round, view, winner):
		self.matches = matches
		self.current_round = current_round
		self.view = view
		self.winner = winner
		self.table_all = self.view.db_table.all()
		self.matable_df = pd.DataFrame.from_dict(self.table_all)
		self.matable_df.index = np.arange(1,len(self.matable_df)+1)
	
		print('---------------------------------------------------')
		print('                    ROUND ' + str(self.current_round))
		print('---------------------------------------------------')

		self.matches_np = []
		for match in self.matches:
			self.matches_np.append(np.array(match))

		matches_data = []
		i = 1
		for match in self.matches_np:
			matches_data.append(np.array([
				str(i) + '.  ',
				str(self.matable_df.loc[int(match[0])].first_name) + ' ' +
					str(self.matable_df.loc[int(match[0])].last_name),
				'  VS  ',
				str(self.matable_df.loc[int(match[1])].first_name) + ' ' +
					str(self.matable_df.loc[int(match[1])].last_name),
				self.winner[int(i)-1]
			]))
			i += 1

		all_index = []
		for item in range(1,len(matches) + 1):
			all_index.append(str(item))

		matches_df = pd.DataFrame(
			matches_data,
			index = all_index,
			columns = ['', 'joueur 1', '', 'joueur 2', 'Vainqueur']
		).to_string(index = False)
	
		print(matches_df)
		print('\n')