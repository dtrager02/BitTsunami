import sys
import struct 
from time import perf_counter
packer = struct.pack("<"+"i",2)
numbers = [*range(10**5,10**7)]
#content = open("ds_4X_96fps.mp4","rb").read() 
#print(bytes(content)+"sviasliovjlsoi".encode("utf-8"))
#a = content+"sviasliovjlsoi".encode("utf-8")
#print(a[0:100])
my_bytes = bytearray()
my_bytes.extend(b"gFfvaojna")
my_bytes.extend(b"gfvojnaeo")
my_bytes.extend(b"gfvojnaeo")
print(str(len(my_bytes)),my_bytes)
start = perf_counter()
for i in numbers:
    b = struct.pack("<"+"i",i)
    c = struct.unpack("<"+"i",b)
print(perf_counter() - start,b,c)
start = perf_counter()
for i in numbers:
    b = i.to_bytes(4,byteorder="little") 
    c = int.from_bytes(b,byteorder="little")
print(perf_counter() - start,b,c)
a = 2**31
#print(struct.pack("<"+"i",a),a.to_bytes(4,byteorder="little"))