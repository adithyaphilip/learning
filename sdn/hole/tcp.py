import socket

own_port = int(input())
ip, op_port = input().split()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("", own_port))
print(s.getsockname())
s.connect((ip, int(op_port)))
s.close()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("", own_port))
s.listen(5)
print(s.getsockname())
conn, addr = s.accept()
print(conn)
