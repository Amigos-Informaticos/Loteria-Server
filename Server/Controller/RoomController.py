import json

from Model.Player import Player
from Model.Room import Room
from Server.Controller.PlayerController import PlayerController


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
						response: dict = {
							"speed": str(room.speed),
							"rounds": str(room.rounds),
							"game_mode": room.game_mode.name,
							"game_mode_id": room.game_mode.idGameMode,
							"available_spaces:": str(room.users_limit - len(room.users))
						}
						response = str(json.dumps(response))
						message: str = self.get_users_in_room(configuration, None)
						self.notify_joining_room(room, message)
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
		if "room_id" in configuration and "user_email" in configuration:
			room_id: str = configuration["room_id"]
			user: str = configuration["user_email"]
			room: Room = RoomController.get_room_by_id(room_id)
			if room is not None:
				room.remove_user(user)
				if room.is_empty():
					self.rooms.remove(room)
					response = "OK"
		return response

	def send_message(self, values: json, _) -> str:
		response: str = "ERROR"
		arguments: set = {"message", "sender", "room_id"}
		if all(key in values for key in arguments):
			room: Room = RoomController.get_room_by_id(values["room_id"])
			room.send_message(values)
			response = "OK"
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

	def notify_joining_room(self, room: Room, message: str) -> None:
		print(message)
		for player in room.users:
			print("A\t" + player.email)
			for subscribed_user in PlayerController.connected_clients:
				print("B\t" + subscribed_user["email"])
				if player.email == subscribed_user["email"]:
					subscribed_user["connection"].send(message.encode())
					print(message)
					break

	@staticmethod
	def get_room_by_id(id: str) -> Room or None:
		response_room: Room or None = None
		for room in RoomController.rooms:
			if room.id == id:
				print(room.id)
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
