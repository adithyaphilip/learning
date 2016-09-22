import sys
f = open("in")
str1 = f.read()

version = int(str1[0:4],2)
hlen = int(str1[4:8],2) * 4
service = int(str1[8:16],2)
total_length = int(str1[16:32],2)

id = int(str1[32:48],2)
flags = int(str1[48:51],2)
flag_offset = int(str1[51:64],2)
ttl = int(str1[64:72],2)
protocol = int(str1[72:80],2)
checksum = int(str1[80:96],2)

source_firstseg = int(str1[96:104],2)
source_secondseg = int(str1[104:112],2)
source_thirdseg = int(str1[112:120],2)
source_fourthseg = int(str1[120:128],2)

dest_firstseg = int(str1[128:136],2)
dest_secondseg = int(str1[136:144],2)
dest_thirdseg = int(str1[144:152],2)
dest_fourthseg = int(str1[152:160],2)


print("Version: ",version);
print("Header Length-bytes: ",hlen)
print("Service: ",service)
print("Total length: ",total_length)

print("Identification: ",id)
print("Flag: ",flags)
print("Offset: ",flag_offset)
print("Time to live: ",ttl)
print("Protocol: ",protocol)
print("Header checksum: ",checksum)

print("Source IP address: ",".".join(map(str, [source_firstseg,source_secondseg,source_thirdseg,source_fourthseg])))
print("Destination IP address: ",".".join(map(str,[dest_firstseg,dest_secondseg,dest_thirdseg,dest_fourthseg])))
      
data = str1[160:]

print(data,file=sys.stderr)
