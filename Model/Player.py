import json

import sqlalchemy
from sqlalchemy import Column, String, SmallInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from Connection.EasyConnection import EasyConnection
from Util.Util import md5


class Player(declarative_base()):
	__tablename__ = "Jugador"

	correoElectronico = Column(String(128), primary_key=True, nullable=False)
	nickname = Column(String(32), nullable=False, unique=True)
	nombres = Column(String(64), nullable=False)
	apellidos = Column(String(64), nullable=False)
	contrasena = Column(String(32), nullable=False)
	puntuacion = Column(SmallInteger(), nullable=False, default=0)
	llavePublica = Column(String(32), nullable=False, unique=True)

	def __init__(self, name: str, lastname: str, nickname: str, email: str, password: str):
		self.nombres = name
		self.apellidos = lastname
		self.nickname = nickname
		self.correoElectronico = email
		self.contrasena = password
		self.llavePublica = md5(self.correoElectronico, len(self.correoElectronico))
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
		if not self.is_registered(self.correoElectronico):
			self.DB.add(self)
			self.DB.commit()
			return json.dumps({"status": "OK", "public_key": self.llavePublica})
		return json.dumps({"status": "Already registered"})

	def login(self) -> bool:
		if self.is_registered(self.email):
			query = """SELECT COUNT(CorreoElectronico) FROM Jugador 
			WHERE CorreoElectronico = %s AND Contrasena = %s"""
			values = (self.email, self.password)
			return self.connection.select(query, values)[0][0] == 1
		return False

	def delete(self) -> bool:
		if self.is_registered(self.email):
			query = """DELETE FROM Jugador WHERE CorreoElectronico = %s"""
			email = (self.email,)
			self.connection.send_query(query, email)
			return True
		return False

	@staticmethod
	def get_by_public_key(key: str):
		query = """SELECT COUNT(CorreoElectronico) FROM Jugador WHERE LlavePublica = %s"""
		key = (key,)
		connection = EasyConnection()
		if connection.select(query, key)[0][0] == 1:
			query = """SELECT Nombre, Apellidos, Mote, CorreoElectronico, Contrasena 
			FROM Jugador WHERE LlavePublica = %s"""
			values = connection.select(query, key)
			return Player(
				values[0][0],
				values[0][1],
				values[0][2],
				values[0][3],
				values[0][4]
			)

	@staticmethod
	def is_registered(email: str) -> bool:
		DB = Player.init_connection()
		exists = DB.query(Player.correoElectronico).filter_by(correoElectronico=email).scalar()
		return exists is not None
