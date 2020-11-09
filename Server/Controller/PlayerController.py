import json

from Model.Player import Player


class PlayerController:
	def save_user(self, player: json, _) -> str:
		response = "Error"
		if len(player) == 5:
			new_player: Player = Player(
				player["name"],
				player["last_name"],
				player["nickname"],
				player["email"],
				player["password"]
			)
			response = str(new_player.register())
		return response

	def login(self, player: json, _) -> str:
		response = "Error"
		if 'email' in player and 'password' in player:
			new_player: Player = Player.get_by_email(player['email'])
			if new_player.login():
				response = "OK"
		return response

	def delete_user(self, player: json, _) -> str:
		response = "Error"
		if 'email' in player:
			player: Player = Player.get_by_email(player['email'])
			if player.delete():
				response = "OK"
		return response
