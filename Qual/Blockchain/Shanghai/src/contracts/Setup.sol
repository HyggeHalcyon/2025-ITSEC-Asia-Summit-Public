// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.23;

contract Setup {
    address public yourContract;
    bytes32 public codeHash;
    bool public isSolved = false;

    constructor() payable {}

    function stage1(address _yourcontract) public {
        require(_yourcontract != address(0), "Invalid contract address");

        uint256 size;
        assembly {
            size := extcodesize(_yourcontract)
        }
        require(size > 0, "Contract not deployed");
        
        yourContract = _yourcontract;
        codeHash = _yourcontract.codehash;
    }

    function stage2() public {
        require(yourContract != address(0), "Your contract not set");
        require(codeHash != bytes32(0), "Code hash not set");

        require(yourContract.codehash != codeHash, "Code hasn't been upgraded");

        isSolved = true;
    }
}
