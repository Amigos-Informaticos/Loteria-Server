import json

import sqlalchemy
from sqlalchemy import Column, String, SmallInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

import Model


class Player(declarative_base()):
	__tablename__ = "Jugador"

	correoElectronico = Column(String(128), primary_key=True, nullable=False)
	nickname = Column(String(32), nullable=False, unique=True)
	nombres = Column(String(64), nullable=False)
	apellidos = Column(String(64), nullable=False)
	contrasena = Column(String(32), nullable=False)
	puntuacion = Column(SmallInteger(), nullable=False, default=0)

	def __init__(self, name: str, lastname: str, nickname: str, email: str, password: str):
		self.nombres = name
		self.apellidos = lastname
		self.nickname = nickname
		self.correoElectronico = email
		self.contrasena = password
		self.DB = Player.init_connection()

	@staticmethod
	def init_connection(path: str = "Configuration/connection.json") -> Session:
		connection_string = "mysql+pymysql://"
		with open(path) as json_connection:
			data = json.load(json_connection)
			connection_string += data['user'] + ":"
			connection_string += data['password'] + "@"
			connection_string += data['host'] + '/'
			connection_string += data['database']
		return Session(sqlalchemy.create_engine(connection_string))

	def register(self) -> str:
		if not Player.is_registered(self.correoElectronico):
			self.DB.add(self)
			self.DB.commit()
			return json.dumps({"status": "OK"})
		return json.dumps({"status": "Already registered"})

	def login(self) -> bool:
		exists = self.DB.query(
			self.DB.query(Player).filter_by(correoElectronico=self.correoElectronico,
			                                contrasena=self.contrasena).exists()
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
	def get_by_email(email: str) -> Model.Player:
		if Player.is_registered(email):
			player = Player.init_connection().query(Player).filter_by(
				correoElectronico=email).first()
			return player
		return None

	@staticmethod
	def is_registered(email: str) -> bool:
		DB = Player.init_connection()
		exists = DB.query(
			DB.query(Player).filter_by(correoElectronico=email).exists()
		).scalar()
		return exists
