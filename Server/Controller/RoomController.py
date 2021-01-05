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
							"game_mode_id": room.game_mode.idGameMode,
							"available_spaces:": str(room.users_limit - len(room.users))
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
				if room.creator.email == configuration["user_email"]:
					room.empty_room()
				else:
					room.remove_user(configuration["user_email"])
					if room.is_empty():
						self.rooms.remove(room)
				response = "OK"
			else:
				response = "ROOM NOT FOUND"
		else:
			response = "WRONG ARGUMENTS"
		return response

	def send_message(self, values: json, _) -> str:
		response: str = "ERROR"
		arguments: set = {"message", "nickname", "room_id"}
		if all(key in values for key in arguments):
			room: Room = RoomController.get_room_by_id(values["room_id"])
			for player in room.users:
				if player.nickname != values["nickname"]:
					player.queue_message(values["message"])
			response = "OK"
		return response

	def get_messages(self, values: json, _) -> str:
		response: str = "ERROR"
		arguments: set = {"user_email", "room_id"}
		if all(key in values for key in arguments):
			room: Room = RoomController.get_room_by_id(values["room_id"])
			player: Player = room.get_player_by_email(values["user_email"])
			if player is not None:
				counter: int = 0
				response: dict = {}
				for message in player.messages:
					response[str(counter)] = message
					counter += 1
				response = str(json.dumps(response))
			else:
				response = "PLAYER NOT IN ROOM"
		else:
			response = "WRONG ARGUMENTS"
		return response

	def get_sorted_deck(self, values: json, _) -> str:
		response: str = "ERROR"
		arguments: set = {"player_email", "room_id"}
		if all(key in values for key in arguments):
			room: Room = RoomController.get_room_by_id(values["room_id"])
			if room is not None:
				player: Player = Player.get_by_email(values["player_email"])
				if player in room.users:
					response = room.get_sorted_deck()
				else:
					response = "USER NOT IN ROOM"
			else:
				response = "WRONG ID"
		else:
			response = "WRONG ARGUMENTS"
		return response

	def set_user_ready(self, values: json, _) -> str:
		response: str = "ERROR"
		arguments: set = {"room_id", "user_email"}
		if all(key in values for key in arguments):
			if Player.is_registered(values["user_email"]):
				if RoomController.get_room_by_id(values["room_id"]) is not None:
					room: Room = RoomController.get_room_by_id(values["room_id"])
					player_found: bool = False
					for player in room.users:
						if player.email == values["user_email"]:
							player.is_ready = True
							player_found = True
							break
					if player_found:
						response = "OK"
					else:
						response = "PLAYER NOT IN ROOM"
				else:
					response = "WRONG ID"
			else:
				response = "PLAYER NOT REGISTERED"
		else:
			response = "WRONG ARGUMENTS"
		return response

	def get_users_in_room(self, values: json, _) -> str:
		response: str = "ERROR"
		if "room_id" in values:
			room: Room = RoomController.get_room_by_id(values["room_id"])
			response: dict = {}
			counter: int = 0
			for player in room.users:
				is_ready: str = "T" if player.is_ready else "F"
				response[str(counter)] = {
					"nickname": player.nickname,
					"email": player.email,
					"is_ready": is_ready
				}
				counter += 1
			response = str(json.dumps(response))
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
