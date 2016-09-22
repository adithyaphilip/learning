import urllib.request
import time
from concurrent.futures import ThreadPoolExecutor

def fire(fname):
    print("Firing " + fname)
    resp = urllib.request.urlopen("http://www.pes.edu")
    if resp.getcode()//100 == 2:
        with open(fname, "wb") as f:
            f.write(resp.read())
        print ("YES!")
    else:
        print(resp.read().decode())
with ThreadPoolExecutor(max_workers=50) as executor:
    ctr = 0
    while True:
        for i in range(1):
            executor.submit(fire, "dirr/"+str(ctr))
            ctr+=1
            print("Submitted " + str(ctr))
        time.sleep(0.5)
#fire("1")
