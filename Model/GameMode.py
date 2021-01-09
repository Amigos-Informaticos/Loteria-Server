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
	player: Column = Column(String(128), nullable=True)
	boards = relationship("Board", back_populates="game_mode")

	def __init__(self, name: str, user_email: str):
		self.name = name
		self.player = user_email
		self.DB: Session = GameMode.init_connection()
		if GameMode.is_registered(self.name):
			auxiliary_game_mode: GameMode = self.DB.query(GameMode).filter_by(
				name=self.name,
				player=self.player).first()
			self.idGameMode = auxiliary_game_mode.idGameMode
			del auxiliary_game_mode

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
		if not GameMode.is_registered(self.name):
			self.save()
		if GameMode.is_valid_pattern(pattern):
			board: Board = Board(self.idGameMode)
			board.pattern = pattern
			response = board.save_pattern()
			response = "OK"
		else:
			response = "WRONG FORMAT"
		return response

	def get_boards(self) -> list or None:
		boards: list or None = None
		boards = Board.get_by_game_mode(self.idGameMode)
		return boards

	@staticmethod
	def is_registered(name: str) -> bool:
		DB: Session = GameMode.init_connection()
		is_registered: bool = DB.query(
			DB.query(GameMode).filter_by(name=name).exists()
		).scalar()
		return is_registered

	@staticmethod
	def get_by_user(user_email: str) -> list or None:
		modes: list or None = None
		if GameMode.count_by_user(user_email) > 0:
			DB: Session = GameMode.init_connection()
			modes = DB.query(GameMode).filter_by(player=user_email)
		return modes

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

	@staticmethod
	def count_by_user(user_email: str) -> int:
		DB: Session = GameMode.init_connection()
		return DB.query(GameMode.idGameMode).filter_by(player=user_email).count()
