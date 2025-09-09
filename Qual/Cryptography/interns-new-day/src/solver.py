s_box = (
    0xa7, 0xb0, 0x6d, 0x63, 0x89, 0x1a, 0xbe, 0xc4, 0x3c, 0x42, 0xa1, 0x01, 0x5b, 0xc8, 0x2c, 0x6e,
    0xa4, 0x9c, 0x7c, 0x1e, 0x2a, 0xbd, 0x14, 0xe8, 0x99, 0x20, 0x27, 0x58, 0xac, 0x44, 0x25, 0x91,
    0x16, 0xe0, 0xb5, 0x85, 0xee, 0xcd, 0xae, 0xa5, 0x8c, 0x46, 0x8f, 0xdc, 0x12, 0xa3, 0x33, 0xd5,
    0x93, 0x94, 0x0b, 0x6c, 0x45, 0xfb, 0x9b, 0x75, 0x56, 0xc9, 0x4f, 0x19, 0xfe, 0xb3, 0x1b, 0x97,
    0x2f, 0x0d, 0xbc, 0xeb, 0x71, 0xd0, 0x77, 0x05, 0xa6, 0xe4, 0x30, 0xb9, 0x6f, 0x5e, 0xb2, 0x49,
    0x9d, 0x59, 0x3d, 0x32, 0xcc, 0x35, 0xf1, 0x48, 0x34, 0x84, 0xd3, 0xf9, 0x7b, 0x51, 0xf0, 0xc0,
    0x5a, 0x4d, 0x66, 0xaa, 0x57, 0x54, 0xb7, 0x24, 0x1f, 0x5c, 0x4b, 0xfa, 0xf3, 0xb4, 0xdd, 0x8e,
    0x92, 0x1c, 0xaf, 0xba, 0xcb, 0x10, 0x88, 0xad, 0x81, 0xfd, 0xe2, 0x28, 0x2e, 0xb6, 0x68, 0xe7,
    0xdb, 0x67, 0xff, 0x06, 0x60, 0x5d, 0x82, 0xd4, 0xc6, 0xdf, 0xab, 0x52, 0xf7, 0x13, 0x62, 0x95,
    0x5f, 0x4e, 0xd6, 0xef, 0x39, 0xc3, 0x38, 0xe9, 0x7d, 0xda, 0x04, 0xc1, 0xc2, 0x18, 0xca, 0x41,
    0x21, 0x73, 0x96, 0x70, 0x80, 0x72, 0x78, 0xd9, 0xb1, 0x8a, 0xa0, 0xce, 0xbb, 0xf5, 0x26, 0x64,
    0xd2, 0x36, 0x50, 0xec, 0xde, 0x79, 0x6a, 0xea, 0xcf, 0x86, 0xd8, 0x1d, 0x9e, 0x40, 0x90, 0xf8,
    0x7f, 0x31, 0x55, 0x83, 0x11, 0xf6, 0xbf, 0x69, 0x07, 0xe3, 0x53, 0x4c, 0x2b, 0x23, 0x00, 0x3e,
    0xc5, 0x37, 0x8d, 0xd1, 0x7a, 0xe1, 0x74, 0xe5, 0xc7, 0x08, 0xa9, 0x0a, 0x0f, 0x7e, 0x76, 0x6b,
    0x87, 0x17, 0x98, 0xd7, 0xe6, 0x3b, 0x22, 0xa2, 0x65, 0x09, 0x47, 0x2d, 0x0e, 0xf2, 0x8b, 0x02,
    0xb8, 0xf4, 0xfc, 0x03, 0x9f, 0x3f, 0xed, 0x61, 0x9a, 0x0c, 0xa8, 0x4a, 0x43, 0x3a, 0x15, 0x29
)

r_con = (
    0x77, 0x4b, 0x05, 0x02, 0xe3, 0x0f, 0xf2, 0x61,
    0xfc, 0x72, 0xf3, 0xf6, 0xc9, 0xe6, 0x20, 0xc9,
    0xb0, 0xad, 0xb8, 0x1f, 0x71, 0x5d, 0xe9, 0xcb,
    0x35, 0x44, 0x51, 0xde, 0xc9, 0x43, 0x03, 0x66
)

def invert_sbox(sbox):
    inv_sbox = [0]*len(sbox)
    for i in range(len(sbox)):
        inv_sbox[sbox[i]] = i
    return inv_sbox

inv_s_box = invert_sbox(s_box)

def sub_bytes(s):
    for i in range(4):
        for j in range(4):
            s[i][j] = s_box[s[i][j]]

def inv_sub_bytes(s):
    for i in range(4):
        for j in range(4):
            s[i][j] = inv_s_box[s[i][j]]

def shift_rows(s):
    s[0][1], s[1][1], s[2][1], s[3][1] = s[1][1], s[2][1], s[3][1], s[0][1]
    s[0][2], s[1][2], s[2][2], s[3][2] = s[2][2], s[3][2], s[0][2], s[1][2]
    s[0][3], s[1][3], s[2][3], s[3][3] = s[3][3], s[0][3], s[1][3], s[2][3]


def inv_shift_rows(s):
    s[0][1], s[1][1], s[2][1], s[3][1] = s[3][1], s[0][1], s[1][1], s[2][1]
    s[0][2], s[1][2], s[2][2], s[3][2] = s[2][2], s[3][2], s[0][2], s[1][2]
    s[0][3], s[1][3], s[2][3], s[3][3] = s[1][3], s[2][3], s[3][3], s[0][3]

