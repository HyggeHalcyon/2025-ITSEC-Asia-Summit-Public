# !/usr/bin/env python3
from Crypto.Util.number import getPrime, bytes_to_long, inverse
from secrets import FLAG

assert FLAG.startswith(b'ITSEC{') and FLAG.endswith(b'}')

class Dungeon:
    def __init__(self, key_len: int = 1024):
        while True:
            try:
                p,q = getPrime(key_len//2), getPrime(key_len//2)
                self.n = p*q
                self.e = 0x10001
                et = (p-1)*(q-1)
                self._d = inverse(self.e, et)
                break
                
            except ValueError:
                continue
    
    def sloth(self, m: int) -> int:
        return pow(m, self.e, self.n)

    def shadow(self, c: int) -> int:
        p = pow(c, self._d, self.n)
        total_bits = p.bit_length()
        top_mask = ((1 << 128) - 1) << (total_bits - 128)
        bottom_mask = (1 << 128) - 1
        mask = top_mask | bottom_mask
        return p & mask

if __name__ == '__main__':
    Aid = Dungeon(1024)
    mystery = Aid.sloth(bytes_to_long(FLAG))

    print("""
You take your first cautious steps inside, and the echo of your boots fills the silence. The corridors twist like the roots of some massive, underground tree, until the path splits into a dimly lit chamber where two odd figures wait. There's a tablet between these to figures.
""")
    print(f"mystery: {mystery}")
    print(f"n: {Aid.n}")

    for _ in range(2014):
        print("What will you do")
        print('1. speak "the weight of sloth"')
        print('2. speak "the toll of secrets"')
        print("3. turn back and run")
        menu = ""
        while menu not in ["1","2","3"]:
            menu = input("(1|2|3): ")

        if menu == "1":
            userInput = ""
            userInput = input("...: ")
            if userInput.isdigit() and int(userInput) == bytes_to_long(FLAG):
                print("...Huh. You're still alive. Figures.")
                print("Well... guess you didn't really need me after all. Good job, I guess.")
                break
            print("...")

        elif menu == "2":
            userInput = ""
            while not userInput.isdigit():
                userInput = input("payment: ")
            
            if int(userInput) < 1:
                print("Coin? Trinkets? Do you take me for a merchant?")
                print("Offer me coin again, and I will offer you silence.")
                continue
            if int(userInput) % mystery == 0:
                print("Secrets weigh more than gold. They stain more than blood. I do not want your glittering junk-bring me something that whispers. Something that hurts to say.")
                continue
            decrypted = Aid.shadow(int(userInput))

            print(f"(whisper): {decrypted}")
        
        elif menu == "3":
            print("Running already? How predictable...")
            break