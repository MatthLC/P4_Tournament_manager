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
			self.all_matches.append([lower_list[i],upper_list[i]])

		return self.all_matches

	def other_round(self, score, ranking, match_played_by_player):
		self.score = score.copy()
		self.ranking = ranking
		self.match_played_by_player = match_played_by_player
		self.all_matches = []

		for key, value in self.ranking.items():
			self.score[key].append(value)

		self.sorted_score = sorted(self.score, key = self.score.get)
		
		while len(self.sorted_score) > 0:
			check_opponent = False

			for i in range(1,len(self.sorted_score)):
				for opponent in self.match_played_by_player[self.sorted_score[0]]:
					if opponent == self.sorted_score[i]:
						check_opponent = True

				if check_opponent == False :
					self.all_matches.append([self.sorted_score[0],self.sorted_score[i]])
					del self.sorted_score[i]
					del self.sorted_score[0]
					break

		return self.all_matches




		