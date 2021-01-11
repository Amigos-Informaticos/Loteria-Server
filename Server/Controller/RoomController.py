import json

from Model.Player import Player
from Model.Room import Room


class RoomController:
	rooms: list = []

	def make_room(self, values: json, _) -> str:
		response: str = "ERROR"
		arguments: set = {"creator_email", "rounds", "speed", "players", "game_mode"}
		if all(key in arguments for key in values):
			if not RoomController.exists_by_creator(values["creator_email"]):
				room: Room = Room(
					values["creator_email"],
					int(values["players"]),
					int(values["speed"]),
					int(values["rounds"]),
					values["game_mode"]
				)
				room.users_limit = int(values["players"])
				RoomController.rooms.append(room)
				response = room.id
			else:
				response = "ROOM ALREADY EXISTS"
		else:
			response = "WRONG ARGUMENTS"
		return response

	def enter_room(self, configuration: json, _) -> str:
		response: str = "ERROR"
		arguments: set = {"room_id", "user_email"}
		if all(key in configuration for key in arguments):
			if RoomController.get_room_by_id(configuration["room_id"]) is not None:
				room: Room = RoomController.get_room_by_id(configuration["room_id"])
				if len(room.users) < room.users_limit:
					if room.add_user(configuration["user_email"]):
						if room.game_mode is not None:
							game_mode = room.game_mode.name
						else:
							game_mode = "NOT FOUND"
						response: dict = {
							"speed": str(room.speed),
							"rounds": str(room.rounds),
							"game_mode": game_mode,
							"game_mode_id": str(room.game_mode.idGameMode),
							"available_spaces:": str(room.users_limit - len(room.users)),
							"max_players": str(room.users_limit)
						}
						response = str(json.dumps(response))
					else:
						response = "ALREADY JOINED"
				else:
					response = "ROOM FULL"
			else:
				response = "WRONG ID"
		else:
			response = "WRONG ARGUMENTS"
		return response

	def exit_room(self, configuration: json, _) -> str:
		response: str = "ERROR"
		arguments: set = {"room_id", "user_email"}
		if all(key in configuration for key in arguments):
			room: Room = RoomController.get_room_by_id(configuration["room_id"])
			if room is not None:
				room.remove_user(configuration["user_email"])
				if room.is_empty():
					self.rooms.remove(room)
				response = "OK"
			else:
				response = "ROOM NOT FOUND"
		else:
			response = "WRONG ARGUMENTS"
		return response

	def send_message_to_room(self, values: json, _) -> str:
		response: str = "ERROR"
		arguments: set = {"message", "nickname", "room_id", "user_email"}
		if all(key in values for key in arguments):
			room: Room = RoomController.get_room_by_id(values["room_id"])
			if room.get_player_by_email(values["user_email"]) is not None:
				for player in room.users:
					if player.nickname != values["nickname"]:
						player.queue_message(values["message"], values["nickname"])
				response = "OK"
			else:
				response = "PLAYER NOT IN ROOM"
		else:
			response = "WRONG ARGUMENTS"
		return response

	def get_messages(self, values: json, _) -> str:
		response: str = "ERROR"
		arguments: set = {"user_email", "room_id"}
		if all(key in values for key in arguments):
			room: Room = RoomController.get_room_by_id(values["room_id"])
			if room is not None:
				player: Player = room.get_player_by_email(values["user_email"])
				if player is not None:
					counter: int = 0
					response: dict = {}
					for message_struct in player.messages:
						response[str(counter)] = message_struct
						counter += 1
					response = str(json.dumps(response))
					player.clear_messages()
				else:
					response = "PLAYER NOT IN ROOM"
			else:
				response = "ROOM NOT FOUND"
		else:
			response = "WRONG ARGUMENTS"
		return response

	def get_sorted_deck(self, values: json, _) -> str:
		response: str = "ERROR"
		arguments: set = {"player_email", "room_id"}
		if all(key in values for key in arguments):
			room: Room = RoomController.get_room_by_id(values["room_id"])
			if room is not None:
				player: Player = room.get_player_by_email(values["player_email"])
				if player is not None:
					response = room.get_sorted_deck()
				else:
					response = "USER NOT IN ROOM"
			else:
				response = "WRONG ID"
		else:
			response = "WRONG ARGUMENTS"
		return response

	def get_users_in_room(self, values: json, _) -> str:
		response: str = "ERROR"
		if "room_id" in values:
			room: Room = RoomController.get_room_by_id(values["room_id"])
			if room is not None:
				counter: int = 0
				response: dict = {}
				for player in room.users:
					response[str(counter)] = {
						"nickname": player.nickname,
						"email": player.email
					}
					counter += 1
				response = str(json.dumps(response))
			else:
				response = "ROOM NOT FOUND"
		else:
			response = "WRONG ARGUMENTS"
		return response

	def save_score(self, values: json, _) -> str:
		response: str = "ERROR"
		arguments: set = {"user_email", "score", "room_id"}
		if all(key in values for key in arguments):
			room: Room = RoomController.get_room_by_id(values["room_id"])
			if room is not None:
				player: Player = room.get_player_by_email(values["user_email"])
				if player is not None:
					player.current_score = values["score"]
					player.score = values["score"]
					player.score += Player.get_score_by_email(values["user_email"])
					player.save()
					response = "OK"
				else:
					response = "PLAYER NOT IN ROOM"
			else:
				response = "ROOM NOT FOUND"
		else:
			response = "WRONG ARGUMENTS"
		return response

	def start_party(self, values: json, _) -> str:
		response: str = "ERROR"
		arguments: set = {"user_email", "room_id"}
		if all(key in values for key in arguments):
			room: Room = RoomController.get_room_by_id(values["room_id"])
			if room is not None:
				if room.creator.email == values["user_email"]:
					room.has_started = True
					response = "OK"
				else:
					response = "PLAYER IS NOT CREATOR"
			else:
				response = "ROOM NOT FOUND"
		else:
			response = "WRONG ARGUMENTS"
		return response

	def stop_party(self, values: json, _) -> str:
		response = "ERROR"
		arguments: set = {"user_email", "room_id"}
		if all(key in values for key in arguments):
			room: Room = RoomController.get_room_by_id(values["room_id"])
			if room is not None:
				if room.creator.email == values["user_email"]:
					room.has_started = False
					response = "OK"
				else:
					response = "USER IS NOT CREATOR"
			else:
				response = "ROOM NOT FOUND"
		else:
			response = "WRONG ARGUMENTS"
		return response

	def is_party_on(self, values: json, _) -> str:
		response: str = "ERROR"
		arguments: set = {"user_email", "room_id"}
		if all(key in values for key in arguments):
			room: Room = RoomController.get_room_by_id(values["room_id"])
			if room is not None:
				if room.get_player_by_email(values["user_email"]) is not None:
					response = "ON" if room.has_started else "OFF"
				else:
					response = "PLAYER NOT IN ROOM"
			else:
				response = "ROOM NOT FOUND"
		else:
			response = "WRONG ARGUMENTS"
		return response

	def kick_player(self, values: json, _) -> str:
		response: str = "ERROR"
		arguments: set = {"user_email", "room_id", "kicked_nickname"}
		if all(key in values for key in arguments):
			room: Room = RoomController.get_room_by_id(values["room_id"])
			if room is not None:
				kicking_player: Player = room.get_player_by_email(values["user_email"])
				if kicking_player is not None:
					player_to_kick: Player = room.get_player_by_nickname(values["kicked_nickname"])
					if player_to_kick is not None:
						if kicking_player not in player_to_kick.kicked_by:
							player_to_kick.kicked_counter += 1
							response = "OK"
						else:
							response = "ALREADY VOTED"
					else:
						response = "KICKED PLAYER NOT IN ROOM"
				else:
					response = "PLAYER NOT IN ROOM"
			else:
				response = "ROOM NOT FOUND"
		else:
			response = "WRONG ARGUMENTS"
		return response

	def get_kicked_players(self, values: json, _) -> str:
		response: str = "ERROR"
		arguments: set = {"user_email", "room_id"}
		if all(key in values for key in arguments):
			room: Room = RoomController.get_room_by_id(values["room_id"])
			if room is not None:
				if room.get_player_by_email(values["user_email"]) is not None:
					response: dict = {}
					for player in room.users:
						response[player.email] = "False"
						if player.kicked_counter > (len(room.users) / 2):
							response[player.email] = "True"
						else:
							response[player.email] = "False"
					response = str(json.dumps(response))
				else:
					response = "PLAYER NOT IN ROOM"
			else:
				response = "ROOM NOT FOUND"
		else:
			response = "WRONG ARGUMENTS"
		return response

	def won_round(self, values: json, _) -> str:
		response: str = "ERROR"
		arguments: set = {"user_email", "room_id", "score"}
		if all(key in values for key in arguments):
			room: Room = RoomController.get_room_by_id(values["room_id"])
			if room is not None:
				player: Player = room.get_player_by_email(values["user_email"])
				if player is not None:
					player.score = Player.get_score_by_email(values["user_email"])
					player.score += int(values["score"])
					player.current_score = int(values["score"])
					player.save()
					if room.winner is None:
						room.winner = player
						response = "OK"
					else:
						response = "NOT WON"
				else:
					response = "PLAYER NOT IN ROOM"
			else:
				response = "ROOM NOT FOUND"
		else:
			response = "WRONG ARGUMENTS"
		return response

	def there_is_a_winner(self, values: json, _) -> str:
		response: str = "ERROR"
		arguments: set = {"room_id"}
		if all(key in values for key in arguments):
			room: Room = RoomController.get_room_by_id(values["room_id"])
			if room is not None:
				if room.winner is None:
					response = "NO WINNER"
				else:
					response = room.winner.nickname
			else:
				response = "ROOM NOT FOUND"
		else:
			response = "WRONG ARGUMENTS"
		return response

	def in_room(self, values: json, _) -> str:
		response: str = "ERROR"
		arguments: set = {"user_email", "room_id"}
		if all(key in values for key in arguments):
			room: Room = RoomController.get_room_by_id(values["room_id"])
			if room is not None:
				response = "PLAYER NOT IN ROOM"
				if room.get_player_by_email(values["user_email"]) is not None:
					response = "OK"
			else:
				response = "ROOM NOT FOUND"
		else:
			response = "WRONG ARGUMENTS"
		return response

	@staticmethod
	def get_room_by_id(id: str) -> Room or None:
		response_room: Room or None = None
		for room in RoomController.rooms:
			if room.id == id:
				response_room = room
				break
		return response_room

	@staticmethod
	def exists_by_creator(user_email: str) -> bool:
		exists: bool = False
		for room in RoomController.rooms:
			if room.creator.email == user_email:
				exists = True
				break
		return exists
