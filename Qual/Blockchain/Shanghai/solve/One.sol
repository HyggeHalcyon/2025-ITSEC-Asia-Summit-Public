// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.23;

contract One {
    uint256 private whenyhsejagohanz;

    event ValueUpdated(uint256 _oldValue, uint256 _newValue);

    function set(uint256 _whenyhsejagofahrul) public {
        emit ValueUpdated(whenyhsejagohanz, _whenyhsejagofahrul);
        whenyhsejagohanz = _whenyhsejagofahrul;
    }

    function get() public view returns (uint256) {
        return whenyhsejagohanz;
    }

    function destroy() public{
        selfdestruct(payable(msg.sender));
    }
}
