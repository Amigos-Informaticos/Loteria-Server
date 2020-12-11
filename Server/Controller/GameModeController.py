import json

from Model.GameMode import GameMode


class GameModeController:
	def save_pattern(self, values: json, _) -> str:
		response: str = "ERROR"
		required_values: set = {"game_mode_name", "pattern", "user_email"}
		if all(key in values for key in required_values):
			game_mode: GameMode = GameMode(
				values["game_mode_name"],
				values["user_email"]
			)
			response = game_mode.save_pattern(values["pattern"])
		else:
			response = "WRONG ARGUMENTS"
		return response
