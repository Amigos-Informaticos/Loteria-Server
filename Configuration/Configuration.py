import socket

local = "Configuration/local.json"

remote = "Configuration/connection.json"


def get_connection_file() -> str:
	ip = socket.gethostbyname(socket.gethostname()).split(".")[-1]
	if ip == "99":
		return local
	return remote
