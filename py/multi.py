import threading
import time
#tlock=threading.Lock()

def func1():

    print ("in 1")
    for i in range(ord('a'),ord('z')+1,2):
        S1.acquire()
        print chr(i)
        S2.release()
    #time.sleep(2)
    print ("out 1")



def func2():

    print ("in 2")
    for i in range(ord('b'),ord('z')+1,2):
        S2.acquire()
        print chr(i)
        S1.release()
    #time.sleep(2)
    print ("out 2")



def main():

    t1=threading.Thread(target=func1)
    t2=threading.Thread(target=func2)
    t1.start()
    t2.start()
    t1.join()
    t2.join()

S1 = threading.Semaphore(1)
S2 = threading.Semaphore(0)
main()
