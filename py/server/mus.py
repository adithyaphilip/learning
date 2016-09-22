import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("localhost", int(input())))

msg, addr = s.recvfrom(4096)
print(msg.decode(), addr)
s.sendto("lolpop".encode("utf-8"), addr)
s.close()
