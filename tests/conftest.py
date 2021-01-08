import pytest


@pytest.fixture(scope="function", autouse=True)
def shared_setup(fn_isolation):
    pass


@pytest.fixture()
def minter(accounts):
    return accounts[0]
    # return accounts.at("0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2", force=True)

@pytest.fixture()
def me(accounts):
    return accounts.at("0xf521Bb7437bEc77b0B15286dC3f49A87b9946773", force=True)

@pytest.fixture()
def big(accounts):
    return accounts.at("0x1E0447b19BB6EcFdAe1e4AE1694b0C3659614e4e", force=True)

@pytest.fixture()
def nftbox(NFTBoxes, minter, accounts):
    return NFTBoxes.deploy({'from':accounts[0]})

@pytest.fixture()
def joy(JOYtoys, minter, accounts):
    return JOYtoys.deploy({'from':accounts[0]})

@pytest.fixture()
def testnft(TestNFT, minter):
    return TestNFT.deploy({'from':minter})
