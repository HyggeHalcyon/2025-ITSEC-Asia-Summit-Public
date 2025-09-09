# Intern's New Day

Category: Cryptography
Difficulty: Easy
Author: EternalBeats

## Description

  Boss: "Can you create an basic encryption for our backend"
  Intern: "Sure Boss, let me work on it"

  *When alone*
  Intern: "Surely a couple of sip of wine does not hurt anyone"

  Flag Format: ITSEC{.*}

  Author: EternalBeats

## Writeup

This is basic AES ECB at it's core, but with a slight twist, that everything in the challenge is are not properly put at the right place. Different sbox, different r_con, wrong order on the substitution, wrong order in the shifting, etc.

Some reference of how AES works: https://medium.com/@dillihangrae/aes-advanced-encryption-standard-step-by-step-in-depth-understanding-62a9db709902

But even with different of anything, we just need to know what function that is currently is doing, and do the inverse of that, just remember that the order also need to be adjusted.

Let's tackle most of the difference one by one

For substitution, shifting, mixing, and round key, even when the order of things is changed, the inversing method should be still the same, because all of them does not overlap.

For sbox, we can see that the box is not what it usualy is, but it does not really matter in this case, we just need to know, how the inverse will be like

```
def invert_sbox(sbox):
    inv_sbox = [0]*len(sbox)
    for i in range(len(sbox)):
        inv_sbox[sbox[i]] = i
    return inv_sbox

inv_s_box = invert_sbox(s_box)
```

Same thing with r_con, even if it changed, we just need to supply the changed r_con. One thing to note for encryption in general. Most of the time, we just need to follow the component used, even if it's not the usual one, we just need to use the changed component.

Now, even with the invertion method for the function is the same for all of the transformation, the order of invertion is important, for example the order transformation should be:

```
substitution bytes
shifting row
mixing columns
add round key
```

but we can see that the see the encrypt block function looks like this:

```
# add round key
for i in range(4):
    for j in range(4):
        ps[i][j] ^= self._km[0][i][j]

for i in range(1, self.nr):
    # subtitution bytes
    for j in range(4):
        for k in range(4):
            ps[j][k] = sb[ps[j][k]]

    # add round key
    for j in range(4):
        for k in range(4):
            ps[j][k] ^= self._km[i][j][k]

    # shifting rows
    ps[0][2], ps[1][2], ps[2][2], ps[3][2] = ps[2][2], ps[3][2], ps[0][2], ps[1][2]
    ps[0][1], ps[1][1], ps[2][1], ps[3][1] = ps[1][1], ps[2][1], ps[3][1], ps[0][1]
    ps[0][3], ps[1][3], ps[2][3], ps[3][3] = ps[3][3], ps[0][3], ps[1][3], ps[2][3]

    # mixing columns
    for j in range(4):
        t = ps[j][0] ^ ps[j][1] ^ ps[j][2] ^ ps[j][3]
        u = ps[j][0]
        ps[j][0] ^= t ^ x(ps[j][0] ^ ps[j][1])
        ps[j][1] ^= t ^ x(ps[j][1] ^ ps[j][2])
        ps[j][2] ^= t ^ x(ps[j][2] ^ ps[j][3])
        ps[j][3] ^= t ^ x(ps[j][3] ^ u)

# subtitution bytes
for i in range(4):
    for j in range(4):
        ps[i][j] = sb[ps[i][j]]

# add round key
for i in range(4):
    for j in range(4):
        ps[i][j] ^= self._km[-1][i][j]

# shifting rows
ps[0][3], ps[1][3], ps[2][3], ps[3][3] = ps[3][3], ps[0][3], ps[1][3], ps[2][3]
ps[0][1], ps[1][1], ps[2][1], ps[3][1] = ps[1][1], ps[2][1], ps[3][1], ps[0][1]
ps[0][2], ps[1][2], ps[2][2], ps[3][2] = ps[2][2], ps[3][2], ps[0][2], ps[1][2]
```

knowing what each part are, we just need to read it backwards.

```
inv_shift_rows(cipher_state)
add_round_key(cipher_state, self._key_matrices[-1])
inv_sub_bytes(cipher_state)

for i in range(self.n_rounds - 1, 0, -1):
    inv_mix_columns(cipher_state)
    inv_shift_rows(cipher_state)
    add_round_key(cipher_state, self._key_matrices[i])
    inv_sub_bytes(cipher_state)

add_round_key(cipher_state, self._key_matrices[0])
```

Flag: ITSEC{I'm_Seriously_Sorry_For_This}