pragma solidity ^0.6.12;
pragma experimental ABIEncoderV2;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";

contract TestNFT is ERC721("NFT test Boxes", "TEST") {
	function mint(address _recipient, uint256 _id) public {
		_mint(_recipient, _id);
	}
}