def add_round_key(s, k):
    for i in range(4):
        for j in range(4):
            s[i][j] ^= k[i][j]

# learned from https://web.archive.org/web/20100626212235/http://cs.ucsb.edu/~koc/cs178/projects/JT/aes.c
xtime = lambda a: (((a << 1) ^ 0x1B) & 0xFF) if (a & 0x80) else (a << 1)

def mix_single_column(a):
    # see Sec 4.1.2 in The Design of Rijndael
    t = a[0] ^ a[1] ^ a[2] ^ a[3]
    u = a[0]
    a[0] ^= t ^ xtime(a[0] ^ a[1])
    a[1] ^= t ^ xtime(a[1] ^ a[2])
    a[2] ^= t ^ xtime(a[2] ^ a[3])
    a[3] ^= t ^ xtime(a[3] ^ u)

def mix_columns(s):
    for i in range(4):
        mix_single_column(s[i])

def inv_mix_columns(s):
    # see Sec 4.1.3 in The Design of Rijndael
    for i in range(4):
        u = xtime(xtime(s[i][0] ^ s[i][2]))
        v = xtime(xtime(s[i][1] ^ s[i][3]))
        s[i][0] ^= u
        s[i][1] ^= v
        s[i][2] ^= u
        s[i][3] ^= v

    mix_columns(s)

def bytes2matrix(text):
    """ Converts a 16-byte array into a 4x4 matrix.  """
    return [list(text[i:i+4]) for i in range(0, len(text), 4)]

def matrix2bytes(matrix):
    """ Converts a 4x4 matrix into a 16-byte array.  """
    return bytes(sum(matrix, []))

def pad(plaintext):
    """
    Pads the given plaintext with PKCS#7 padding to a multiple of 16 bytes.
    Note that if the plaintext size is a multiple of 16,
    a whole block will be added.
    """
    padding_len = 16 - (len(plaintext) % 16)
    padding = bytes([padding_len] * padding_len)
    return plaintext + padding

def unpad(plaintext):
    """
    Removes a PKCS#7 padding, returning the unpadded text and ensuring the
    padding was correct.
    """
    padding_len = plaintext[-1]
    assert padding_len > 0
    message, padding = plaintext[:-padding_len], plaintext[-padding_len:]
    assert all(p == padding_len for p in padding)
    return message

def split_blocks(message, block_size=16, require_padding=True):
        assert len(message) % block_size == 0 or not require_padding
        return [message[i:i+16] for i in range(0, len(message), block_size)]

class AES:
    """
    Class for AES-128 encryption with CBC mode and PKCS#7.

    This is a raw implementation of AES, without key stretching or IV
    management. Unless you need that, please use `encrypt` and `decrypt`.
    """
    rounds_by_key_size = {16: 10, 24: 12, 32: 14}
    def __init__(self, master_key):
        """
        Initializes the object with a given key.
        """
        assert len(master_key) in AES.rounds_by_key_size
        self.n_rounds = AES.rounds_by_key_size[len(master_key)]
        self._key_matrices = self._expand_key(master_key)

    def _expand_key(self, master_key):
        key_columns = [list(master_key[i:i+4]) for i in range(0, len(master_key), 4)]
        iteration_size = len(master_key) // 4

        i = 1
        while len(key_columns) < (self.n_rounds + 1) * 4:
            word = list(key_columns[-1])

            if len(key_columns) % iteration_size == 0:
                word.append(word.pop(0))
                word = [s_box[b] for b in word]
                word[0] ^= r_con[i]
                i += 1
            elif len(master_key) == 32 and len(key_columns) % iteration_size == 4:
                word = [s_box[b] for b in word]

            word = bytes(i^j for i, j in zip(word, key_columns[-iteration_size]))
            key_columns.append(word)

        # Group key words in 4x4 byte matrices.
        return [key_columns[4*i : 4*(i+1)] for i in range(len(key_columns) // 4)]

    def decrypt_block(self, ciphertext):
        """
        Decrypts a single block of 16 byte long ciphertext.
        """
        assert len(ciphertext) == 16

        cipher_state = bytes2matrix(ciphertext)

        inv_shift_rows(cipher_state)
        add_round_key(cipher_state, self._key_matrices[-1])
        inv_sub_bytes(cipher_state)

        for i in range(self.n_rounds - 1, 0, -1):
            inv_mix_columns(cipher_state)
            inv_shift_rows(cipher_state)
            add_round_key(cipher_state, self._key_matrices[i])
            inv_sub_bytes(cipher_state)

        add_round_key(cipher_state, self._key_matrices[0])

        return matrix2bytes(cipher_state)

    def decrypt_ecb(self, ciphertext):
        blocks = []
        for ciphertext_block in split_blocks(ciphertext):
            block = self.decrypt_block(ciphertext_block)
            blocks.append(block)
        return unpad(b''.join(blocks))

if __name__ == '__main__':
    key = b'"SECRETKEYDONTSHARETHISTOANYONE"'
    cipher = bytes.fromhex("9e65ce8e1fefcec7e09384b3709a1ca9b50aca476513d390cbe40beb254bd007bf8e79389fd1d3bb11c3cc055d6c3754")
    print(AES(key).decrypt_ecb(cipher).decode())