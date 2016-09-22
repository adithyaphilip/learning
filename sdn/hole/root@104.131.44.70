import socket

own_port = int(input())

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("", own_port))
print(s.getsockname())
while (True):
    data, addr = s.recvfrom(1024)
    print(data, addr)
