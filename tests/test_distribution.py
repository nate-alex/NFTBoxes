import pytest
import brownie
from brownie import Wei

def test_box(nftbox, minter, accounts):
    nftbox.createBoxMould(50, Wei('0.1 ether'), [1, 2, 3, 4], [], [], "This is a test box", {'from':minter})
    nftbox.createBoxMould(25, Wei('.20 ether'), [5, 6], [], [], "This is a second test box", {'from':minter})
    u1 = accounts[0]
    u2 = accounts[1]
    nftbox.buyBox(0, {'from':u1, "value": Wei("0.1 ether")})
    nftbox.buyBox(0, {'from':u2, "value": Wei("0.1 ether")})
    nftbox.buyBox(1, {'from':u1, "value": Wei("0.2 ether")})
    nftbox.buyBox(1, {'from':u2, "value": Wei("0.2 ether")})

    assert nftbox.ownerOf(0) == u1
    assert nftbox.ownerOf(1) == u2

    assert nftbox.boxes(0) == (0, 0)
    assert nftbox.boxes(1) == (0, 1)
    assert nftbox.boxes(2) == (1, 0)
    assert nftbox.boxes(3) == (1, 1)

def test_many_of_one(nftbox, minter, accounts):
    nftbox.createBoxMould(50, Wei('0.01 ether'), [1, 2, 3, 4], [], [], "This is a test box", {'from':minter})
    nftbox.createBoxMould(20, Wei('0.1 ether'), [1, 2, 3, 4], [], [], "This is a test box", {'from':minter})
    for j in range(5):
        nftbox.buyBox(1, {'from':accounts[0], "value": Wei("0.1 ether")})
    supply = nftbox.totalSupply()
    for i in range(10):
        nftbox.buyBox(0, {'from':accounts[0], "value": Wei("0.01 ether")})
        assert nftbox.ownerOf(2 * i + supply) == accounts[0]
        assert nftbox.boxes(2 * i + supply) == (0, i * 2)
        nftbox.buyBox(0, {'from':accounts[1], "value": Wei("0.01 ether")})
        assert nftbox.ownerOf(2 * i + supply + 1) == accounts[1]
        assert nftbox.boxes(2 * i + 1 + supply) == (0, i * 2 + 1)

def test_not_buyable_edition_over(nftbox, minter, accounts):
    nftbox.createBoxMould(5, Wei('0.01 ether'), [1, 2, 3, 4], [], [], "This is a test box", {'from':minter})
    for j in range(5):
        nftbox.buyBox(0, {'from':accounts[0], "value": Wei("0.01 ether")})
    with brownie.reverts("NFTBoxes: Box is no longer buyable."):
        nftbox.buyBox(0, {'from':accounts[0], "value": Wei("0.01 ether")})

def test_wrong_price(nftbox, minter, accounts):
    nftbox.createBoxMould(50, Wei('0.01 ether'), [1, 2, 3, 4], [], [], "This is a test box", {'from':minter})
    for j in range(5):
        nftbox.buyBox(0, {'from':accounts[0], "value": Wei("0.01 ether")})
    with brownie.reverts("NFTBoxes: Wrong price."):
        nftbox.buyBox(0, {'from':accounts[0], "value": Wei("1 ether")})

# def test_distribution(nftbox, minter, me, testnft, accounts):
#     nftbox.createBoxMould(100, Wei('0.01 ether'), [1, 2, 3, 4], [], [], "This is a test box", {'from':minter})
#     for j in range(10):
#         for k in range(10):
#             print(f'{j}.{k} buy')
#             nftbox.buyBox(0, {'from':accounts[j], "value": Wei("0.01 ether")})
#     nftbox.setNFT(testnft, {'from':minter})
#     for i in range(4):
#         print(f'distribute {i}')
#         nftbox.distribute2(0, 25,{'from':minter})
#     for l in range(10):
#         assert testnft.balanceOf(accounts[l]) == 40
#     for i in range(10):
#         print(f'Owner of #{i} - {testnft.ownerOf(i)}')
#     with brownie.reverts("NFTBoxes: minting too many NFTs."):
#         nftbox.distribute(0, 1,{'from':minter})

def test_distribution_with_machine_one(nftbox, joy, me, minter, accounts):
    joy.setCaller(nftbox, True, {'from':minter})
    nftbox.setVendingMachine(joy, {'from': minter})
    nftbox.createBoxMould(1, Wei('0.01 ether'), [1, 2, 3, 4], [], [], "This is a test box", {'from':minter})
    for i in range(1, 5):
        print(f'minting id {i}')
        joy.createJOYtoy("c0ffee", "someType", "over 9000", "toy", "fun", 100, True, 0, 0, {'from':minter})
    nftbox.buyBox(0, {'from':accounts[0], "value": Wei("0.01 ether")})
    nftbox.distribute(0, 1,{'from':minter})
    assert nftbox.balanceOf(accounts[0]) == 1
    assert joy.balanceOf(accounts[0]) == 4

def test_distribution_with_machine(nftbox, joy, minter, accounts):
    joy.setCaller(nftbox, True, {'from':minter})
    nftbox.setVendingMachine(joy, {'from': minter})
    nftbox.createBoxMould(20, Wei('0.01 ether'), [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [], [], "This is a test box", {'from':minter})
    for i in range(1, 11):
        joy.createJOYtoy("c0ffee", "someType", "over 9000", "toy", "fun", 100, True, 0, 0, {'from':minter})
    for j in range(10):
        for k in range(2):
            nftbox.buyBox(0, {'from':accounts[j], "value": Wei("0.01 ether")})
    for i in range(10):
        nftbox.distribute(0, 2,{'from':minter})
    for i in range(10):
        assert joy.balanceOf(accounts[i]) == 20

def test_distribution_with_machine2(nftbox, joy, minter, accounts):
    joy.setCaller(nftbox, True, {'from':minter})
    nftbox.setVendingMachine(joy, {'from': minter})
    nftbox.createBoxMould(20, Wei('0.01 ether'), [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], [], [], "This is a test box", {'from':minter})
    for i in range(1, 21):
        joy.createJOYtoy("c0ffee", "someType", "over 9000", "toy", "fun", 100, True, 0, 0, {'from':minter})
    for j in range(10):
        for k in range(2):
            print(f'{j}.{k} buy')
            nftbox.buyBox(0, {'from':accounts[j], "value": Wei("0.01 ether")})
    for i in range(10):
        print(f'distribute {i}')
        nftbox.distribute(0, 2,{'from':minter})
    for i in range(10):
        assert joy.balanceOf(accounts[i]) == 40

# def f():
# minter = accounts.at("0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2", force=True)
# box = NFTBoxes.deploy({'from':minter})
# box.createBoxMould(50, Wei('0.1 ether'), [1, 2, 3, 4], "This is a test box", {'from':minter})
# box.createBoxMould(25, Wei('1 ether'), [5, 6], "This is a second test box", {'from':minter})
# box.buyBox(0, {'from':minter, "value": Wei("0.1 ether")})
