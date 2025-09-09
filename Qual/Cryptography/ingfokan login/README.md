# Ingfokan Login

Category: Cryptography
Difficulty: Medium
Author: Jakwan Bagung

## Description

  winfo parti 5 compe road to immo beton keras siap tabrak n1ka dan juragan raps

  Flag Format: ITSEC{.*}

  Author: Jakwan Bagung

## Writeup

In this challenge we are given a single file:

    chall.py: The source code of a simulation of attacker performing man-in-the-middle attack upon a secure logon protocol. Attacker have capabilities to tamper the outgoing and upcoming traffic.


This challenge have 2 parts:

Part 1: AES-CFB8 Zerologon vulnerability on Microsoft Netlogon CVE-2020-1472

`computeCred` function use modified AES ECB like this:

```
        cipher_ecb = AES.new(self.calculatedKey, AES.MODE_ECB)
        ciphertext = bytearray()
        shift_reg = bytearray(iv)

        for byte in plaintext:
            encrypted = cipher_ecb.encrypt(bytes(shift_reg))
            keystream_byte = encrypted[0]
            cipher_byte = byte ^ keystream_byte
            ciphertext.append(cipher_byte)

            shift_reg = shift_reg[1:] + bytes([cipher_byte])
```

which is the same function as AES-CFB8 implementation.

This challenge simulates vulnerable Microsoft's Netlogon protocol flow CVE-2020-1472 where AES-CFB8 is used to generate netlogon credential. In this vulnerability, sending a tamperent plaintext consisting of all null-bytes challenge have 1/256 chances of getting all null-bytes ciphertext, depending on the key. More details can be found: https://cybersecurity.bureauveritas.com/uploads/whitepapers/Zerologon.pdf

how to get all zero ciphertext:
```
from pwn import *

r = remote('localhost', 2025, level="debug")
r.recvuntil(b'Username: ')
sendusername = b'apa aja bebas boy'
r.sendline(sendusername)
r.recvuntil(b'Password: ')
sendpassword = b'apa aja bebas cok'
r.sendline(sendpassword)
for i in range(1000):
  r.recvuntil(b'(tamper): ')
  sendChallenge = b'\x00' * 64
  r.sendline(sendChallenge.hex().encode())


  r.recvuntil(b'(tamper): ')
  sendChallenge = b'fwd'
  r.sendline(sendChallenge)

  r.recvuntil(b'(tamper): ')
  sendCred = b'\x00' * 48
  r.sendline(sendCred.hex().encode())

  # r.interactive()
  # r.recvline()
  result = r.recvline()
  print("hasil: ", result)
  if b'Authentication Failure' not in result:
    #logged in
```


Part 2: AES CFB Chosen Plaintext Attack

after being logged in, user will received AES CFB encrypted client challenge and encrypted server secret AKA the flag. As we already know our own client challenge, we can recover encrypted flag by:
ENC_CLIENTCHALL XOR PLAIN_CLIENTCHALL XOR ENC_FLAG 

```
    r.recvuntil(b'sending server credential:  ')
    cipnull = bytes.fromhex(r.recvline().strip().decode())
    
    r.recvuntil(b'(tamper): ')
    sendChallenge = b'fwd'
    r.sendline(sendChallenge)
    
    r.recvuntil(b'sending server credential:  ')
    encflag = bytes.fromhex(r.recvline().strip().decode())

    r.recvuntil(b'(tamper): ')
    sendChallenge = b'fwd'
    r.sendline(sendChallenge)

    plainnull = sendCred
    flag = xor(xor(cipnull, plainnull), encflag)

    print("flag:", flag[:16])

    # r.interactive()
    break

```


Flag: ITSEC{i_l1ke_1t_b3tter}