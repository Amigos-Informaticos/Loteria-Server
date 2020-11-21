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

	def add_message(self, message: str) -> None:
		self.messages.append(message + "\n")

	def send(self, message: str = None) -> None:
		complete_url = self.url + self.groupId + "&text="
		if message is None:
			for single_message in self.messages:
				complete_url = complete_url + single_message
			self.messages: list = []
		else:
			complete_url = complete_url + message
		requests.get(complete_url)
