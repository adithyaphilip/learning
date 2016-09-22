import socket

s = socket.socket(type=socket.SOCK_DGRAM)
s.sendto(input().encode("utf-8"), ("localhost", int(input())))
msg, addr = s.recvfrom(2)
print(msg)
s.close()
