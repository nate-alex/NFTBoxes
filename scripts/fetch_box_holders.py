from brownie import NFTBoxes, web3
import csv

def main():
    boxId = 1
    seedStr = '0x6b81fc5c9ff7a165c1f5254bc7dff5280dbc1d7d6d2f16a3cb9de105b1b67569'
    byteSeed = web3.toBytes(hexstr=seedStr)
    seed  = web3.soliditySha3(['bytes32'], [byteSeed])
    seedInt = web3.toInt(seed)
    box = NFTBoxes.at('0xfa4Ff49c6ab0Ad4Fc2f5729F2807a28D497Db5c3')
    print(f'Box contract at {box.address}\nFetching holders of box edition {boxId}...')
    ids = box.getIdsLength(boxId)
    box_contract = web3.eth.contract(address=box.address, abi=box.abi)
    filt = box_contract.events.BoxBought.createFilter(fromBlock=0, toBlock= 'latest', argument_filters={'boxMould':boxId})
    res = filt.get_all_entries()
    holders = [box.ownerOf(e.args.tokenId) for e in res]
    print(f'Box holders fetched. Size: {len(holders)}\nExecuting distribution from initial seed: {seedStr}')
    dissArr = []
    for i in range(ids):
        dissArr.append([h for h in holders])
    winnerArray = []
    for i in range(len(holders)):
        tempWinnerArray = []
        for j in range(ids):
            indexWinner = seedInt % len(dissArr[j])
            winner = dissArr[j][indexWinner]
            (seed, seedInt) = newSeed(seed, web3)
            tempWinnerArray.append(winner)
            dissArr[j].pop(indexWinner)
        winnerArray.append([w for w in tempWinnerArray])
        tempWinnerArray.clear()
    print(f'Distribution finished, writing data onto boxHolders_{boxId}.csv...')
    wtr = csv.writer(open (f'boxHolders_{boxId}.csv', 'w'), delimiter=',', lineterminator='\n')
    for x in winnerArray:
        wtr.writerow (x)
    print('done')

def newSeed(seed, web3):
    seed = web3.soliditySha3(['bytes32'], [seed])
    return (seed, web3.toInt(seed))