import multiprocessing as m
from multiprocessing import set_start_method
import time
a = 1
def nigz():
    time.sleep(5)
    print(a)
if __name__ == '__main__':    
    set_start_method("forkserver")
    m.Process(target=nigz).start()
    a = 2
    print(a)
