// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./ChovidPrize.sol";

contract Setup {
    ChovidPrize public chovidPrize;
    bool solved = false;

    constructor() {
        chovidPrize = new ChovidPrize();
    }

    function solve(bytes calldata hookData) external {
        if (chovidPrize.redeemPrize(hookData) == 1) {
            solved = true;
        }
    }

    function isSolved() public view returns (bool) {
        return solved;
    }
}
