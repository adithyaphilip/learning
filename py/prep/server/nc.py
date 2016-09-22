import socket as sk
import pickle
l = [("rev", "hello"), ("cap", "hello"), ("encr", "hello"), ("random", "hello")]
port = int(input())
for i in l:
    s = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
    s.sendto(pickle.dumps(i), ("localhost", port))
    print(s.recv(4096).decode())
    s.close()
