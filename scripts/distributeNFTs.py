from brownie import NFTBoxes, accounts
import csv

def main():
    user = accounts.load('moist')

    boxId = 1
    offset = 0
    box = NFTBoxes.at('0xfa4Ff49c6ab0Ad4Fc2f5729F2807a28D497Db5c3')
    dissArr = []
    with open(f'boxHolders_{boxId}.csv') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            dissArr.append(row)

    batchSize = 50 // len(dissArr[0])
    loops = len(dissArr) // batchSize + (1 if len(dissArr) % batchSize > 0 else 0)
    print(f'Batch size: {batchSize} - loops: {loops}')
    for i in range(offset, loops):
        print(f'Sending batch #{i + 1} out of {loops}')
        if i == loops - 1:
            print(f'range[{i * batchSize}:end]')
            users = dissArr[i * batchSize:]
        else:
            print(f'range[{i * batchSize}:{(i + 1) * batchSize}]')
            users = dissArr[i * batchSize : (i + 1) * batchSize]
        box.distributeOffchain(boxId, users, {'from':user})
