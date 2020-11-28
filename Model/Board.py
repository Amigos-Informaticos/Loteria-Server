from sqlalchemy import Column, SmallInteger, ForeignKey, String
from sqlalchemy.orm import relationship, Session

from Model.BaseModel import BaseModel


class Board(BaseModel):
	__tablename__ = "Board"

	idGameMode: Column = Column(SmallInteger(), ForeignKey("GameMode.idGameMode"))
	idBoard: Column = Column(SmallInteger(), nullable=False, primary_key=True, autoincrement=True)
	pattern: Column = Column(String(25), nullable=False)
	game_mode = relationship("GameMode", back_populates="Board")

	def __init__(self, pattern: list, id_game_mode: int):
		pattern_string: str = ""
		for row in pattern:
			for mark in row:
				pattern_string = pattern_string + mark
		self.pattern = pattern_string
		self.idGameMode = id_game_mode
		self.DB: Session = Board.init_connection()

	def save_pattern(self) -> str:
		response: str = "ERROR"
		if not Board.is_registered(self.pattern):
			self.DB.add(self)
			self.DB.commit()
		return response

	@staticmethod
	def is_registered(pattern: str):
		DB: Session = Board.init_connection()
		is_registered: bool = DB.query(
			DB.query(Board).filter_by(pattern=pattern).exists()
		).scalar()
		return is_registered
