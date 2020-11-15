import json
from socket import socket
from time import sleep

from Model.Mailer import Mailer
from Model.Player import Player
from Util.Util import remove_key, get_message_from_file, md5


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
				response = str(new_player.register())
			else:
				response = "WRONG CODE"
		return response

	def login(self, player: json, connection_values: dict, _) -> str:
		response: str = "Error"
		if 'email' in player and 'password' in player:
			new_player: Player = Player.get_by_email(player['email'])
			if new_player.login():
				response = "OK"
				user: dict = {
					"email": player["email"],
					"connection": connection_values["connection"],
					"address": connection_values["address"]
				}
				PlayerController.watch_user(user)
		return response

	def logout(self, player: json, _) -> str:
		response: str = "Error"
		if "email" in player:
			PlayerController.unwatch_user(player["email"])
			response = "OK"
		return response

	def delete_user(self, player_email: str, _) -> str:
		response: str = "Error"
		if player_email is not None:
			player: Player = Player.get_by_email(player_email)
			if player.delete():
				PlayerController.unwatch_user(player_email)
				response = "OK"
		return response

	@staticmethod
	def watch_user(user: dict) -> None:
		if user not in PlayerController.connected_clients:
			PlayerController.connected_clients.append(user)

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
		response: str = "ERROR"
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
