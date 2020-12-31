import json
import random

from Model.GameMode import GameMode
from Model.Player import Player
from Server.Controller.PlayerController import PlayerController
from Util.Util import md5


class Room:
	def __init__(self, creator_email: str, limit: int, speed: int, rounds: int, game_mode: str):
		self.creator: Player = Player.get_by_email(creator_email)
		self.users: list = []
		self.users_limit = limit
		self.deck: list = []
		self.speed = speed
		self.rounds = rounds
		self.set_game_mode(game_mode, self.creator.email)
		self.users.append(self.creator)
		self.id: str = md5(creator_email, 2)[0:5]

	def set_game_mode(self, game_mode_name: str, user_email: str) -> None:
		self.game_mode: GameMode = GameMode.get_by_name_and_user(game_mode_name, user_email)

	def add_user(self, user_email) -> bool:
		response: bool = False
		in_room: bool = False
		user: Player = Player.get_by_email(user_email)
		for player in self.users:
			if player.email == user_email:
				in_room = True
				break
		if not in_room:
			self.users.append(user)
			response = True
		return response

	def remove_user(self, user_email) -> bool:
		response: bool = False
		user: Player = Player.get_by_email(user_email)
		if user in self.users:
			self.users.remove(user)
			response = True
		return response

	def send_message(self, values: json) -> None:
		arguments: set = {"sender", "message"}
		if all(key in values for key in arguments):
			values["room_id"] = self.id
			for user in self.users:
				if user.correoElectronico != values["sender"]:
					values["receiver"] = user.correoElectronico
					PlayerController.send_message(values)

	def is_empty(self) -> bool:
		return len(self.users) == 0

	def get_sorted_deck(self) -> str:
		response: str = "ERROR"
		cards: dict = {}
		if len(self.deck) == 0:
			self.sort_deck()
		for i in range(54):
			cards[i] = {
				"card": self.deck[i]
			}
		response = str(json.dumps(cards))
		return response

	def sort_deck(self) -> None:
		if len(self.deck) == 0:
			self.deck = [*range(1, 55)]
		random.shuffle(self.deck)
