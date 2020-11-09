import inspect
import json
import socket
import threading
from json import JSONDecodeError

from Server.Controller.PlayerController import PlayerController as Player


class Server(Player):
	def __init__(self, host: str = '', port: int = 42069):
		self.host = host
		self.port = port
		self.threads = []
		self.methods = []
		self.connected_clients = []
		self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		print(f"Host set to: {host}")
		print(f"Port set to: {port}")

	def run(self, capacity: int = 10):
		self.load_methods()
		self.prepare()
		self.activate(capacity)
		self.init_cycle()

	def load_methods(self):
		for method in inspect.getmembers(self, predicate=inspect.ismethod):
			self.methods.append(method[0])

	def prepare(self, activate: bool = False):
		self.tcp_socket.bind((self.host, self.port))
		if activate:
			self.activate()

	def activate(self, capacity: int = 10):
		self.tcp_socket.listen(capacity)
		print(f"Socket listening on {self.host}:{self.port} with capacity for {capacity}")

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
		print(f"Connected from: {address}")
		try:
			received = connection.recv(1024)
			received = json.loads(received.decode("utf-8"))
			method = received["Method"]
			args = received["Arguments"]
			while method != "close":
				if method in self.methods:
					response = getattr(self, method)(args, {connection, address})
					connection.send(response.encode())

					received = connection.recv(1024)
					received = json.loads(received.decode("utf-8"))
					method = received["Method"]
					args = received["Arguments"]
				else:
					connection.send("Method not supported".encode())
			if method == "close":
				connection.close()
				if {connection, address} in self.connected_clients:
					self.connected_clients.remove({connection, address})
		except JSONDecodeError:
			print(f"Unexpected disconnection from {address}")
		print(f"{address} disconnected")

	def ping(self, message: json, _) -> str:
		return message['message']

	def make_room(self, player: json) -> str:
		response = str(False)
		if len(player) == 5:
			pass
		return response
