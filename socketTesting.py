import selectors
import socket
import types

live_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

selector = selectors.DefaultSelector()


def accept_con(socket: socket.socket):
	connection, address = socket.accept()
	print(f"{address} connected")
	connection.setblocking(False)
	data = types.SimpleNamespace(addr=address, inb=b'', out=b'')
	events = selectors.EVENT_READ | selectors.EVENT_WRITE
	selector.register(connection, events, data=data)


def service_con(key, mask):
	sock: socket.socket = key.fileobj
	data = key.data
	if mask & selectors.EVENT_READ:
		received = sock.recv(1024)
		if received:
			data.outb += received
		else:
			print(f"Closing {data.addr}")
			selector.unregister(sock)
			sock.close()
	if mask & selectors.EVENT_WRITE:
		if data.outb:
			print(f"From {repr(data.outb)} to {data.addr}")
			sent = sock.send(data.outb)
			data.outb = data.outb[sent:]


if __name__ == '__main__':
	host = socket.gethostname()
	port = 12345
	tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	tcp_socket.setblocking(False)
	tcp_socket.bind((host, port))
	tcp_socket.listen()
	print(f"Open socket on {host}:{port}")
	tcp_socket.setblocking(False)
	selector.register(tcp_socket, selectors.EVENT_READ, data=None)

	while tcp_socket:
		events = selector.select(timeout=None)
		for key, mask in events:
			if key.data is None:
				accept_con(key.fileobj)
			else:
				service_con(key, mask)
		tcp_socket.close()
	print("Connection ended")
