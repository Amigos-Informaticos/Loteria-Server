from Server.Controller.RoomController import RoomController


class ServerController:
	def view_rooms(self):
		for room in RoomController.rooms:
			print(room.)