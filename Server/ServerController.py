import inspect

from Server.Controller.RoomController import RoomController


class ServerController:
	def list_methods(self) -> None:
		for method in inspect.getmembers(self, predicate=inspect.ismethod):
			print(method.__str__())

	def view_rooms(self):
		for room in RoomController.rooms:
			print(room.id)
