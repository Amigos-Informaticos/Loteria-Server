import json
import socket

LOCAL = "Configuration/local.json"

REMOTE = "Configuration/connection.json"


def get_connection_file() -> str:
	file = REMOTE
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("8.8.8.8", 80))
	if str(s.getsockname()[0]).split(".")[-1] == "99":
		file = LOCAL
	return file


def get_connection_path() -> str:
	with open(get_connection_file()) as json_connection:
		data = json.load(json_connection)
		connection_string: str = data['connection_path']
		connection_string += data['user'] + ":"
		connection_string += data['password'] + "@"
		connection_string += data['host'] + '/'
		connection_string += data['database']
	return connection_string
