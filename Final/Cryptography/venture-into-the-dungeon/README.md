# Venture Into the Dungeon

Category: Cryptography
Difficulty: Medium
Author: EternalBeats

## Description

The dungeon's entrance groans open as the party pushes aside the moss-covered stone door. A breath of stale, cool air rushes out, carrying with it the scent of forgotten battles and dust. The flicker of your torches catches faint carvings on the walls-warnings in an old tongue about "the toll of secrets" and "the weight of sloth."

Slumped against the wall is a man in tattered leather armor, a rusty sword leaning beside him. His hair is a tangled mess, his eyes half-closed, and his breathing slow, almost exaggerated. When you approach, he doesn't greet you, he just mutters something that sounds like,
"**...wake me up when the dungeon's cleared...**", it seems that only a certain command will wake this man up.

Opposite him stands a hunched figure draped in robes the color of ash, a hood obscuring their face. The only thing visible is a pale grin beneath the shadows. When you greet them, their voice rasps out,
"Information... yes, I have much. But words are weighty things, adventurers. **Payment must match the value.**"

Both figures clearly hold pieces of the puzzle. The lazy man might prove to be a powerful ally once roused, and the secret-keeper might reveal crucial truths about the dungeon's traps and treasures, but neither will cooperate easily.

Author: EternalBeats

## Writeup
RSA decrypt function?, LSB still intact? RSA Oracle is possible.

RSA Parity Oracle is just a way to recover encrypted data, using the knowledge from oracle, even if it's only odd or even. Why is that?

TLDR;
- 2 * message should always be even
- but proper modulus is odd

this make it possible to determine where 2 * message will falls into
if even:
2M < n meaning M < n/2

if odd:
2M > n meaning m > n/2

it's also possible with 4M, 8M, etc. Looping this logic, we can determine where M is placed into in regards of n

Mode Indepth explaination:
https://medium.com/dataseries/robots-oracles-and-protocols-breaking-cryptography-through-information-leakage-3a1e73c9483a
https://secgroup.dais.unive.it/wp-content/uploads/2012/11/Practical-Padding-Oracle-Attacks-on-RSA.html