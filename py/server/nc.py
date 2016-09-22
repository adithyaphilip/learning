import socket
from threading import Thread
from time import sleep
port = int(input())
while True:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    Thread(target = s.connect, args = (("localhost", port),)).start()
    #s.send("hello".encode("utf-8"))
    sleep(1)
    print("lol")
s.close()
