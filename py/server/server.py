import os
import socket
from time import sleep
s = socket.socket()
s.bind(("0.0.0.0", 8125))
s.listen(5)
while True:
    c, addr = s.accept()
    print("Connected to:", addr)
    ip = os.popen("ifconfig eth0 | grep 'inet addr' | cut -d: -f2 | awk '{print $1}'").read()
    c.send(bytes("lel swag", "utf-8"))
    sleep(10)
    c.close()
