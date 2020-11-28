from sqlalchemy import Column, SmallInteger, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class GameMode(Base):
	__tablename__ = "GameMode"

	idGameMode: Column = Column(
		SmallInteger(), primary_key=True, nullable=False, autoincrement=True)
	name: Column = Column(String(32), nullable=False, unique=True)
	boards = relationship("Board")

	def __init__(self, name: str):
		self.name = name
