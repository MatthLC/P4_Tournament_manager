class SwissSystem:

	def first_round(self, base):
		self.base= base
		self.half = int(self.base.index.size/ 2)
		self.all_matches = []

		lower_half = self.base.iloc[0: self.half]
		upper_half = self.base.iloc[self.half:]

		lower_list = list(lower_half.index)
		upper_list = list(upper_half.index)

		for i in range(0, self.half):
			self.all_matches.append([str(lower_list[i]),str(upper_list[i])])

		return self.all_matches

	def other_round(self, score, ranking, match_played_by_player):
		self.score = score
		self.score_copy = {}
		self.ranking = ranking
		self.match_played_by_player = match_played_by_player
		self.all_matches = []

		for key, value in self.ranking.items():
			self.score_copy[str(key)] = [self.score[str(key)], value]

		self.sorted_score = sorted(self.score_copy, key = self.score_copy.get, reverse = True)
		
		while len(self.sorted_score) > 0:

			for i in range(1,len(self.sorted_score)):
				for opponent in self.match_played_by_player[self.sorted_score[0]]:
					if opponent == self.sorted_score[i]:
						break
						
				self.all_matches.append([self.sorted_score[0],self.sorted_score[i]])
				del self.sorted_score[i]
				del self.sorted_score[0]
				break

		return self.all_matches 




		