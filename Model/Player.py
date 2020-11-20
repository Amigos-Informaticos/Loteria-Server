import json

import sqlalchemy
from sqlalchemy import Column, String, SmallInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

from Configuration.Configuration import get_connection_file
from Model import Player


class Player(declarative_base()):
	__tablename__ = "Jugador"

	correoElectronico = Column(String(128), primary_key=True, nullable=False)
	nickname: Column = Column(String(32), nullable=False, unique=True)
	nombres: Column = Column(String(64), nullable=False)
	apellidos: Column = Column(String(64), nullable=False)
	contrasena: Column = Column(String(32), nullable=False)
	puntuacion: Column = Column(SmallInteger(), nullable=False, default=0)

	def __init__(self, name: str, lastname: str, nickname: str, email: str, password: str):
		self.nombres = name
		self.apellidos = lastname
		self.nickname = nickname
		self.correoElectronico = email
		self.contrasena = password
		self.DB = Player.init_connection()

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
		response: str = "Error"
		if not Player.is_registered(self.correoElectronico):
			self.DB.add(self)
			self.DB.commit()
			response = "OK"
		else:
			response = "Already registered"
		return response

	def login(self) -> bool:
		exists = self.DB.query(
			self.DB.query(Player).filter_by(
				correoElectronico=self.correoElectronico, contrasena=self.contrasena).exists()
		).scalar()
		return exists

	def delete(self) -> bool:
		if Player.is_registered(self.correoElectronico):
			self.DB.delete(self)
			response = True
		else:
			response = False
		return response

	@staticmethod
	def get_by_email(email: str) -> Player:
		if Player.is_registered(email):
			player = Player.init_connection().query(Player).filter_by(
				correoElectronico=email).first()
			new_player = Player(
				player.nombres,
				player.apellidos,
				player.nickname,
				player.correoElectronico,
				player.contrasena
			)
			return new_player
		return None

	@staticmethod
	def is_registered(email: str) -> bool:
		DB = Player.init_connection()
		exists = DB.query(
			DB.query(Player).filter_by(correoElectronico=email).exists()
		).scalar()
		return exists

	@staticmethod
	def get_top_ten() -> str:
		response: str = "ERROR"
		DB = Player.init_connection()
		counter: int = 0
		players: dict = {}
		results: list = DB.query(Player.nombres, Player.puntuacion).order_by(
			Player.puntuacion.asc()).limit(10)
		for player in results:
			values: dict = {
				"name": player.nombres,
				"points": str(player.puntuacion)
			}
			players[counter] = values
			counter = counter + 1
		if len(players) > 0:
			response = str(players)
		print()
		print(response)
		print()
		return response
