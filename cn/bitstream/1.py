bits = input()
fl = map(lambda x: int(x,2), [bits[:16], bits[16:32], bits[32:64], bits[64:96], bits[96:100], bits[112:128], bits[128:144], bits[144:160]])
names = ['Source port', 'Destination Port', 'Seq. Number', 'Ack. Number', 'Header Length', 'Window', 'Checksum', 'Urgent']

fld = [[i,j] for i,j in zip(names,fl)]
fld[4][1]*=4
fld[-2][1] = hex(fld[-2][1])
print(*fld, sep="\n")
print(['Data', list(map(lambda x: int(x,2), [bits[i:i+8] for i in range(fld[4][1]*8,len(bits),8)]))])

