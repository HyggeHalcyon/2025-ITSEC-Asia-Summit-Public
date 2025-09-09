from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import hashlib
from secret import flag

class Server:
    def __init__(self):
        random = get_random_bytes(256)
        self.password = hashlib.md5(random).hexdigest()
        assert len(flag) == 16
        self.secret = (flag + get_random_bytes(48)).hex()

    def receive_challenge(self, challenge):
        self.clientChallenge = challenge

    def sendChallenge(self, receiver):
        self.challenge = get_random_bytes(16).hex() + get_random_bytes(48).hex()
        print("sending server challenge: ", self.challenge)
        receiver.receive_challenge(self, self.challenge)

    def receive_credential(self, credential):
        self.clientCredential = credential.decode()

    def calculateSessionKey(self):
        salt = b""
        iterations = 100_000
        key_length = 32
        self.calculatedKey = hashlib.pbkdf2_hmac('sha256', server.clientChallenge.encode() + self.challenge.encode() + self.password.encode(), salt, iterations, dklen=key_length)


    def computeCred(self):
        challenge = bytes.fromhex(self.clientChallenge)
        iv = challenge[:16]
        plaintext = challenge[16:]

        cipher_ecb = AES.new(self.calculatedKey, AES.MODE_ECB)
        ciphertext = bytearray()
        shift_reg = bytearray(iv)

        for byte in plaintext:
            encrypted = cipher_ecb.encrypt(bytes(shift_reg))
            keystream_byte = encrypted[0]
            cipher_byte = byte ^ keystream_byte
            ciphertext.append(cipher_byte)

            shift_reg = shift_reg[1:] + bytes([cipher_byte])

        result = bytes(ciphertext)
        self.nonce = iv
        self.credential = result.hex()

    def sendCredential(self, receiver, message):
        challenge = bytes.fromhex(message)
        plaintext = challenge
        cipher_ecb = AES.new(self.calculatedKey, AES.MODE_ECB)
        ciphertext = bytearray()
        shift_reg = bytearray(self.nonce)

        for i in range(0, len(plaintext), 16):
            block = plaintext[i:i+16]

            encrypted = cipher_ecb.encrypt(bytes(shift_reg))

            cipher_block = bytes([b ^ e for b, e in zip(block, encrypted)])
            ciphertext.extend(cipher_block)

            shift_reg = bytearray(cipher_block)

        result = bytes(ciphertext).hex()
        print("sending server credential: ", result)
        receiver.receive_credential(self, result)


    def verifyCred(self):
        if self.clientCredential == self.credential:
            print("[+] Authentication Successful.")
            return True
        else:
            print("[!] Authentication Failure!")
            return False


class Client:
    def __init__(self, username, password):
        self.username = hashlib.md5(username.encode()).hexdigest()
        self.password = hashlib.md5(password.encode()).hexdigest()
        self.randombytes = get_random_bytes(48).hex()
        self.serverChallenge = None
        self.serverCredential = None

    def sendChallenge(self, receiver):
        self.challenge = self.username + self.randombytes
        print("sending client challenge: ", self.challenge)
        receiver.receive_challenge(self, self.challenge)

    def receive_challenge(self, serverChallenge):
        self.serverChallenge = serverChallenge

    def sendCredential(self, receiver):
        print("sending client credential: ", self.credential)
        receiver.receive_credential(self, self.credential)

    def receive_credential(self, credential):
        self.serverCredential = credential.decode()

    def calculateSessionKey(self):
        salt = b""
        iterations = 100_000
        key_length = 32
        self.calculatedKey = hashlib.pbkdf2_hmac('sha256', self.challenge.encode() + self.serverChallenge.encode() + self.password.encode(), salt, iterations, dklen=key_length)

    def computeCred(self):
        challenge = bytes.fromhex(self.challenge)
        iv = challenge[:16]
        plaintext = challenge[16:]

        cipher_ecb = AES.new(self.calculatedKey, AES.MODE_ECB)
        ciphertext = bytearray()
        shift_reg = bytearray(iv)

        for byte in plaintext:
            encrypted = cipher_ecb.encrypt(bytes(shift_reg))
            keystream_byte = encrypted[0]
            cipher_byte = byte ^ keystream_byte
            ciphertext.append(cipher_byte)

            shift_reg = shift_reg[1:] + bytes([cipher_byte])

        result = bytes(ciphertext)
        self.credential = result.hex()


class Attacker:
    def __init__(self, client, server):
        self.client = client
        self.server = server

    def relay_challenge(self, receiver, challenge):
        receiver.receive_challenge(challenge)

    def receive_challenge(self, sender, challenge):
        tamp = input(f"(tamper): ")
        if tamp == "fwd":
            msg_sent = challenge
        else:
            msg_sent = tamp

        if sender == self.server:
            self.relay_challenge(self.client, msg_sent)
        elif sender == self.client:
            self.relay_challenge(self.server, msg_sent)

    def relay_credential(self, receiver, challenge):
        receiver.receive_credential(challenge)

    def receive_credential(self, sender, challenge):
        tamp = input(f"(tamper): ")
        if tamp == "fwd":
            msg_sent = challenge.encode()
        else:
            msg_sent = tamp.encode()

        if sender == self.server:
            self.relay_credential(self.client, msg_sent)
        elif sender == self.client:
            self.relay_credential(self.server, msg_sent)


if __name__ == "__main__":
    print("===HAPPY HAPPY ITSEC LOGoN PAGE==")
    username = input("Username: ")
    password = input("Password: ")

    client = Client(username, password)
    server = Server()
    attacker = Attacker(client, server)

    def begin_communication():
        while True:
            client.sendChallenge(attacker)
            server.sendChallenge(attacker)
            client.calculateSessionKey()
            server.calculateSessionKey()
            client.computeCred()
            server.computeCred()
            client.sendCredential(attacker)
            result = server.verifyCred()
            if result:
                server.sendCredential(attacker, server.clientChallenge)
                server.sendCredential(attacker, server.secret)

    begin_communication()