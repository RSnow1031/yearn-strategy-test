# TODO: Add tests that show proper migration of the strategy to a newer one
#       Use another copy of the strategy to simulate the migration
#       Show that nothing is lost!

import pytest
from brownie import StrategyTest

def test_migration(
    chain,
    token,
    vault,
    strategy,
    amount,
    lp_token,
    Strategy,
    strategist,
    gov,
    user,
    RELATIVE_APPROX,
):

    # Deposit to the vault and harvest
    token.approve(vault, amount, {"from": user})
    vault.deposit(amount, {"from": user})
    chain.sleep(1)
    strategy.harvest()
    assert pytest.approx(strategy.estimatedTotalAssets(), rel=RELATIVE_APPROX) == amount

    # migrate to a new strategy
    new_strategy = strategist.deploy(StrategyTest, vault)
    vault.migrateStrategy(strategy, new_strategy, {"from": gov})
    assert pytest.approx(new_strategy.estimatedTotalAssets(), rel=RELATIVE_APPROX) == amount

    assert lp_token.balanceOf(strategy) == 0
    assert lp_token.balanceOf(new_strategy) > 0
