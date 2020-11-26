import json

import sqlalchemy
from sqlalchemy import Column, String, SmallInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

from Configuration.Configuration import get_connection_file
from Model import Player


class Player(declarative_base()):
	__tablename__ = "Player"

	email: Column = Column(String(128), primary_key=True, nullable=False)
	nickname: Column = Column(String(32), nullable=False, unique=True)
	name: Column = Column(String(64), nullable=False)
	lastname: Column = Column(String(64), nullable=False)
	password: Column = Column(String(32), nullable=False)
	score: Column = Column(SmallInteger(), nullable=False, default=0)

	def __init__(self, name: str, lastname: str, nickname: str, email: str, password: str):
		self.name = name
		self.lastname = lastname
		self.nickname = nickname
		self.email = email
		self.password = password
		self.DB: Session = Player.init_connection()

	@staticmethod
	def init_connection(path: str = None) -> Session:
		connection_string = "mysql+pymysql://"
		if path is None:
			path = get_connection_file()
		with open(path) as json_connection:
			data = json.load(json_connection)
			connection_string += data['user'] + ":"
			connection_string += data['password'] + "@"
			connection_string += data['host'] + '/'
			connection_string += data['database']
		return Session(sqlalchemy.create_engine(connection_string))

	def register(self) -> str:
		if not Player.is_registered(self.email):
			if Player.is_nickname_available(self.nickname):
				self.DB.add(self)
				self.DB.commit()
				response = "OK"
			else:
				response = "Nickname occupied"
		else:
			response = "Already registered"
		return response

	def login(self) -> bool:
		exists = self.DB.query(
			self.DB.query(Player).filter_by(
				email=self.email, password=self.password).exists()
		).scalar()
		return exists

	def delete(self) -> bool:
		if Player.is_registered(self.email):
			self.DB.delete(self)
			response = True
		else:
			response = False
		return response

	@staticmethod
	def get_by_email(email: str) -> Player:
		if Player.is_registered(email):
			player = Player.init_connection().query(Player).filter_by(
				email=email).first()
			new_player = Player(
				player.name,
				player.lastname,
				player.nickname,
				player.email,
				player.password
			)
			return new_player
		return None

	@staticmethod
	def is_registered(email: str) -> bool:
		DB = Player.init_connection()
		exists = DB.query(
			DB.query(Player).filter_by(email=email).exists()
		).scalar()
		return exists

	@staticmethod
	def is_nickname_available(nickname: str) -> bool:
		DB = Player.init_connection()
		is_occupied = DB.query(
			DB.query(Player).filter_by(nickname=nickname).exists()
		).scalar()
		return not is_occupied

	@staticmethod
	def get_top_ten() -> str:
		response: str = "ERROR"
		DB: Session = Player.init_connection()
		counter: int = 0
		players: dict = {}
		results: list = DB.query(Player.name, Player.score).order_by(
			Player.score.asc()).limit(10)
		for player in results:
			values: dict = {
				"name": player.name,
				"points": str(player.score)
			}
			players[counter] = values
			counter = counter + 1
		response = str(json.dumps(players))
		return response
