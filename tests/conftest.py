import pytest
from brownie import config
from brownie import Contract


@pytest.fixture
def gov(accounts):
    yield accounts.at("0xFEB4acf3df3cDEA7399794D0869ef76A6EfAff52", force=True)


@pytest.fixture
def user(accounts):
    yield accounts[0]


@pytest.fixture
def rewards(accounts):
    yield accounts[1]


@pytest.fixture
def guardian(accounts):
    yield accounts[2]


@pytest.fixture
def management(accounts):
    yield accounts[3]


@pytest.fixture
def strategist(accounts):
    yield accounts[4]


@pytest.fixture
def keeper(accounts):
    yield accounts[5]


@pytest.fixture
def token_liquidity(accounts):
    yield accounts.at("0xbe0eb53f46cd790cd13851d5eff43d12404d33e8", force=True)


@pytest.fixture
def token():
    token_address = "0x1f9840a85d5af5bf1d1762f925bdaddc4201f984"  # this should be the address of the ERC-20 used by the strategy/vault
    yield Contract(token_address)


@pytest.fixture
def amount(accounts, token, user):
    amount = 10_000 * 10 ** token.decimals()
    # In order to get some funds for the token you are about to use,
    # it impersonate an exchange address to use it's funds.
    reserve = accounts.at("0xbe0eb53f46cd790cd13851d5eff43d12404d33e8", force=True)
    token.transfer(user, amount, {"from": reserve})
    yield amount


@pytest.fixture
def weth():
    token_address = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
    yield Contract(token_address)


@pytest.fixture
def weth_amout(user, weth):
    weth_amout = 10 ** weth.decimals()
    user.transfer(weth, weth_amout)
    yield weth_amout


@pytest.fixture
def vault(pm, gov, rewards, guardian, management, token):
    Vault = pm(config["dependencies"][0]).Vault
    vault = guardian.deploy(Vault)
    vault.initialize(token, gov, rewards, "", "", guardian, management)
    vault.setDepositLimit(2 ** 256 - 1, {"from": gov})
    vault.setManagement(management, {"from": gov})
    yield vault


@pytest.fixture
def strategy(
    strategist,
    guardian,
    keeper,
    vault,
    StrategyTest,
    gov,
    want_pool,
    reward_token,
    unirouter,
    lp_token,
):
    strategy = guardian.deploy(
        StrategyTest,
        vault,
        want_pool,
        reward_token,
        unirouter,
        lp_token,
    )
    strategy.setKeeper(keeper)
    vault.addStrategy(strategy, 10_000, 0, 2 ** 256 - 1, 1_000, {"from": gov})
    yield strategy


@pytest.fixture
def unirouter():  # unirouter contract
    yield Contract("0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D")


@pytest.fixture
def want_pool():  # random address not working
    yield Contract("0x0650d780292142835F6ac58dd8E2a336e87b4393")


@pytest.fixture
def reward_token():  # random address not working
    yield Contract("0x0cec1a9154ff802e7934fc916ed7ca50bde6844e")


@pytest.fixture
def lp_token():  # random address not working
    yield Contract("0xa92a861fc11b99b24296af880011b47f9cafb5ab")


@pytest.fixture
def newstrategy(
    strategist,
    guardian,
    keeper,
    vault,
    StrategyTest,
    gov,
    want_pool,
    reward_token,
    unirouter,
    lp_token,
):
    newstrategy = guardian.deploy(
        StrategyTest,
        vault,
        want_pool,
        reward_token,
        unirouter,
        lp_token,
    )
    newstrategy.setKeeper(keeper)
    yield newstrategy


@pytest.fixture(scope="session")
def RELATIVE_APPROX():
    yield 1e-5
