import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("localhost", int(input())))
s.listen(1)
conn, addr = s.accept()
print(conn.proto)
print(conn.type)
    
