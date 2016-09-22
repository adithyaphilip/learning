from socket import *
import pickle

for i in [("rev", "hello"), ("encr", "bye"), ("cap", "lower"), ("kuch", "lol")]:
    s = socket(AF_INET, SOCK_STREAM)
    s.connect(("127.0.0.1", 3125))
    s.send(pickle.dumps(i))
    print(str(s.recv(2048), "utf-8"))
    s.close()

