pragma solidity ^0.6.12;

contract Controller {
	address public owner;

	constructor() public {
		owner = msg.sender;
	}

	modifier onlyOwner() {
		require(msg.sender == owner, "Controller: You are not the owner.");
		_;
	}

	function transferOwnership(address _newOwner) public onlyOwner {
		owner = _newOwner;
	}
}