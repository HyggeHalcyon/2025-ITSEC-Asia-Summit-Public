# Bank of People

Category: Blockchain
Difficulty: Medium
Author: Enkidu

## Writeup
TL;DR

1. Attach your wallet to a smart contract (can be done sooner or later, before withdrawing)
2. Notice that to get the HP of BOP down you need to trigger the healthcheck
3. Regist and deposit some funds, make sure you have enough for the next step
4. "safely" create a "failing" account with gas griefing for isolatedAccount
5. trigger the fail check on applyForLoan
6. reentrancy your way to drain the contract