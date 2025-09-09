//SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {PoolKey} from "../types/PoolKey.sol";
import {PoolId} from "../types/PoolId.sol";
import {Currency} from "../types/Currency.sol";

interface IPoolManager {
    /// @notice Thrown when trying to interact with a non-initialized pool
    error PoolNotInitialized();

    /// @notice PoolKey must have currencies where address(currency0) < address(currency1)
    error CurrenciesInitializedOutOfOrder();

    /// @notice Return PoolKey for a given PoolId
    function poolIdToPoolKey(PoolId id)
        external
        view
        returns (
            Currency currency0,
            Currency currency1,
            IPoolManager poolManager,
            uint24 fee,
            bytes32 parameters
        );
}
