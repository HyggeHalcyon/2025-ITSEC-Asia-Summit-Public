# IPWD

TL;DR
1. Get enough token from Validator (abusing transfer and unchecked receiver)
2. Register yourself 
3. Register helper contract (referal can be read from storage)
4. Since the contract check-switch is not protected, can easily turn it off
5. Use the helper to request mint token with max number
6. Sell all the token and retrieve the ether 
        NOTE: Step 3 to 5 is using the delegatecall msg.value reuse vuln and executed using the multicall function
7. reset the contract check to false 
8. set the player as your address 
   
