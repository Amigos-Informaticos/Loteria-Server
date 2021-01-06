import json

import requests

CONFIGURATION_PATH = "Configuration/TelegramBotConfig.json"


class TelegramBot:
	def __init__(self, groupId: str):
		self.groupId = groupId
		self.messages: list = []
		self.load_configuration()

	def load_configuration(self, configuration_path: str = CONFIGURATION_PATH) -> None:
		with open(configuration_path) as file:
			values: dict = json.load(file)
			if "url" in values:
				self.url = values["url"]
				self.complete_url = self.url + self.groupId + "&text="

	def add_message(self, message: str) -> None:
		self.messages.append(message + "\n")

	def send(self, message: str = None) -> None:
		if message is None and len(self.messages) > 0:
			for single_message in self.messages:
				payload = self.complete_url + single_message
			self.messages.clear()
		else:
			payload = self.complete_url + message
		requests.get(payload)
