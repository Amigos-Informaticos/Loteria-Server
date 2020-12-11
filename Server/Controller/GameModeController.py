import json

from Model.GameMode import GameMode


class GameModeController:
	def save_pattern(self, values: json, _) -> str:
		response: str = "ERROR"
		arguments: set = {"game_mode_name", "pattern", "user_email"}
		if all(key in values for key in arguments):
			game_mode: GameMode = GameMode.get_by_name_and_user(
				values["game_mode_name"],
				values["user_email"]
			)
			if game_mode is not None:
				response = game_mode.save_pattern(values["pattern"])
				response = "OK"
			else:
				response = "GAME NOT REGISTERED"
		else:
			response = "WRONG ARGUMENTS"
		return response

	def get_patterns(self, values: json, _) -> str:
		response: str = "ERROR"
		arguments: set = {"game_mode_name", "user_email"}
		if all(key in values for key in arguments):
			if GameMode.is_registered(values["game_mode_name"]):
				game_mode: GameMode = GameMode.get_by_name(values["game_mode_name"])
				boards: list or None = game_mode.get_boards()
				if boards is not None:
					patterns: dict = {}
					counter = 0
					for board in boards:
						patterns[counter] = {
							"pattern": board.pattern
						}
						counter = counter + 1
					response = str(json.dumps(patterns))
				else:
					response = "NOT RELATED PATTERNS"
			else:
				response = "GAME MODE NOT REGISTERED"
		else:
			response = "WRONG ARGUMENTS"
		return response

	def get_game_modes_by_user(self, values: json, _) -> str:
		response: str = "ERROR"
		if "user_email" in values:
			pass
		else:
			response = "WRONG ARGUMENTS"
		return response
