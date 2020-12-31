import json

from Model.GameMode import GameMode


class GameModeController:
	def save_pattern(self, values: json, _) -> str:
		response: str = "ERROR"
		arguments: set = {"game_mode_name", "pattern", "user_email"}
		if all(key in values for key in arguments):
			game_mode: GameMode = GameMode(
				values["game_mode_name"],
				values["user_email"]
			)
			response = game_mode.save_pattern(values["pattern"])
		else:
			response = "WRONG ARGUMENTS"
		return response

	def get_patterns(self, values: json, _) -> str:
		response: str = "ERROR"
		arguments: set = {"game_mode_name", "user_email"}
		if all(key in values for key in arguments):
			if GameMode.is_registered(values["game_mode_name"], values["user_email"]):
				game_mode: GameMode = GameMode.get_by_user(values["user_email"])
				boards: list or None = game_mode.get_boards()
				if boards is not None:
					patterns: dict = {}
					counter: int = 0
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
			game_modes: list or None = GameMode.get_by_user(values["user_email"])
			if game_modes is not None:
				response: dict = {}
				counter: int = 0
				for game_mode in game_modes:
					response[counter] = game_mode.name
					counter += 1
				response = str(json.dumps(response))
			else:
				response = "NO GAME MODE REGISTERED"
		else:
			response = "WRONG ARGUMENTS"
		return response
