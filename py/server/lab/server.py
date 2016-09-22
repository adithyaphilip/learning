from socket import *
import pickle

s = socket(AF_INET, SOCK_STREAM)
s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
s.bind(("127.0.0.1", 3125))
s.listen(5)
try:
    while True:
        conn, addr = s.accept()
        data = pickle.loads(conn.recv(2048))
        sw = {"rev":lambda x: ''.join(reversed(list(x))),"cap": str.upper, "encr":lambda x: ''.join([chr(ord(i)+1) for i in x]), "end":lambda x: s.close}
        print(data)
        result = sw.get(data[0], lambda x: "Invalid Operation")(data[1])
        print(result)
        conn.send(bytes(result,"utf-8"))
except Exception as e:
    print(e)
    s.close()
s.close()
