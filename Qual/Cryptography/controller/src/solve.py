from pwn import *


goal_user = b"thegreatestadminsinthewholeworld"
part_one = goal_user.hex()[:32]
part_two = goal_user.hex()[32:]


r = remote('localhost', 20255)
r.recvuntil(">> ")
r.sendline('1')
r.recvuntil("Username (hex): ")
r.sendline(part_one)
r.recvuntil("Password: ")
r.sendline("kodokgaming")
r.recvuntil("authentication token: ")
auth_token1 = r.recvline().strip().decode()
print(auth_token1)

part_two = xor(bytes.fromhex(auth_token1), bytes.fromhex(part_two)).hex()

r.sendline('1')
r.recvuntil("Username (hex): ")
r.sendline(part_two)
r.recvuntil("Password: ")
r.sendline("kodokgaming")
r.recvuntil("authentication token: ")
auth_token2 = r.recvline().strip().decode()
print(auth_token2)

r.sendline('2')
r.sendline('b')
r.recvuntil("Username (hex): ")
r.sendline(goal_user.hex())
r.recvuntil("Token: ")
r.sendline(auth_token2)


r.interactive()