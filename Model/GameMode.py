from sqlalchemy import Column, SmallInteger, String
from sqlalchemy.orm import relationship, Session

from Model import GameMode
from Model.BaseModel import BaseModel
from Model.Board import Board


class GameMode(BaseModel):
	__tablename__ = "GameMode"

	idGameMode: Column = Column(
		SmallInteger(), primary_key=True, nullable=False, autoincrement=True)
	name: Column = Column(String(32), nullable=False, unique=True)
	player: Column(String(128), nullable=True)
	boards = relationship("Board")

	def __init__(self, name: str, user_email: str):
		self.name = name
		self.player = user_email
		self.DB: Session = GameMode.init_connection()

	def save(self) -> str:
		response: str = "ERROR"
		if not GameMode.is_registered(self.name):
			self.DB.add(self)
			self.DB.commit()
			response = "OK"
		else:
			response = "NAME OCCUPIED"
		return response

	def delete(self) -> str:
		response: str = "ERROR"
		if GameMode.is_registered(self.name):
			self.DB.delete(self)
			self.DB.commit()
			response = "OK"
		else:
			response = "GAME MODE NOT REGISTERED"
		return response

	def save_pattern(self, pattern: str) -> str:
		response: str = "ERROR"
		if GameMode.is_valid_pattern(pattern):
			response = Board(self.idGameMode, pattern).save_pattern()
		else:
			response = "WRONG FORMAT"
		return response

	@staticmethod
	def is_registered(name: str):
		DB: Session = GameMode.init_connection()
		is_registered: bool = DB.query(
			DB.query(GameMode).filter_by(name=name).exists()
		).scalar()
		return is_registered

	@staticmethod
	def get_by_name(name: str) -> GameMode or None:
		game_mode: GameMode or None = None
		DB: Session = GameMode.init_connection()
		if GameMode.is_registered(name):
			game_mode = DB.query(GameMode).filter_by(name=name).first()
		return game_mode

	@staticmethod
	def is_valid_pattern(pattern: str) -> bool:
		response: bool = False
		if len(pattern) == 25:
			for mark in pattern:
				if mark != '0' and mark != '1':
					break
			response = True
		return response
