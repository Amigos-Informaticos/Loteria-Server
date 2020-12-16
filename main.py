from Server.Controller.RoomController import RoomController
from Server.Server import Server

CONFIGURATION: dict = {
	"config_file": "Configuration/connection.json"
}

if __name__ == "__main__":
	server = Server(CONFIGURATION)
	response = RoomController.make_room(
		server,
		{
			"creator_email": "alexisao@hotmail.com",
			"rounds": "1",
			"speed": "1",
			"players": "3",
			"game_mode": "Hardcore mode"
		},
		{
			"connection": "connection",
			"address": "address"
		}
	)
	print(response)
	server.run()
