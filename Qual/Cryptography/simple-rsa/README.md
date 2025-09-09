# Simple RSA
TL;DR
1. Player need to notice the unusual 2049 bit (instead of 2048) for N and realize that N can be factorized using william's p+1. Player will found that p is 683 bits, while N/p is 1366 bits (2 x 683). This suggest that N/p is likely to be the product of two other primes, q and r. qr can be factorized with Fermat since q is close to r.
2. Player will likely attempt to calculate d with e and phi, but the decryption output will be wrong. This will lead player to investigate the non-standard e (which is nextprime(2^28)), but on its own, there is nothing wrong security-wise for e to be a prime bigger than 65537.
3. Player must found that gcd(e,q-1) != 1, this violates basic RSA requirement where e must be coprime with phi.
4. Realize the implication that d does not exist, and there will be e possible plaintext that results in the same ciphertext.
5. Understand that the general Adleman–Manders–Miller + CRT method is too slow because e is too big.
6. Utilize the algorithm developed by Shumow to efficiently retrieve possible plaintext, since it satisfies special condition where e is prime, gcd(phi,e) > 1, but gcd(phi,e^2) is 1 and gcd(phi,e^3) is 1, or in other words, there is only one prime affected by e.
7. Stop the search early and distinguish the flag from all possible plaintext using the known-plaintext part (starts with "ITSEC{"). Local bruteforce with efficient implementation tested on M1 chip completes in <30 minutes.

Possible Hints if needed:
Level1: N=pqr
Level2: https://eprint.iacr.org/2020/1059

# Ref
Incorrectly Generated RSA Keys: How To Recover Lost Plaintexts (by Daniel Shumow from Microsoft Research)
https://eprint.iacr.org/2020/1059