from tinydb import TinyDB, Query, where
import numpy as np
import pandas as pd


ACTOR_FORMAT = {
	'first_name' : 'Prénom',
	'last_name' : 'Nom',
	'sex': 'sexe',
	'birthday':'Anniversaire',
	'ranking': 'classement' 
}

ACTOR_KEEP = []

TOURNAMENT_FORMAT = {
	'name' : 'Nom',
	'number_of_rounds' : 'Nombre de tours',
	'current_round': 'Tour en cours',
	'tournament_started':'Date de lancement',
	'tournament_finished': 'Date de fin' 
}

TOURNAMENT_KEEP = [
	'name',
	'localisation',
	'number_of_rounds',
	'current_round',
	'tournament_started',
	'tournament_finished'
]

class Database:
	def __init__(self, name, table_format = None):
		self.name = name
		self.db = TinyDB(self.name + '.json')
		self.db_table = self.db.table(self.name)
		self.db_query = Query()
		self.table_format = table_format
		self.table_all = self.db_table.all()
		self.matable_df = pd.DataFrame.from_dict(self.table_all)

	#insert data to database using __dict__ on class object
	def insert_db(self, data_from_object):
		self.data_from_object = data_from_object
		self.db_table.insert(self.data_from_object.__dict__)

	#updated
	def update_db(self, tournament):
		self.tournament = tournament
		self.db_table.update(
			self.tournament.__dict__,
			doc_ids = [
				self.db_table.get(
					self.db_query.name == self.tournament.name
				).doc_id
			]
		)

	def modify_db(self, dictionnary, id_list):
		self.dictionnary = dictionnary
		self.id_list = id_list

		self.db_table.update(self.dictionnary, doc_ids = [int(self.id_list)])

	#search by columns
	def search_db(self, column1, value1, column2 = None, value2 = None):
		self.db_query = Query()
		self.column1 = column1
		self.column2 = column2
		self.value1 = value1
		self.value2 = value2
		
		if column2 == None:
			result = self.db_table.search(where(self.column1) == self.value1)
		if column2 != None:
			result = self.db_table.search((where(self.column1) == self.value1) & (where(self.column2) == self.value2))

		return result

	#delete all
	def clear_db(self):
		self.db_table.truncate()

	#show database

	def show(self, keep = None, id_list = []):
		self.keep = keep
		
		self.id_list = id_list

		self.table_all = self.db_table.all()
		
		self.matable_df = pd.DataFrame.from_dict(self.table_all)
		self.matable_df.index = np.arange(1,len(self.matable_df)+1)
		self.df = self.matable_df

		if self.keep:
			self.df = self.df[self.keep]

		if len(self.id_list) > 0:
			self.df = self.df.loc[self.id_list]
		
		self.new_index = []
		for i in range(1,len(self.df) + 1):
			self.new_index.append(i)

		self.df.index = self.new_index
		self.df_renamed = self.df.rename(columns = self.table_format)

		return self.df_renamed

	def load(self, line):
		self.table_all = self.db_table.all()
		self.line = line
		return self.db_table.all()[int(self.line) - 1]

	def sort_by(self, item_list, sort_list):
		self.matable_df = pd.DataFrame.from_dict(self.table_all)
		self.matable_df.index = np.arange(1,len(self.matable_df)+1)
		self.item_list =  item_list
		self.sort_list = sort_list

		df = self.matable_df.loc[self.item_list].sort_values(by = self.sort_list)

		return df




