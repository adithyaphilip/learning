import threading
def a():
    for i in range(ord('a'),ord('z'),2):
        S1.acquire()
        print(chr(i))
        S2.release()
        
def b():
    for i in range(ord('b'), ord('z')+1,2):
        S2.acquire()
        print(chr(i))
        S1.release()
        
S1 = threading.Semaphore(1)
S2 = threading.Semaphore(0)

threading.Thread(target=a).start()
threading.Thread(target=b).start()

