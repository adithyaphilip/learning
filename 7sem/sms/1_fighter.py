from tkinter import *
import time
import threading

off_x = 100
off_y =100 
height=500
width=1000
top = Tk()
top.geometry("%dx%d" % (height, width))
var_f = StringVar()
var_b = StringVar()
var_f.set("fighter")
var_b.set("bomber")
fighter = Label(top, textvariable=var_f)
bomber = Label(top, textvariable=var_b)

def draw(bomber_pos, fighter_pos):
    bomber.place(x=off_x + bomber_pos[0], y = off_y + bomber_pos[1])
    fighter.place(x=off_x + fighter_pos[0], y = off_y + fighter_pos[1])

def get_bomber_poses():
    return [
        (80,90),
        (90,-2),
        (99,-5),
        (108,-9),
        (116,-15),
        (125,-18),
        (133,-23),
        (141,-29),
        (151,-28),
        (160,-25),
        (169,-21),
        (179,-20)
    ]


def euclidean_dist(pos1, pos2):
    return ((pos1[0]-pos2[0])**2 + (pos1[1]-pos2[1])**2) ** 0.5

def is_hit(bomber_pos, fighter_pos):
    return euclidean_dist(bomber_pos, fighter_pos) <= 10


def next_pos(bomber_pos, fighter_pos, fighter_speed):
    sin_theta = (bomber_pos[1]-fighter_pos[1])/euclidean_dist(bomber_pos, fighter_pos)
    cos_theta = (bomber_pos[0]-fighter_pos[0])/euclidean_dist(bomber_pos, fighter_pos)
    return fighter_pos[0] + fighter_speed * cos_theta, fighter_pos[1] + fighter_speed * sin_theta


def start_simulation(bomber_poses, fighter_pos, fighter_speed):
    print ("%-13s|%-13s|%-13s|%-13s|%-13s" % ("Bomber X", "Bomber Y", "Fighter X", "Fighter Y", "Distance"))
    # print ("-"*69)
    for pos in bomber_poses:
        print("%-13f|%-13f|%-13f|%-13f|%-13f" % (pos[0], pos[1], fighter_pos[0], fighter_pos[1],euclidean_dist(pos, fighter_pos)))
        draw(pos, fighter_pos)
        time.sleep(1)
        if is_hit(pos,fighter_pos):
            return True
        else:
            fighter_pos = next_pos(pos, fighter_pos, fighter_speed)
    return False

def main():
    init_xf = 0
    init_yf = 50

    if start_simulation(get_bomber_poses(), (init_xf, init_yf), 10):
        print('BOOM! Tango down!')
    else:
        print('Enemy out of range. Falling back')


threading.Thread(target=main).start()

top.mainloop()
