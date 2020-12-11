import json

from Model.Player import Player
from Model.Room import Room
from Server.Controller.PlayerController import PlayerController


class RoomController:
	rooms = []

	def make_room(self, configuration: json, connection_values: dict) -> str:
		response: str = "ERROR"
		if "creator_email" in configuration:
			watchable_user: dict = {
				"email": configuration["creator_email"],
				"connection": connection_values["connection"],
				"address": connection_values["address"],
				"is_ready": False
			}
			PlayerController.watch_user(watchable_user)
			room: Room = Room(configuration["creator_email"])
			response = room.id
		return response

	def enter_room(self, configuration: json, connection_values: dict) -> str:
		response: str = "ERROR"
		arguments: set = {"room_id", "user_email"}
		if all(key in configuration for key in arguments):
			watchable_user: dict = {
				"email": configuration["user_email"],
				"connection": connection_values["connection"],
				"address": connection_values["address"],
				"is_ready": False
			}
			PlayerController.watch_user(watchable_user)
			if RoomController.get_room_by_id(configuration["room_id"]) is None:
				response = "WRONG ID"
			else:
				room: Room = RoomController.get_room_by_id(configuration["room_id"])
				room.add_user(configuration["user_email"])
				response = "OK"
		else:
			response = "WRONG ARGUMENTS"
		return response

	def exit_room(self, configuration: json, _) -> str:
		response: str = "ERROR"
		if "room_id" in configuration and "user_email" in configuration:
			room_id: str = configuration["room_id"]
			user: str = configuration["user_email"]
			room: Room = RoomController.get_room_by_id(room_id)
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
			player: Player = Player.get_by_email(values["player_email"])
			if player in room.users:
				response = room.get_sorted_deck()
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
				#room.
				else:
					response = "WRONG ID"
			else:
				response = "PLAYER NOT FOUND"
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
