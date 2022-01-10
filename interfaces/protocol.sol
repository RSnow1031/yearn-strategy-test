// SPDX-License-Identifier: AGPL-3.0
pragma solidity 0.6.12;
pragma experimental ABIEncoderV2;

interface IProtocol {

    /**
     * @notice
     * Provide the `_amount` of `want` tokens to the liquidity pool and receives `lpToken` (liquidity provider tokens).
     * The `want` tokens are added to the liquidity pool and `lpToken` are minted to the msg.sender
     * 
     * @param _amount How much `want` to deposit
     */
    function deposit(uint256 _amount) external;

    /**
     * @notice
     * Provide the `_amount` of `lpToken` tokens to the liquidity pool and redeems `want` tokens.
     * 
     * @param _amount How much `lpToken` to deposit
     */
    function withdraw(uint256 _amount) external;

    /**
     * @notice
     * Claim the `rewardToken` (reward tokens).
     * Reward tokens are paid over time to the `lpToken` holders.
     * Here, msg.sender can receive `rewardToken` by calling this function.
     */
    function claimRewards() external;

}
