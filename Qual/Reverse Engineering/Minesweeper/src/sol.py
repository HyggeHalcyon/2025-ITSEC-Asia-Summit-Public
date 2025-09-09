from Crypto.Util.number import *
from Crypto.Cipher import ChaCha20
Empty = 16;
Mines = 48;
width= 8;
height = 8;
seed = 88403651

val=[]
for i in range(height):
    val.append([])
    for j in range(width):
        mod = (width*height)+1
        val[i].append(((i*width+j)*(seed))%mod)

order = set()
now = 4
while now not in order:
    order.add(now)
    now = (now*seed)%mod

key =seed
keys=[]
for _ in range(10):
    mod = (width*height)+1
    key = ((key)*(seed))%mod
    keys.append(key)
arr=[342066253,686880041,828922036,509868183]

for _ in range(9,-1,-1):
    mod=1123996597
    key=keys[_]
    save=[0]*4
    save[2]=arr[0]
    save[1]=arr[3]^((save[2]*key+key)%mod)
    save[0]=arr[1]^((save[1]*key+key)%mod)
    save[3]=((arr[2]-save[0]*save[1]*save[2])*inverse(save[0]*save[2],mod))%mod
    arr=[i for i in save]

ans=[]
for i in arr:
    cnt=4
    temp=i
    save=[]
    while(cnt):
        cnt-=1
        save.append(temp&0xff)
        temp>>=8
    for _ in save[::-1]:
        ans.append(_)

def valueChecker(value):
    return (value * seed) % (width * height+1);
peta=dict()
for i in range(1,65):
    peta[i]=valueChecker(i)
key=[]
for i in ans:
    key.append(i)
for i in ans:
    key.append(peta[i])

    
key=b''.join(bytes([i]) for i in key)
cipher=ChaCha20.new(key=key,nonce=b'\xf0g\x906\xf2\xa4e\x17')
print(cipher.decrypt(bytes.fromhex("84bcea7b4084411805c7cbdb22f4e8623c73859183db14d27241cd4dc800")))
