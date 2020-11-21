import inspect
import json
import socket
import threading
from json import JSONDecodeError

from Server.Controller.PlayerController import PlayerController
from Util.TelegramBot import TelegramBot


class Server(PlayerController):
	def __init__(self, configuration: dict):
		super().__init__()
		self.logger: TelegramBot = TelegramBot("W3Log")

		if all(key in configuration for key in ("host", "port", "capacity")):
			self.host: str = configuration["host"]
			self.port: int = configuration["port"]
			self.capacity: int = configuration["capacity"]

		elif "config_file" in configuration:
			self.prepare_from_file(configuration["config_file"])

		self.threads: list = []
		self.methods: list = []
		self.tcp_socket: socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.logger.add_message(f"Host set to: {self.host}")
		self.logger.add_message(f"Port set to: {self.port}")
		self.logger.send()

	def run(self) -> None:
		self.load_methods()
		self.prepare()
		self.activate()
		self.init_cycle()

	def load_methods(self) -> None:
		for method in inspect.getmembers(self, predicate=inspect.ismethod):
			self.methods.append(method[0])

	def prepare_from_file(self, file_path: str) -> None:
		with open(file_path) as json_file:
			data = json.load(json_file)
			self.host: str = data["address"]
			self.port: int = data["port"]
			if "capacity" in data:
				self.capacity: int = data["capacity"]
			else:
				self.capacity: int = 10

	def prepare(self, activate: bool = False) -> None:
		self.tcp_socket.bind((self.host, self.port))
		if activate:
			self.activate()

	def activate(self):
		self.tcp_socket.listen(self.capacity)
		self.logger.send(f"Listening on {self.port} with capacity for {self.capacity}")

	def init_cycle(self):
		while True:
			try:
				connection, address = self.tcp_socket.accept()
				new_thread = threading.Thread(target=self.serve, args=(connection, address))
				self.threads.append(new_thread)
				new_thread.start()
			except KeyboardInterrupt:
				exit("Interrupted")
			except Exception as Error:
				self.logger.send(str(Error))

	def serve(self, connection, address):
		self.logger.send(f"Connected from: {address[0]}")
		try:
			received = connection.recv(1024)
			received: json = json.loads(received.decode("utf-8"))
			method: str = received["Method"]
			arguments: json = received["Arguments"]

			while method != "close":
				if method in self.methods:
					connection_values: dict = {"connection": connection, "address": address}
					response = getattr(self, method)(arguments, connection_values)

					connection.send(response.encode())
					received = connection.recv(1024)
					received = json.loads(received.decode("utf-8"))
					method = received["Method"]
					arguments = received["Arguments"]
				else:
					connection.send("Method not supported".encode())
					received = connection.recv(1024)
					received = json.loads(received.decode("utf-8"))
					method = received["Method"]
					arguments = received["Arguments"]
			if method == "close":
				connection.close()
		except JSONDecodeError:
			self.logger.send(f"Unexpected disconnection from {address}")
		self.logger.send(f"{address} disconnected")

	def ping(self, message: json, _) -> str:
		return message['message']
