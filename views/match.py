class MatchView:
	def set_score(self, matches, current_round, view, match_selected):
		self.match_selected = match_selected
		self.match = matches[int(self.match_selected)-1]
		self.current_round = current_round
		self.view = view

		print('---------------------------------------------------')
		print('                And the winner is ?                ')
		
		"""Marker
			'.  (0 : 1)  :    ' +
		"""
		print(
			'1. ' +
			str(self.view.matable_df.loc[self.match[0]].first_name) +
			' ' +
			str(self.view.matable_df.loc[self.match[0]].last_name)
		)
		print(
			'2. ' +
			str(self.view.matable_df.loc[self.match[1]].first_name) +
			' ' +
			str(self.view.matable_df.loc[self.match[1]].last_name)
		)
		print('3. Egalité')
		print('---------------------------------------------------')	
		print('\n')

		return input('Résultat du match : ')
		

