import inspect

from Server.Controller.RoomController import RoomController


class ServerController:
	def list_methods(self) -> None:
		for method in inspect.getmembers(self, predicate=inspect.ismethod):
			print(method.__str__())

	def view_rooms(self) -> None:
		for room in RoomController.rooms:
			print(room.id)

	def view_players_per_room(self) -> None:
		for room in RoomController.rooms:
			print(room.id)
			for player in room.users:
				print(player.email)
			print("")