from brownie import NFTBoxes, JOYtoys, accounts, chain, interface, Wei
from time import sleep

def main():
    user = accounts.load('moist')
    # box = NFTBoxes.at('0x637a3710f4B9b79dC9512Dadd7DdF36C3063023D')
    # joy = JOYtoys.at('0xB61E4789662621b16064dD21e8a8173a85A4a3E0')
    box = NFTBoxes.deploy({'from':user}, publish_source=True)
    joy = JOYtoys.deploy({'from':user}, publish_source=True)
    box.transferOwnership('0x63a9dbCe75413036B2B778E670aaBd4493aAF9F3', {'from':user})
    joy.transferOwnership('0x63a9dbCe75413036B2B778E670aaBd4493aAF9F3', {'from':user})
    # joy.setCaller(box, True, {'from':user})
    # box.setVendingMachine(joy, {'from': user})
    # box.createBoxMould(40, Wei('0 ether'), [5, 6, 7, 8, 9, 10, 11, 12, 13, 14], [], [], "This is a test box", {'from':user})
    # for i in range(5, 15):
    #     joy.createJOYtoy("c0ffee", "someType", "over 9000", "toy", "fun", 100, True, 0, 0, {'from':user})
    # for j in range(40):
    #     box.buyBox(1, {'from':user, "value": Wei("0 ether")})
    # for i in range(10):
    #     box.distribute(1, 4,{'from':user})

# Transaction sent: 0x7542064deb91244495173878730898ab95fd79e2facfc242fe7c56034e7d98b1
#   Gas price: 1.0 gwei   Gas limit: 3297878   Nonce: 807
#   NFTBoxes.constructor confirmed - Block: 7848388   Gas used: 2998071 (90.91%)
#   NFTBoxes deployed at: 0x637a3710f4B9b79dC9512Dadd7DdF36C3063023D

# Transaction sent: 0x0b3c684611b0de4e2d8fbd3ba85080a01a0ae91db3251b097006370ec904a642
#   Gas price: 1.0 gwei   Gas limit: 4532105   Nonce: 808
#   JOYtoys.constructor confirmed - Block: 7848389   Gas used: 4120096 (90.91%)
#   JOYtoys deployed at: 0xB61E4789662621b16064dD21e8a8173a85A4a3E0