import time
import threading

def f(): 
    threading.Thread(target=lambda :time.sleep(10)).start()
    time.sleep(5)
    print("Daemon! Rawr!")

t = threading.Thread(target=f,daemon=True)
t.start()
time.sleep(1)
