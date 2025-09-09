// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.23;

contract Two {
    address public whenyhsejagowrth;

    constructor() {
        whenyhsejagowrth = msg.sender;
    }

    function donate() public payable {
        require(msg.value > 0, "Donation must be greater than 0");
    }

    function withdraw() public {
        require(msg.sender == whenyhsejagowrth, "Only the owner can withdraw funds");
        uint256 whenyhsejagozafin = address(this).balance;
        require(whenyhsejagozafin > 0, "No funds to withdraw");
        (bool success, ) = whenyhsejagowrth.call{value: whenyhsejagozafin}("");
        require(success, "Failed to withdraw funds");
    }

    function destroy() public{
        selfdestruct(payable(msg.sender));
    }
}
