from sqlalchemy import Column, SmallInteger, ForeignKey, String
from sqlalchemy.orm import relationship, Session

from Model import Board
from Model.BaseModel import BaseModel


class Board(BaseModel):
	__tablename__ = "Board"

	idGameMode: Column = Column(SmallInteger(), ForeignKey("GameMode.idGameMode"))
	idBoard: Column = Column(SmallInteger(), nullable=False, primary_key=True, autoincrement=True)
	pattern: Column = Column(String(25), nullable=False)
	game_mode = relationship("GameMode", backpopulates="Board")

	def __init__(self, id_game_mode: int):
		self.idGameMode = id_game_mode
		self.DB: Session = Board.init_connection()

	def save_pattern(self) -> str:
		response: str = "ERROR"
		if not Board.is_registered(self.pattern):
			self.DB.add(self)
			self.DB.commit()
			response = "OK"
		return response

	@staticmethod
	def get_by_game_mode(id_game_mode: str) -> list or None:
		boards: list or None = None
		DB: Session = Board.init_connection()
		boards = DB.query(Board).filter_by(idGameMode=id_game_mode)
		return boards

	@staticmethod
	def get_by_pattern(pattern: str) -> Board or None:
		board: Board or None = None
		DB: Session = Board.init_connection()
		if Board.is_registered(pattern):
			board = DB.query(Board).filter_by(pattern=pattern).first()
		return board

	@staticmethod
	def is_registered(pattern: str):
		DB: Session = Board.init_connection()
		is_registered: bool = DB.query(
			DB.query(Board).filter_by(pattern=pattern).exists()
		).scalar()
		return is_registered
