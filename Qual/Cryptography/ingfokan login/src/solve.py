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
		print("result:", result)
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


'''
to do list:
1. create and compute cred v2 (cfb128) and send to clientV
2. send the cfb128-encrypted flagV
3. cuma bisa 16 bytes


'''