// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract ChovidPrize {
    bytes public encodedPrize;
    bool public isPrizeActive = false;
    uint256 public lastPrizeId = 0;
    uint256 public lastBlockNumber;
    address private owner;

    constructor() {
        owner = msg.sender;
    }

    function createPrize(address receiver) external returns (uint256) {
        require(receiver != owner, "Receiver cannot be owner");
        uint256 id = ++lastPrizeId;
        bytes memory encoded = abi.encodePacked(
            id,
            receiver,
            uint256(1_000_000_000)
        );
        encodedPrize = encoded;
        isPrizeActive = true;
        lastBlockNumber = block.number;
        return id;
    }

    function redeemPrize(bytes calldata hookData) public returns (uint256) {
        require(hookData.length <= 200_000, "Hook data too large");
        require(isPrizeActive, "Prize not active");
        require(lastBlockNumber < block.number, "Too early to claim");
        lastBlockNumber = block.number;

        bytes memory encoded = abi.encodePacked(encodedPrize, hookData.length, hookData);
        uint256 hookDataSize = hookData.length;
        assembly {
            let dataLength := mload(encoded)
            let newEncoded := mload(0x40)
            mstore(0x40, add(newEncoded, add(0x20, dataLength)))
            pop(staticcall(gas(), 0x4, encoded, add(0x20, dataLength), newEncoded, add(0x20, dataLength)))
            
            let amountToBeRedeemed := mload(add(newEncoded, 0x54))
            if gt(amountToBeRedeemed, 0) {
                mstore(add(newEncoded, 0x54), sub(amountToBeRedeemed, 1))
            }
            if eq(amountToBeRedeemed, 0) {
                mstore(0x00, sload(lastPrizeId.slot))
                return(0x00, 0x20)
            }
            let receiver := mload(add(newEncoded, 0x34))
            if gt(hookDataSize, 0) {
                pop(call(gas(), receiver, 0, add(hookData.offset, 0x20), hookDataSize, 0, 0))
            }
            if eq(caller(), receiver) {
                mstore(0x00, sload(lastPrizeId.slot))
                return(0x00, 0x20)
            }
        }

        bytes memory data = encodedPrize;
        uint256 id;
        address receiver;
        uint256 amount;
        assembly {
            id := mload(add(data, 0x20))
            receiver := mload(add(data, 0x34))
            amount := mload(add(data, 0x54))
        }
        bytes memory newEncodedPrize = abi.encodePacked(id, receiver, amount - 1);
        encodedPrize = newEncodedPrize;
        return 0;
    }
}
