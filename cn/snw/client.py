import signal
import sys
import const


def valid_packet(pdu, sent_ack):
    flags, rseq, rack, rchecksum, rsub = pdu.split(":")
    checksum = int(flags) + int(rseq) + int(rack) + sum([ord(c) for c in rsub])
    return checksum == int(rchecksum) and sent_ack == int(rseq)

msg = input()
MSG_SIZE = 4 # chars
TIMEOUT = 4


def timeouter(x,y):
    raise TimeoutError("Timeout!")

signal.signal(signal.SIGALRM, timeouter)

seq = 0
ack = 0
flags = 0
for i in range(0, len(msg), MSG_SIZE):
    while True:
        sub = msg[i:i+MSG_SIZE]
        ack = seq + len(sub)
        checksum = sum([ord(c) for c in sub]) + seq + ack + flags
        print(flags, seq, ack, checksum, sub, sep=":")
        try:
            signal.alarm(TIMEOUT)
            while True:
                reply = input()
                if not valid_packet(reply, ack):
                    print("Discarding invalid packet", reply, file=sys.stderr)
                else:
                    signal.alarm(0)
                    break
        except TimeoutError as e:
            # resend packet due to timeout
            print("Timeout for packet seq", seq, file=sys.stderr)
            continue
        # print(rseq, rack, rchecksum, rsub)
        print("Accepted packet seq", seq, file=sys.stderr)
        seq = int(reply.split(":")[1])
        break
flags = flags | const.eot
sub =""
ack = seq + len(sub)
checksum = sum([ord(c) for c in sub]) + seq + ack + flags
print(flags, seq, ack, checksum, sub, sep=":")
