from Server.Server import Server

CONFIGURATION: dict = {
	"config_file": "Configuration/connection.json"
}

if __name__ == "__main__":
	server = Server(CONFIGURATION)
	server.run()
