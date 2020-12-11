import json
from socket import socket
from time import sleep

from Model.Mailer import Mailer
from Model.Player import Player
from Util.Util import remove_key, md5


class PlayerController:
	connected_clients = []

	def sign_up(self, values: json, _) -> str:
		response: str = "Error"
		required_values: set = {"name", "lastname", "nickname", "email", "password", "code"}
		if all(key in values for key in required_values):
			if values["code"] == PlayerController.get_code_from_email(values["email"]):
				new_player: Player = Player(
					values["name"],
					values["lastname"],
					values["nickname"],
					values["email"],
					values["password"]
				)
				response = new_player.register()
			else:
				response = "WRONG CODE"
		else:
			response = "WRONG ARGUMENTS"
		return response

	def login(self, player: json, connection_values: dict) -> str:
		response: str = "ERROR"
		if 'email' in player and 'password' in player:
			new_player: Player = Player.get_by_email(player['email'])
			if Player.is_registered(player['email']):
				if new_player.login():
					response = "OK"
					user: dict = {
						"email": player["email"],
						"connection": connection_values["connection"],
						"address": connection_values["address"]
					}
					PlayerController.watch_user(user)
				else:
					response = "WRONG PASSWORD"
			else:
				response = "EMAIL NOT REGISTERED"
		return response

	def logout(self, player: json, _) -> str:
		response: str = "ERROR"
		if "email" in player:
			PlayerController.unwatch_user(player["email"])
			response = "OK"
		return response

	def delete_user(self, values: json, _) -> str:
		response: str = "ERROR"
		if "email" in values:
			player: Player = Player.get_by_email(values["email"])
			if player.delete():
				PlayerController.unwatch_user(values["email"])
				response = "OK"
		else:
			response = "WRONG ARGUMENTS"
		return response

	def get_user(self, values: json, _) -> str:
		response: str = "ERROR"
		if "email" in values:
			if Player.is_registered(values["user_email"]):
				player: Player = Player.get_by_email(values["email"])
				player_values: dict = {
					"name": player.name,
					"lastname": player.lastname,
					"email": player.email,
					"password": player.password
				}
				response = str(json.dumps(player_values))
				print(response)
			else:
				response = "PLAYER NOT FOUND"
		else:
			response = "WRONG ARGUMENTS"
		return response

	@staticmethod
	def watch_user(watchable_user: dict) -> None:
		is_watched: bool = False
		for connected_user in PlayerController.connected_clients:
			if connected_user["email"] == watchable_user["email"]:
				is_watched = True
				break
		if not is_watched:
			PlayerController.connected_clients.append(watchable_user)

	@staticmethod
	def unwatch_user(email: str) -> None:
		for user in PlayerController.connected_clients:
			if user["email"] == email:
				PlayerController.connected_clients.remove(user)
				break

	@staticmethod
	def get_connection_by_email(email: str) -> socket:
		connection: socket or None = None
		for user in PlayerController.connected_clients:
			if user["email"] == email:
				connection = user["connection"]
				break
		return connection

	@staticmethod
	def get_email_by_address(address: str) -> str:
		email: str = ""
		for user in PlayerController.connected_clients:
			if user["address"] == address:
				email = user["email"]
				break
		return email

	@staticmethod
	def send(email: str, message: str) -> None:
		sleep(5)

		connection: socket = PlayerController.get_connection_by_email(email)
		connection.send(message.encode())
		PlayerController.unwatch_user(email)

	@staticmethod
	def send_message(message: dict) -> None:
		required_values: set = {"room_id", "sender", "message", "receiver"}
		if all(key in message for key in required_values):
			connection: socket = PlayerController.get_connection_by_email(message["receiver"])
			values: dict = remove_key(message, "receiver")
			connection.send(str(values).encode())

	@staticmethod
	def get_code_from_email(email: str) -> str:
		return md5(email)[0:5]

	def send_code_to_email(self, values: json, _) -> str:
		response: str
		if "email" in values:
			code: str = PlayerController.get_code_from_email(values["email"])
			# TODO
			# message: str = get_message_from_file("Configuration/messages.json", "new_user")
			# message = message.replace("{}", code)
			message = code
			mail: Mailer = Mailer()
			mail.login_from_file()
			response = mail.send(values["email"], message)
		else:
			response = "EMAIL NOT SET"
		return response

	def get_top_ten(self, a, _) -> str:
		return Player.get_top_ten()
