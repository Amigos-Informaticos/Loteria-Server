from sqlalchemy import Column, SmallInteger, ForeignKey, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Board(Base):
	__tablename__ = "Board"

	idGameMode: Column = Column(SmallInteger(), ForeignKey("GameMode.idGameMode"))
	idBoard: Column = Column(SmallInteger(), nullable=False, primary_key=True, autoincrement=True)
	pattern: Column = Column(String(25), nullable=False)
	game_mode = relationship("GameMode", back_populates="Board")

	def __init__(self, pattern: list):
		pattern_string: str = ""
		for i in pattern:
			for j in i:
				pattern_string = pattern_string + j
		self.pattern = pattern_string
