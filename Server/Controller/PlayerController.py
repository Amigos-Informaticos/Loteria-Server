import json
from socket import socket
from time import sleep

from Model.Mail import Mail
from Model.Player import Player
from Util.Util import remove_key, md5


class PlayerController:
	connected_clients = []

	def sign_up(self, values: json, _) -> str:
		response: str = "Error"
		arguments: set = {"name", "lastname", "nickname", "email", "password", "code"}
		if all(key in values for key in arguments):
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

	def login(self, values: json, _) -> str:
		response: str = "ERROR"
		arguments: set = {"email", "password"}
		if all(key in values for key in arguments):
			new_player: Player = Player.get_by_email(values['email'])
			if Player.is_registered(values['email']):
				if new_player.login(values["email"], values["password"]):
					response = "OK"
				else:
					response = "WRONG PASSWORD"
			else:
				response = "EMAIL NOT REGISTERED"
		else:
			response = "WRONG ARGUMENTS"
		return response

	def logout(self, player: json, _) -> str:
		response: str = "ERROR"
		if "email" in player:
			PlayerController.unwatch_user(player["email"])
			response = "OK"
		else:
			response = "WRONG ARGUMENTS"
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
		if "user_email" in values:
			if Player.is_registered(values["user_email"]):
				player: Player = Player.get_by_email(values["user_email"])
				player_values: dict = {
					"name": player.name,
					"lastname": player.lastname,
					"email": player.email,
					"password": player.password,
					"nickname": player.nickname,
					"score": str(player.score)
				}
				response = str(json.dumps(player_values))
			else:
				response = "PLAYER NOT FOUND"
		else:
			response = "WRONG ARGUMENTS"
		return response

	def save_score(self, values: json, _) -> str:
		response: str = "ERROR"
		arguments: set = {"user_email", "score"}
		if all(key in values for key in arguments):
			player: Player = Player.get_by_email(values["user_email"])
			if player is not None:
				Player.add_score(int(values["score"]), values["user_email"])
				response = "OK"
			else:
				response = "PLAYER NOT FOUND"
		else:
			response = "WRONG ARGUMENTS"
		return response

	def change_password(self, values: json, _) -> str:
		response: str = "ERROR"
		arguments: set = {"user_email", "old_password", "new_password"}
		if all(key in values for key in arguments):
			if Player.is_registered(values["user_email"]):
				player: Player = Player.get_by_email(values["user_email"])
				if player.password == values["old_password"]:
					Player.change_password(
						values["user_email"],
						values["new_password"])
					response = "OK"
				else:
					response = "WRONG OLD PASSWORD"
			else:
				response = "PLAYER NOT FOUND"
		else:
			response = "WRONG ARGUMENTS"
		return response

	def send_code_to_email(self, values: json, _) -> str:
		response: str
		if "email" in values:
			code: str = PlayerController.get_code_from_email(values["email"])
			mail: Mail = Mail()
			mail.login_from_file()
			response = mail.send(values["email"], code)
		else:
			response = "EMAIL NOT SET"
		return response

	def get_top_ten(self, a, _) -> str:
		return Player.get_top_ten()

	def unwatch_by_connection(self, connection: socket) -> bool:
		response: bool = False
		for connected_user in PlayerController.connected_clients:
			if connected_user["connection"] == connection:
				PlayerController.connected_clients.remove(connected_user)
				response = True
				break
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
		arguments: set = {"room_id", "sender", "message", "receiver"}
		if all(key in message for key in arguments):
			connection: socket = PlayerController.get_connection_by_email(message["receiver"])
			values: dict = remove_key(message, "receiver")
			connection.send(str(values).encode())

	@staticmethod
	def get_code_from_email(email: str) -> str:
		return md5(email)[0:5]
