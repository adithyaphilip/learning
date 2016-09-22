import socket as skt
import pickle
s = skt.socket(skt.AF_INET, skt.SOCK_DGRAM)
s.bind(("127.0.0.1",int(input())))
while True:
    data, addr = s.recvfrom(4096)
    t = pickle.loads(data)
    print(t)
    sw = {"rev":lambda x: "".join(reversed(x)), "cap":lambda x: x.upper(), "encr":lambda x: "".join(map(lambda x: chr(ord(x)+1), x))}
    s.sendto(sw.get(t[0], lambda x: "Invalid Operatio!")(t[1]).encode("utf-8"), addr)

