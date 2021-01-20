from brownie import NFTBoxes, JOYtoys, accounts, chain, interface, Wei, web3
from time import sleep

def main():
    # user2 = accounts.load('owl')
    user = accounts.load('moist')
    box = NFTBoxes.at('0xfa4Ff49c6ab0Ad4Fc2f5729F2807a28D497Db5c3')
    # joy = JOYtoys.at('0x4de525edb160dc7b773cd249554d8ba98c550d07')
    # box = NFTBoxes.deploy({'from':user}, publish_source=False)
    # print(box.kecc('0x6b81fc5c9ff7a165c1f5254bc7dff5280dbc1d7d6d2f16a3cb9de105b1b67567'))
    # joy = JOYtoys.deploy({'from':user}, publish_source=False)
    joy = JOYtoys.at('0x59b37C410ead4a9CD1515E515a6135cA7Ec51c60')
    # box.transferOwnership('0x63a9dbCe75413036B2B778E670aaBd4493aAF9F3', {'from':user})
    # joy.transferOwnership('0x63a9dbCe75413036B2B778E670aaBd4493aAF9F3', {'from':user})
    # joy.setCaller(box, True, {'from':user})
    # joy.createJOYtoy("c0ffee", "someType", "over 9000", "toy", "fun", 100, True, 0, 0, {'from':user})
    # joy.setCaller(user, True, {'from':user})
    joy.JOYtoyMachineFor(1, user, {'from':user})
    joy.JOYtoyMachineFor(1, user, {'from':user})
    joy.JOYtoyMachineFor(1, user, {'from':user})
    # box.setVendingMachine(joy, {'from': user})
    # box.createBoxMould(40, Wei('0 ether'), [1, 2, 3, 4, 5, 6, 7, 8], [], [], "This is a test box", {'from':user})
    # box.buyManyBoxes(1, 20, {'from':user})
    # box.buyManyBoxes(1, 20, {'from':user2})
    # for i in range(8):
    #     joy.createJOYtoy("c0ffee", "someType", "over 9000", "toy", "fun", 100, True, 0, 0, {'from':user})

