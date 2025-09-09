//SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {Currency} from "../types/Currency.sol";
import {PoolId} from "../types/PoolId.sol";
import {PoolKey} from "../types/PoolKey.sol";
import {BalanceDelta} from "../types/BalanceDelta.sol";
import {IPoolManager} from "./IPoolManager.sol";
import {BinPosition, MartabakPool} from "../libraries/MartabakPool.sol";

interface IMartabakPoolManager is IPoolManager {
    /// @notice PoolManagerMismatch is thrown when pool manager specified in the pool key does not match current contract
    error PoolManagerMismatch();

    /// @notice Pool binStep cannot be lesser than 1. Otherwise there will be no price jump between bin
    error BinStepTooSmall();

    /// @notice Pool binstep cannot be greater than the limit set at MAX_BIN_STEP
    error BinStepTooLarge();

    /// @notice Error thrown when owner set max bin step too small
    error MaxBinStepTooSmall(uint16 maxBinStep);

    /// @notice Error thrown when amount specified is 0 in swap
    error AmountSpecifiedIsZero();

    /// @notice Returns the constant representing the max bin step
    /// @return maxBinStep a value of 100 would represent a 1% price jump between bin (limit can be raised by owner)
    function MAX_BIN_STEP() external view returns (uint16);

    /// @notice Returns the constant representing the min bin step
    /// @dev 1 would represent a 0.01% price jump between bin
    function MIN_BIN_STEP() external view returns (uint16);

    struct MintParams {
        bytes32[] liquidityConfigs;
        /// @dev amountIn intended
        bytes32 amountIn;
        /// the salt to distinguish different mint from the same owner
        bytes32 salt;
    }

    struct BurnParams {
        /// @notice id of the bin from which to withdraw
        uint256[] ids;
        /// @notice amount of share to burn for each bin
        uint256[] amountsToBurn;
        /// the salt to specify the position to burn if multiple positions are available
        bytes32 salt;
    }

    /// @notice Get the current value in slot0 of the given pool
    function getSlot0(PoolId id) external view returns (uint24 activeId, uint24 protocolFee, uint24 lpFee);

    /// @notice Returns the reserves of a bin
    /// @param id The id of the bin
    /// @return binReserveX The reserve of token X in the bin
    /// @return binReserveY The reserve of token Y in the bin
    /// @return binLiquidity The liquidity in the bin
    function getBin(PoolId id, uint24 binId)
        external
        view
        returns (uint128 binReserveX, uint128 binReserveY, uint256 binLiquidity);

    /// @notice Returns the positon of owner at a binId
    /// @param id The id of PoolKey
    /// @param owner Address of the owner
    /// @param binId The id of the bin
    /// @param salt The salt to distinguish different positions for the same owner
    function getPosition(PoolId id, address owner, uint24 binId, bytes32 salt)
        external
        view
        returns (BinPosition.Info memory position);

    /// @notice Returns the next non-empty bin
    /// @dev The next non-empty bin is the bin with a higher (if swapForY is true) or lower (if swapForY is false)
    ///     id that has a non-zero reserve of token X or Y.
    /// @param swapForY Whether the swap is for token Y (true) or token X (false)
    /// @param id The id of the bin
    /// @return nextId The id of the next non-empty bin
    function getNextNonEmptyBin(PoolId id, bool swapForY, uint24 binId) external view returns (uint24 nextId);

    /// @notice Initialize a new pool
    function initialize(PoolKey memory key, uint24 activeId, uint24 protocolFee) external;

    /// @notice Add liquidity to a pool
    /// @return delta BalanceDelta, will be negative indicating how much total amt0 and amt1 liquidity added
    /// @return mintArray Liquidity added in which ids, how much amt0, amt1 and how much liquidity added
    function mint(PoolKey memory key, IMartabakPoolManager.MintParams calldata params)
        external
        returns (BalanceDelta delta, MartabakPool.MintArrays memory mintArray);

    /// @notice Remove liquidity from a pool
    /// @return delta BalanceDelta, will be positive indicating how much total amt0 and amt1 liquidity removed
    function burn(PoolKey memory key, IMartabakPoolManager.BurnParams memory params)
        external
        returns (BalanceDelta delta);

    /// @notice Donate the given currency amounts to the pool with the given pool key.
    /// @return delta Negative amt means the caller owes the vault, while positive amt means the vault owes the caller
    /// @return binId The donated bin id, which is the current active bin id. if no-op happen, binId will be 0
    function donate(PoolKey memory key, uint128 amount0, uint128 amount1)
        external
        returns (BalanceDelta delta, uint24 binId);
}
