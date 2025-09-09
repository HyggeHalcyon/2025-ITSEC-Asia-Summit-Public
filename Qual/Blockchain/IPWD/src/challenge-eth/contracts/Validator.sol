// SPDX-License-Identifier: INJU
pragma solidity ^0.8.28;

import "./ERC20/ERC20.sol";

contract Validator is ERC20{
    address public owner;


    constructor() ERC20("Validator", "VLDTR"){
        owner = msg.sender;
        _mint(owner, 100);
    }

    function mint(address _to, uint256 amount) external onlyOwner{
        _mint(_to, amount);
    }

    modifier onlyOwner{
        require(msg.sender == owner, "VALIDATOR: Only Owner Function");
        _; 
    }

}