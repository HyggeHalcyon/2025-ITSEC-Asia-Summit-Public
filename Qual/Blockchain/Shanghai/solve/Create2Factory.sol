// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Create2Factory {
    function deploy(bytes memory bytecode) public payable returns (address addr) {
        bytes32 salt = keccak256("idk");
        require(address(this).balance >= msg.value, "Insufficient funds");
        assembly {
            addr := create2(0, add(bytecode, 0x20), mload(bytecode), salt)
        }
        require(addr != address(0), "Deploy failed");
    }

    function computeAddress(bytes32 bytecodeHash) public view returns (address) {
        bytes32 salt = keccak256("idk");
        return address(uint160(uint256(keccak256(abi.encodePacked(
            bytes1(0xff),
            address(this),
            salt,
            bytecodeHash
        )))));
    }
} 