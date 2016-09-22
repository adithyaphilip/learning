__author__ = 'abrahamphilip'
import copy

change = True

def update(src, dst):
    for loc in dst:
        if loc == "id" or loc == src["id"]: continue
        if loc not in src:
            src[loc] = 1000000
        ncost = dst[loc] + src[dst["id"]]
        if src[loc] > ncost:
            src[loc] = ncost
            global change
            change = True

def start():
    nodes ={
        "a": {"id":"a", "b":1, "c":5},
        "b": {"id":"b", "a":1, "d":3},
        "c": {"id":"c", "a":5, "d":1},
        "d": {"id":"d", "b":3, "c":1}
    }
    global change
    while change:
        print(nodes)
        change = False
        nl = copy.deepcopy(nodes)
        for key in nodes:
            node = nodes[key]
            for nb in node:
                if nb == "id": continue
                update(nl[nb], node)
        for key in nl:
            nodes[key] = nl[key]

start()

