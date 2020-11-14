import json

from Model.Room import Room
from Server.Controller.PlayerController import PlayerController


class RoomController:
	rooms = []

	def make_room(self, configuration: json, connection_values: dict) -> str:
		response: str = "Error"
		if "creator_email" in configuration:
			email: str = configuration["creator_email"]
			PlayerController.watch_user(email, connection_values)
			room: Room = Room(email)
			response = str({"Room_id": room.id})
		return response

	def exit_room(self, configuration: json, _) -> str:
		response: str = "Error"
		if "room_id" in configuration and "user_email" in configuration:
			room_id: str = configuration["room_id"]
			user: str = configuration["user_email"]
			room: Room = RoomController.get_room_by_id(room_id)
			room.remove_user(user)
		return response

	def send_message(self, values: json, _) -> str:
		response: str = ""
		required_values: set = {"message", "sender", "room_id"}
		if all(key in values for key in required_values):
			room: Room = RoomController.get_room_by_id(values["room_id"])
			room.send_message(values)
		return response

	@staticmethod
	def get_room_by_id(id: str) -> Room or None:
		response_room: Room or None = None
		for room in RoomController.rooms:
			if room.id == id:
				response_room = room
				break
		return response_room
