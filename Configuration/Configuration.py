import socket

local = "Configuration/local.json"

remote = "Configuration/connection.json"


def get_connection_file() -> str:
	file = remote
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("8.8.8.8", 80))
	if str(s.getsockname()[0]).split(".")[-1] == "99":
		file = local
	return file
