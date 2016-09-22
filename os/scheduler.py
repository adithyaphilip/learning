import multiprocessing as mp
from queue import Queue
from time import sleep
import math
import random
import json

PAGES_MAX = 2 ** 32 // 1024;  # 1024 is page size i.e 1KB
PAGES_BITS = int(32 - math.log(PAGES_MAX, 2))  # bits required to represent total possible pages
REALLY_SLEEP = 0

def readMemConfig():
    with open("memconf") as f:
        return json.load(f)


def readAppConfig():
    with open("appconf") as f:
        return json.load(f)


def memListen(pipe, page_table):
    '''
    :param pipe: end to receive (addr, appname) and send "OK" to
    :param page_table: dictionary to be used as pt[appname][pageno]=frameno
    :return:
    '''

    conf = readMemConfig()

    TLB_MAX = conf['T']  # how many can TLB hold, need not be power of two
    FRAMES_MAX = conf['P']  # how many frames can we hold in memory, must be power of 2 for easy logical->physical address conversion

    tlb = {}  # dictionary of (app, page) => (frame, time_inserted). Can be achieved with only the first TLB_MAX of lru,
    # but we implement as a separate data struture for semantic purposes
    lru = []  # list of (app, page, addr)

    print("Memory Unit: Starting")

    times = 0

    while True:
        times += 1
        addr, app = pipe.recv()

        if addr == None:
            pipe.send("OK")
            break

        tot_mem_access.value += 1

        page = addr >> (32 - PAGES_BITS)
        # print("{0:032b}".format(addr), ("{0:0"+str(PAGES_BITS)+"b}").format(page))

        pt = page_table[app]

        print("Memory Unit:", "Current TLB:", tlb)
        sleep(REALLY_SLEEP*1)
        if (app, page) in tlb:
            print("Memory Unit:", addr, "TLB HIT! Frame no.:", tlb[(app, page)][0])
            tlb[(app, page)][1] = times  # updating time used
            lru.remove((app, page))
            lru.append((app, page))
        else:
            tot_tlb_miss.value += 1

            print("Memory Unit:", addr, "TLB MISS!")
            sleep(REALLY_SLEEP*2)

            frameNo = pt[page]
            if frameNo != None:
                print("Memory Unit:", addr, "Page in memory! Frame:", frameNo)
                # updating lru
                lru.remove((app, page))
                lru.append((app, page))
            else:
                tot_page_fault.value += 1
                print("Memory Unit:", addr, "Page faulted!")
                sleep(REALLY_SLEEP*4)

                # removing from memory if necessary
                if (len(lru) == FRAMES_MAX):
                    p_name, p_page = lru.pop(0)
                    frameNo = page_table[p_name][p_page]
                    page_table[p_name][p_page] = None
                else:
                    frameNo = len(lru)

                pt[page] = frameNo
                lru.append((app, page))

                print("Loaded into memory and accessed.")

            # loading into tlb
            if len(tlb) == TLB_MAX:
                tlb.pop(min(tlb, key=lambda x:tlb[x][1]))  # pop oldest key

            tlb[(app, page)] = [frameNo, times]

            print("Memory Unit:", "Loaded into TLB:", tlb)

        pipe.send("OK")
    print("Memory Unit: Shutting down")


def application(q, conf):
    v = conf['V']
    n = conf['N']
    for _ in range(n):
        rand = random.randint(0, (v << (32 - PAGES_BITS))-1)
        q.put(rand)
        print(rand >> (32 - PAGES_BITS))

class Scheduler(mp.Process):
    def __init__(self, app_q_tuple, mem_pipe):
        super().__init__()
        self._app_q_tuple = app_q_tuple
        self._mem_pipe = mem_pipe

    def run(self):
        print("Scheduler:", "starting")
        s = self.getSlice()
        q = self._app_q_tuple
        for apps in iter(q.get, None):
            for i in range(0,s):
                if (apps[1].empty()):
                    break
                else:
                    memAddress = apps[1].get()
                    print("Scheduler:", apps[0], "has requested", memAddress)
                    self.mem_request(memAddress, apps[0])
            if not apps[1].empty():
                q.put(apps)
            else:
                print("Scheduler:", apps[0], "has no more requests, removing from queue!")
                if q.empty(): q.put(None)
        self.mem_request(None, None)
        print("Scheduler: Shutting down!")

    def mem_request(self, addr, name):
        self._mem_pipe.send((addr, name))
        print("Scheduler:", "Access completed", self._mem_pipe.recv())

    def getSlice(self):
        with open("sconf") as f:
            return json.load(f)['C']

if __name__ == '__main__':
    manager = mp.Manager()
    tot_mem_access = manager.Value('i', 0)
    tot_page_fault = manager.Value('i', 0)
    tot_tlb_miss = manager.Value('i', 0)

    pt = {}
    q = Queue()

    for app in readAppConfig():
        aq = mp.Queue()
        pt[app["name"]] = {}
        for i in range(app["V"]):
            pt[app["name"]][i] = None
        a_process = mp.Process(target=application, args=(aq, app))
        a_process.start()
        a_process.join()
        q.put((app["name"], aq))
        sleep(0.1)  # python bug requires it

    p_pipe, c_pipe = mp.Pipe()

    memUnit = mp.Process(target=memListen, args=(p_pipe, pt))
    memUnit.start()

    s = Scheduler(q, c_pipe)
    s.start()

    s.join()
    memUnit.join()

    print("Simulation complete: \nTotal memory accesses:", tot_mem_access.value, "\nPage fault rate:",
          tot_page_fault.value / tot_mem_access.value, "\nTLB Miss rate:", tot_tlb_miss.value / tot_mem_access.value)
