// SPDX-License-Identifier: INJU
pragma solidity ^0.8.28;

import "./ERC20/ERC20.sol";
import { IPWDAdministrator } from "./IPWDAdministrator.sol";

contract IPWD is ERC20{

    IPWDAdministrator public IPWDAdmin;

    address public Administrator;
    address public owner;
    bool public allowAllContracts;

    mapping(address => bool) public whitelistedAddress;
    mapping(address => bool) public blacklistedAddress;

    error exceedMaximumWithdrawal(address holder);

    constructor(
        bool _allowContracts
    ) ERC20("IPWD Token", "IPWD") {
        owner = msg.sender;
        allowAllContracts = _allowContracts;
    }

    function transfer(address recipient, uint256 amount) public override onContractDetected(recipient) returns (bool) {
        return super.transfer(recipient, amount);
    }

    function transferFrom(address sender, address recipient, uint256 amount)
        public override onContractDetected(recipient) returns (bool) 
    {
        return super.transferFrom(sender, recipient, amount);
    }

    function approve(address spender, uint256 amount) public override onContractDetected(spender) returns (bool) {
        return super.approve(spender, amount);
    }

    function mint(
        address _to,
        uint256 _amount
    ) external onContractDetected(_to) onlyAdministrator{
        _mint(_to, _amount);
    }

    function setAdministrator(address _addr) external onlyOwner{
        Administrator = _addr;
    }

    function isSmartContract(address _addr) public view returns (bool) {
        uint32 size;
        assembly {
            size := extcodesize(_addr)
        }
        return (size > 0);
    }

    function addWhiteList(address _addr) external onlyOwner {
        whitelistedAddress[_addr] = true;
    }

    function addBlackList(address _addr) external onlyOwner {
        blacklistedAddress[_addr] = true;
    }
   
    function removeWhiteList(address _addr) external onlyOwner{
        whitelistedAddress[_addr] = false;
    }

    function removeBlackList(address _addr) external onlyOwner{
        blacklistedAddress[_addr] = false;
    }

    function updateAllowContractStatus(bool _status) external {
        allowAllContracts = _status;
    }

    function getBalance(address _addr) external view returns(uint256){
        return balanceOf(_addr);
    }

    function getAddressStatus(address _addr) external view returns(bool, bool){
        return (whitelistedAddress[_addr], blacklistedAddress[_addr]);
    }

    modifier onlyOwner {
        require(msg.sender == owner, "Owner-level required");
        _;
    }
 
    modifier onlyAdministrator {
        require(msg.sender == Administrator, "Administrator-level required");
        _;
    }

    modifier onContractDetected(address _addr){
        if(_addr != Administrator){
            if(isSmartContract(_addr)){
                if(!allowAllContracts){
                    require(whitelistedAddress[_addr], "Only Whitelisted is allowed!");
                }
                if(allowAllContracts){
                    require(!blacklistedAddress[_addr], "Blacklisted address is not allowed!");
                }
            }
        }
        _;
    }



}