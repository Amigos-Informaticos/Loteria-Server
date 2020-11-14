import inspect
import json
import socket
import threading
from json import JSONDecodeError

from Server.Controller.PlayerController import PlayerController


class Server(PlayerController):
	def __init__(self, configuration: dict):
		super().__init__()

		if all(key in configuration for key in ("host", "port", "capacity")):
			self.host: str = configuration["host"]
			self.port: int = configuration["port"]
			self.capacity: int = configuration["capacity"]

		elif "config_file" in configuration:
			self.prepare_from_file(configuration["config_file"])

		self.threads: list = []
		self.methods: list = []
		self.tcp_socket: socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		print(f"Host set to: {self.host}")
		print(f"Port set to: {self.port}")

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
		print(f"Socket listening on {self.host}:{self.port} with capacity for {self.capacity}")

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
				print(Error)

	def serve(self, connection, address):
		print(f"Connected from: {address[0]}")
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
			print(f"Unexpected disconnection from {address}")
		print(f"{address} disconnected")

	def ping(self, message: json, _) -> str:
		return message['message']

	# TODO eliminar metodo
	def after_ping(self, values: dict, connection: dict) -> str:
		response: str = "Error"
		if "email" in values:
			user: dict = {
				"email": values["email"],
				"connection": connection["connection"],
				"address": connection["address"]
			}
			PlayerController.watch_user(user)
			t1 = threading.Thread(target=PlayerController.send, args=values.values())
			t1.start()
			response = "OK"
		return response
