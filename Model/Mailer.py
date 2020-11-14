import json
import ssl
from smtplib import SMTP
from ssl import SSLContext


class Mailer:
	def __init__(self, port: int = 587, server: str = "smtp.gmail.com"):
		self.port: int = port
		self.server_address: str = server
		self.recipients = []
		self.prepare()

	def login(self, address: str, password: str) -> None:
		self.address = address
		self.password = password

	def login_from_file(self, file_path: str = "Configuration/mail_config.json"):
		with open(file_path) as json_file:
			data = json.load(json_file)
			self.address = data["address"]
			self.password = data["password"]

	def prepare(self) -> SMTP:
		context: SSLContext = ssl.create_default_context()
		server: SMTP = SMTP(self.server_address, self.port)
		server.starttls(context=context)
		return server

	def add_recipient(self, receiver_address: str) -> None:
		if receiver_address not in self.recipients:
			self.recipients.append(receiver_address)

	def clear_recipients(self) -> None:
		self.recipients = []

	def send(self, receiver: str, message: str) -> bool:
		response: bool = False
		server: SMTP = self.prepare()
		server.login(self.address, self.password)
		server.sendmail(self.address, receiver, message)
		return response

	def sent_to_all(self, message: str, delete_recipients_on_send: bool = False) -> None:
		for receier in self.recipients:
			self.send(receier, message)
		if delete_recipients_on_send:
			self.clear_recipients()
