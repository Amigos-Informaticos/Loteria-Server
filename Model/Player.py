import json
from typing import Optional

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
		self.current_score: int = 0
		self.messages: list = []
		self.kicked_counter: int = 0
		self.kicked_by: list = []
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

	def queue_message(self, message: str, sender: str) -> None:
		self.messages.append({"nickname": sender, "message": message})

	def clear_messages(self) -> None:
		self.messages.clear()

	def save(self) -> None:
		self.DB.commit()

	@staticmethod
	def change_password(user_email: str, old_password: str, new_password: str) -> bool:
		response: bool = False
		DB: Session = Player.init_connection()
		player: Player = DB.query(Player).filter_by(email=user_email).first()
		if player.password == old_password:
			player.password = new_password
			DB.commit()
			response = True
		return response

	@staticmethod
	def add_score(score: int, user_email: str) -> None:
		DB: Session = Player.init_connection()
		player = DB.query(Player).filter_by(email=user_email).first()
		player.score += score
		DB.commit()

	@staticmethod
	def get_score_by_email(email: str) -> int:
		score: int or None = None
		if Player.is_registered(email):
			player = Player.init_connection().query(Player).filter_by(
				email=email).first()
			score = player.score
		if score is None:
			score = 0
		return score

	@staticmethod
	def get_by_email(email: str) -> Player or None:
		new_player: Optional[Player] = None
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
			Player.score.desc()).limit(10)
		for player in results:
			values: dict = {
				"name": player.nickname,
				"points": str(player.score)
			}
			players[counter] = values
			counter = counter + 1
		response = str(json.dumps(players))
		return response
