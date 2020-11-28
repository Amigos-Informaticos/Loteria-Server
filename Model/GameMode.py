from sqlalchemy import Column, SmallInteger, String
from sqlalchemy.orm import relationship, Session

from Model.BaseModel import BaseModel


class GameMode(BaseModel):
	__tablename__ = "GameMode"

	idGameMode: Column = Column(
		SmallInteger(), primary_key=True, nullable=False, autoincrement=True)
	name: Column = Column(String(32), nullable=False, unique=True)
	boards = relationship("Board")

	def __init__(self, name: str):
		self.name = name
		self.DB: Session = GameMode.init_connection()

	def save(self) -> str:
		if not GameMode.is_registered(self.name):
			self.DB.add(self)
			self.DB.commit()
			response: str = "OK"
		else:
			response: str = "NAME OCCUPIED"
		return response

	def delete(self) -> str:
		if GameMode.is_registered(self.name):
			self.DB.delete()
			self.DB.commit()
			response: str = "OK"
		else:
			response: str = "GAME MODE NOT REGISTERED"
		return response

	@staticmethod
	def is_registered(name: str):
		DB: Session = GameMode.init_connection()
		is_registered: bool = DB.query(
			DB.query(GameMode).filter_by(name=name).existst()
		).scalar()
		return is_registered
