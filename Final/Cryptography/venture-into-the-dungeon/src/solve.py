import pwn
import math
from Crypto.Util.number import long_to_bytes
from fractions import Fraction

LOCAL = True

if LOCAL:
    pty = pwn.process.PTY
    s = pwn.process(["python3", "chall.py"], stdin=pty, stdout=pty)
else:
    s = pwn.remote('127.0.0.1', 5828)

# get encrypted flag & n
s.recvuntil(b'mystery: ')
encryptedFlag = int(s.recvuntil(b'\n').strip())
print(f"{encryptedFlag = }")

s.recvuntil(b'n: ')
n = int(s.recvuntil(b'\n').strip())
print(f"{n = }")
encryptedTwo = pow(2,0x10001,n)

# decrypt repeatedly
low_frac, high_frac = Fraction(0), Fraction(1)
low, high = 0, n

num_repetitions = n.bit_length()
for i in range(num_repetitions):
    encryptedFlag = (encryptedFlag * encryptedTwo) % n
    
    s.recvuntil(b'(1|2|3): ')
    s.sendline(b'2')
    s.recvuntil(b'payment: ')
    s.sendline(str(encryptedFlag).encode())
    s.recvuntil(b'(whisper): ')
    decrypted = int(s.recvuntil(b'\n').strip(), 16)
    res = not decrypted & 1

    # the plaintext is less than half the modulus
    if res:
        high_frac = (high_frac - low_frac) / 2 + low_frac
        high = n * high_frac

    # the plaintext is more than half the modulus
    else:
        low_frac = (high_frac - low_frac) / 2 + low_frac
        # low = n * low_frac

    msg = long_to_bytes(math.floor(high))
    print(f'Iteration {i}: {msg}')
s.close()