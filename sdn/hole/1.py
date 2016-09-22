import socket

own_port = int(input())
ip, op_port = input().split()

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("", own_port))
print(s.getsockname())
while (True):
    s.sendto(str(s.getsockname()).encode("utf-8"), (ip, int(op_port)))
    data, addr = s.recvfrom(1024)
    ip, op_port = addr
    print(data, addr)
