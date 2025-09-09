// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract CreateFactory {

    function deploy(bytes memory bytecode) public returns (address deployedContract) {
        assembly {
            deployedContract := create(0, add(bytecode, 0x20), mload(bytecode))
        
            if iszero(deployedContract) {
                revert(0, 0)
            }
        }
    }

    function destroy() public{
        selfdestruct(payable(msg.sender));
    }
}