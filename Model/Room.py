import json
import random
from random import randint

from Model.GameMode import GameMode
from Model.Player import Player
from Util.Util import md5


class Room:
	def __init__(self, creator_email: str, limit: int, speed: int, game_mode: str):
		self.creator: Player = Player.get_by_email(creator_email)
		self.users: list = []
		self.users_limit = limit
		self.deck: list = []
		self.speed = speed
		self.winner: Player or None = None
		self.set_game_mode(game_mode)
		self.users.append(self.creator)
		self.id: str = md5(str(randint(0, 99)), 2)[0:5]
		self.has_started = False

	def set_game_mode(self, game_mode_name: str) -> None:
		self.game_mode: GameMode = GameMode.get_by_name(game_mode_name)

	def add_user(self, user_email: str) -> bool:
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

	def remove_user(self, user_email: str) -> bool:
		response: bool = False
		for player in self.users:
			if player.email == user_email:
				player.clear_messages()
				self.users.remove(player)
				response = True
				break
		return response

	def empty_room(self) -> None:
		self.users.clear()

	def is_empty(self) -> bool:
		return len(self.users) == 0

	def get_sorted_deck(self) -> str:
		response: str = "ERROR"
		cards: dict = {}
		if len(self.deck) == 0:
			self.sort_deck()
		for i in range(54):
			cards[str(i)] = str(self.deck[i])
		response = str(json.dumps(cards))
		return response

	def sort_deck(self) -> None:
		if len(self.deck) == 0:
			self.deck = [*range(1, 55)]
		random.shuffle(self.deck)

	def get_player_by_email(self, player_email: str) -> Player or None:
		player_response: Player or None = None
		for player in self.users:
			if player.email == player_email:
				player_response = player
				break
		return player_response

	def get_player_by_nickname(self, nickname: str) -> Player or None:
		player_response: Player or None = None
		for player in self.users:
			if player.nickname == nickname:
				player_response = player
		return player_response
