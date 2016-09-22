import signal
import sys
import const

def valid_packet(pdu, sent_ack):
    if sent_ack == -1: return True
    flags, rseq, rack, rchecksum, rsub = pdu.split(":")
    checksum = int(flags) + int(rseq) + int(rack) + sum([ord(c) for c in rsub])
    return checksum == int(rchecksum) and sent_ack == int(rseq)

MSG_SIZE = 4 # chars
TIMEOUT = 4


def timeouter(x,y):
    raise TimeoutError("Timeout!")

signal.signal(signal.SIGALRM, timeouter)

seq = 0
ack = -1
msg = ""
while True:
    sub = input()
    if valid_packet(sub, ack):
        while True:
            flags, rseq, rack, rchecksum, rsub = sub.split(":")
            if int(flags) & const.eot != 0:
                print("Final message received!", msg)
                exit(0)
            seq = int(rack)
            ack = seq
            checksum = ack + seq + int(flags)
            msg += rsub
            while True:
                try:
                    signal.alarm(TIMEOUT)
                    print(flags, ":", seq, ":", ack, ":", checksum, ":", sep="")
                    while True:
                        sub = input()
                        if valid_packet(sub, ack):
                            break
                        else:
                            print("Discarding invalid packet!", sub, file=sys.stderr)
                    break
                except TimeoutError as e:
                        print("Timeout waiting for response!",file=sys.stderr)




