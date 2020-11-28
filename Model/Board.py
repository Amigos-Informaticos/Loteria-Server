import json

import sqlalchemy
from sqlalchemy import Column, SmallInteger, ForeignKey, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Session

from Configuration.Configuration import get_connection_file

Base = declarative_base()


class Board(Base):
	__tablename__ = "Board"

	idGameMode: Column = Column(SmallInteger(), ForeignKey("GameMode.idGameMode"))
	idBoard: Column = Column(SmallInteger(), nullable=False, primary_key=True, autoincrement=True)
	pattern: Column = Column(String(25), nullable=False)
	game_mode = relationship("GameMode", back_populates="Board")

	def __init__(self, pattern: list, id_game_mode: int):
		pattern_string: str = ""
		for i in pattern:
			for j in i:
				pattern_string = pattern_string + j
		self.pattern = pattern_string
		self.idGameMode = id_game_mode
		self.DB: Session = Board.init_connection()

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

	def save_pattern(self) -> str:
		response: str = "ERROR"
		if not Board.is_registered(self.pattern):
			self.DB.add(self)
			self.DB.commit()
		return response

	@staticmethod
	def is_registered(pattern: str):
		DB = Board.init_connection()
		is_registered = DB.query(
			DB.query(Board).filter_by(pattern=pattern).exists()
		).scalar()
		return is_registered
