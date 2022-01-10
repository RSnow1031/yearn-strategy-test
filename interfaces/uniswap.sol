// SPDX-License-Identifier: AGPL-3.0
pragma solidity 0.6.12;
pragma experimental ABIEncoderV2;

interface IUniswap {

    /**
     * Given an input asset amount and an array of token addresses, 
     * calculates all subsequent maximum output token amounts by 
     * calling getReserves for each pair of token addresses in the path 
     * in turn, and using these to call getAmountOut.
     */
    function getAmountsOut(
        uint256, 
        address[] calldata
    ) external view returns (uint256[] memory);

    /**
     * Swaps an exact amount of input tokens for as many output tokens 
     * as possible, along the route determined by the path. 
     * The first element of path is the input token, the last is the output token, 
     * and any intermediate elements represent intermediate pairs to trade through 
     * (if, for example, a direct pair does not exist).
     */
    function swapExactTokensForTokens(
        uint256,
        uint256,
        address[] calldata,
        address,
        uint256
    ) external;
}
