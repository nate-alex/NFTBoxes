pragma solidity ^0.6.12;
pragma experimental ABIEncoderV2;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "../interfaces/IVendingMachine.sol";
import "./Controller.sol";

contract NFTBoxes is ERC721("NFT Boxes", "BOX"), Controller {

	struct BoxMould{
		uint8				live; // bool
		uint8				shared; // bool
		uint128				maxEdition;
		uint128				currentEditionCount;
		uint128				checkpoint;
		uint256				price;
		uint256				seed;
		uint256[]			ids;
		address payable[]	artists;
		uint256[]			shares;
		string				name;
	}

	struct Box {
		uint256				boxId;
		uint256				edition;
	}

	IVendingMachine public	vendingMachine;
	uint256 public			boxMouldCount;

	uint256 constant public TOTAL_SHARES = 1000;

	mapping(uint256 => BoxMould) public	boxMoulds;
	mapping(uint256 =>  Box) public	boxes;

	mapping(uint256 =>mapping(uint256 => address[])) dissArr;

	mapping(address => uint256) public teamShare;
	address payable[] public team;

	event BoxMouldCreated(uint256 id);
	event BoxBought(uint256 id);

	function addTeamMember(address payable _member) external onlyOwner {
		for (uint256 i = 0; i < team.length; i++)
			require( _member != team[i], "NFTBoxes: members exists already");
		team.push(_member);
	}

	function setTeamShare(address _member, uint _share) external onlyOwner {
		require(_share < TOTAL_SHARES, "NFTBoxes: share must be below 1000");
		for (uint256 i = 0; i < team.length; i++)
			if (team[i] == _member)
				teamShare[_member] = _share;
	}

	function createBoxMould(
		uint128 _max,
		uint256 _price,
		uint256[] memory _ids,
		address payable[] memory _artists,
		uint256[] memory _shares,
		string memory _name)
		external onlyOwner{
		require(_artists.length == _shares.length, "NFTBoxes: arrays are not of same length.");
		BoxMould memory boxMould = BoxMould({
			live: uint8(0),
			shared: uint8(0),
			maxEdition: _max,
			currentEditionCount: 0,
			checkpoint: 0,
			price: _price,
			seed: 0,
			ids: _ids,
			artists: _artists,
			shares: _shares,
			name: _name
		});
		boxMoulds[boxMouldCount] = boxMould;
		boxMouldCount++;
		// add event
		// ask nate about metadata stuff
	}

	// dont even need this tbh?
	function getArtistRoyalties(uint256 _id) external view returns (address payable[] memory artists, uint256[] memory royalties) {
		require(boxMouldCount > _id, "NFTBoxes: ID does not exist.");
		BoxMould memory boxMould = boxMoulds[_id];
		artists = boxMould.artists;
		royalties = boxMould.shares;
	}

	function buyBox(uint256 _id) external payable {
		BoxMould storage boxMould = boxMoulds[_id];
		require(boxMould.live == 0, "NFTBoxes: Box is no longer buyable.");
		require(msg.value == boxMould.price, "NFTBoxes: Wrong price.");

		boxes[totalSupply()] = Box(_id, boxMould.currentEditionCount);
		for (uint256 i = 0; i < boxMould.ids.length; i++)
			dissArr[_id][i].push(msg.sender);
		boxMould.currentEditionCount++;
		if (boxMould.currentEditionCount == boxMould.maxEdition)
			boxMould.live = uint8(1);

		//safe mint?
		_mint(msg.sender, totalSupply());
	}

	function setVendingMachine(address _machine) external  onlyOwner{
		vendingMachine = IVendingMachine(_machine);
	}

	function distribute(uint256 _id, uint128 _amount) external  onlyOwner{
		BoxMould storage boxMould= boxMoulds[_id];
		require(boxMould.live == 1, "NTFBoxes: Box is still live, cannot start distribution");
		require (boxMould.checkpoint + _amount <= boxMould.currentEditionCount, "NFTBoxes: minting too many NFTs.");

		uint256 _seed = boxMould.seed == 0 ? _getNewSeed(0, msg.sender) : boxMould.seed;
		uint128 _check = boxMould.checkpoint;
		for (uint128 i = _check; i < _check + _amount; i++) {
			for (uint256 j = 0; j < boxMould.ids.length; j++) {
				_seed = _getNewSeed(_seed, address(0));
				uint256 index = _seed % dissArr[_id][j].length;
				address winner = dissArr[_id][j][index];
				dissArr[_id][j][index] = dissArr[_id][j][dissArr[_id][j].length - 1];
				dissArr[_id][j].pop();
				vendingMachine.JOYtoyMachineFor(boxMould.ids[j], winner);
			}
		}
		boxMould.checkpoint += uint128(_amount);
		boxMould.seed = _seed;
	}

	function distributeShares(uint256 _id) external {
		BoxMould storage boxMould= boxMoulds[_id];
		require(_id < boxMouldCount, "NFTBoxes: Box does not exist.");
		require(boxMould.live == 1 && boxMould.shared == 0,  "NFTBoxes: cannot distribute shares yet.");
		require(is100(_id), "NFTBoxes: shares do not add up to 100%.");

		boxMould.shared = 1;
		uint256 rev = uint256(boxMould.currentEditionCount) * boxMould.price;
		uint256 share;
		for (uint256 i = 0; i < team.length; i++) {
			share = rev * teamShare[team[i]] / TOTAL_SHARES;
			team[i].transfer(share);
		}
		for (uint256 i = 0; i < boxMould.artists.length; i++) {
			share = rev * boxMould.shares[i] / TOTAL_SHARES;
			boxMould.artists[i].transfer(share);
		}
	}

	function is100(uint256 _id) internal returns(bool) {
		BoxMould storage boxMould= boxMoulds[_id];
		uint256 total;
		for (uint256 i = 0; i < team.length; i++) {
			total += teamShare[team[i]];
		}
		for (uint256 i = 0; i < boxMould.shares.length; i++) {
			total += boxMould.shares[i];
		}
		return total == TOTAL_SHARES;
	}

	function _getNewSeed(uint256 _seed, address _sender) internal view returns (uint256) {
		if (_seed == 0)
			return uint256(keccak256(abi.encodePacked(block.timestamp, block.difficulty, _sender)));
		else
			return uint256(keccak256(abi.encodePacked(_seed)));
	}

}