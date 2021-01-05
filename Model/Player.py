import json

from sqlalchemy import Column, String, SmallInteger
from sqlalchemy.orm import Session

from Model import Player
from Model.BaseModel import BaseModel


class Player(BaseModel):
	__tablename__ = "Player"

	email: Column = Column(String(128), primary_key=True, nullable=False)
	nickname: Column = Column(String(32), nullable=False, unique=True)
	name: Column = Column(String(64), nullable=False)
	lastname: Column = Column(String(64), nullable=False)
	password: Column = Column(String(32), nullable=False)
	score: Column = Column(SmallInteger(), nullable=False, default=0)

	def __init__(self, name: str, lastname: str, nickname: str, email: str, password: str):
		self.name = name
		self.lastname = lastname
		self.nickname = nickname
		self.email = email
		self.password = password
		self.score = 0
		self.messages: list = []
		self.DB: Session = Player.init_connection()

	def register(self) -> str:
		if not Player.is_registered(self.email):
			if Player.is_nickname_available(self.nickname):
				self.DB.add(self)
				self.DB.commit()
				response = "OK"
			else:
				response: str = "NICKNAME OCCUPIED"
		else:
			response: str = "ALREADY REGISTERED"
		return response

	def login(self, email: str, password: str) -> bool:
		user: Player = self.DB.query(Player).filter_by(
			email=self.email).first()
		return user.email == email and user.password == password

	def delete(self) -> bool:
		deleted: bool = False
		if Player.is_registered(self.email):
			self.DB.delete(self)
			self.DB.commit()
			deleted = True
		return deleted

	def queue_message(self, message: str) -> None:
		self.messages.append(message)

	def empty_messages_queue(self) -> None:
		self.messages.clear()

	@staticmethod
	def get_by_email(email: str) -> Player or None:
		new_player: Player or None = None
		if Player.is_registered(email):
			player = Player.init_connection().query(Player).filter_by(
				email=email).first()
			new_player: Player = Player(
				player.name,
				player.lastname,
				player.nickname,
				player.email,
				player.password
			)
			print(new_player.email)
		return new_player

	@staticmethod
	def is_registered(email: str) -> bool:
		DB: Session = Player.init_connection()
		exists: bool = DB.query(
			DB.query(Player).filter_by(email=email).exists()
		).scalar()
		return exists

	@staticmethod
	def is_nickname_available(nickname: str) -> bool:
		DB: Session = Player.init_connection()
		is_occupied: bool = DB.query(
			DB.query(Player).filter_by(nickname=nickname).exists()
		).scalar()
		return not is_occupied

	@staticmethod
	def get_top_ten() -> str:
		response: str = "ERROR"
		DB: Session = Player.init_connection()
		counter: int = 0
		players: dict = {}
		results: list = DB.query(Player.nickname, Player.score).order_by(
			Player.score.asc()).limit(10)
		for player in results:
			values: dict = {
				"name": player.nickname,
				"points": str(player.score)
			}
			players[counter] = values
			counter = counter + 1
		response = str(json.dumps(players))
		return response
