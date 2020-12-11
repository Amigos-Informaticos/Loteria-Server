import abc

from Server.Controller.PlayerController import PlayerController
from Server.Controller.RoomController import RoomController


class IServer(abc.ABCMeta, PlayerController, RoomController):
	def __init__(self):
		super().__init__()

	@abc.abstractmethod
	def run(self) -> None:
		pass

	@abc.abstractmethod
	def load_methods(self) -> None:
		pass

	@abc.abstractmethod
	def prepare_from_file(self, file_path: str) -> None:
		pass

	@abc.abstractmethod
	def prepare(self, activate: bool = False) -> None:
		pass

	@abc.abstractmethod
	def activate(self) -> None:
		pass

	@abc.abstractmethod
	def init_cycle(self) -> None:
		pass

	@abc.abstractmethod
	def serve(self, connection, address) -> None:
		pass

	@abc.abstractmethod
	def close_all(self) -> None:
		pass
