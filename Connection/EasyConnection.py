import json

import mysql.connector
from mysql.connector import Error


class EasyConnection:
	def __init__(self, host=None, database=None, user=None, password=None):
		if host is not None:
			self.user = user
			self.password = password
			self.database = database
			self.host = host
		else:
			self.load_file()
		self.connection = None

	def load_file(self, path="Configuration/local.json"):
		with open(path) as json_file:
			data = json.load(json_file)
			self.host = data['host']
			self.database = data['database']
			self.user = data['user']
			self.password = data['password']

	def connect(self):
		self.connection = mysql.connector.connect(
			host=self.host,
			database=self.database,
			user=self.user,
			password=self.password
		)

	def close_connection(self):
		if self.connection.is_connected():
			self.connection.close()

	def send_query(self, query, values=None):
		if self.host is not None:
			try:
				self.connect()
				if values is not None:
					cursor = self.connection.cursor(prepared=True)
					cursor.execute(query, values)
				else:
					cursor = self.connection.cursor()
					cursor.execute(query)

				self.connection.commit()
			except Error as error:
				print("Problem connecting to the database: {}".format(error))
			finally:
				self.close_connection()

	def select(self, query, values=None):
		results = []
		if self.host is not None:
			try:
				self.connect()
				if values is not None:
					cursor = self.connection.cursor(prepared=True)
					cursor.execute(query, values)
				else:
					cursor = self.connection.cursor()
					cursor.execute(query)

				results = cursor.fetchall()
			except Error as error:
				print("Problem connecting to the database: {}".format(error))
			finally:
				self.close_connection()
		return results
