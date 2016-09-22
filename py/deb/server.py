import socket

HOST = '10.2.22.52'
PORT = 9090

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(10)
cs, addr = s.accept()
while True:
    data = cs.recv(2048)
    print(data.decode("utf-8"))


