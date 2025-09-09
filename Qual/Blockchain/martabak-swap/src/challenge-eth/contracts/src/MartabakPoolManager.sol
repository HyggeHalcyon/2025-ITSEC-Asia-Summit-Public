// SPDX-License-Identifier: GPL-2.0-or-later
pragma solidity ^0.8.24;

import {MartabakPool} from "./libraries/MartabakPool.sol";
import {MartabakPoolParametersHelper} from "./libraries/MartabakPoolParametersHelper.sol";
import {ParametersHelper} from "./libraries/math/ParametersHelper.sol";
import {Currency, CurrencyLibrary} from "./types/Currency.sol";
import {IPoolManager} from "./interfaces/IPoolManager.sol";
import {IMartabakPoolManager} from "./interfaces/IMartabakPoolManager.sol";
import {PoolId, PoolIdLibrary} from "./types/PoolId.sol";
import {PoolKey} from "./types/PoolKey.sol";
import {BalanceDelta, BalanceDeltaLibrary} from "./types/BalanceDelta.sol";
import {BinPosition} from "./libraries/BinPosition.sol";
import {LPFeeLibrary} from "./libraries/LPFeeLibrary.sol";
import {PackedUint128Math} from "./libraries/math/PackedUint128Math.sol";
import {IERC20Minimal} from "./interfaces/IERC20Minimal.sol";
import {Ownable} from "./Ownable.sol";

/// @notice Holds the state for all bin pools
contract MartabakPoolManager is IMartabakPoolManager, Ownable {
    using PoolIdLibrary for PoolKey;
    using MartabakPool for *;
    using BinPosition for mapping(bytes32 => BinPosition.Info);
    using MartabakPoolParametersHelper for bytes32;
    using LPFeeLibrary for uint24;
    using PackedUint128Math for bytes32;

    
    uint16 public constant override MIN_BIN_STEP = 1;

    
    uint16 public override MAX_BIN_STEP = 100;

    mapping(PoolId id => MartabakPool.State) public pools;

    mapping(PoolId id => PoolKey) public poolIdToPoolKey;

    mapping(Currency currency => uint256) public protocolFeesAccrued;

    constructor() Ownable(msg.sender) {}

    /// @notice pool manager specified in the pool key must match current contract
    modifier poolManagerMatch(address poolManager) {
        if (address(this) != poolManager) revert PoolManagerMismatch();
        _;
    }

    function _getPool(PoolKey memory key) private view returns (MartabakPool.State storage) {
        return pools[key.toId()];
    }

    
    function getSlot0(PoolId id) external view override returns (uint24 activeId, uint24 protocolFee, uint24 lpFee) {
        MartabakPool.Slot0 memory slot0 = pools[id].slot0;

        return (slot0.activeId, slot0.protocolFee, slot0.lpFee);
    }

    
    function getBin(PoolId id, uint24 binId)
        external
        view
        override
        returns (uint128 binReserveX, uint128 binReserveY, uint256 binLiquidity)
    {
        PoolKey memory key = poolIdToPoolKey[id];
        (binReserveX, binReserveY, binLiquidity) = pools[id].getBin(key.parameters.getBinStep(), binId);
    }

    
    function getPosition(PoolId id, address owner, uint24 binId, bytes32 salt)
        external
        view
        override
        returns (BinPosition.Info memory position)
    {
        return pools[id].positions.get(owner, binId, salt);
    }

    
    function getNextNonEmptyBin(PoolId id, bool swapForY, uint24 binId)
        external
        view
        override
        returns (uint24 nextId)
    {
        nextId = pools[id].getNextNonEmptyBin(swapForY, binId);
    }

    
    // TODO: Only Owner
    function initialize(PoolKey memory key, uint24 activeId, uint24 protocolFee)
        external
        override
        onlyOwner
        poolManagerMatch(address(key.poolManager))
    {
        uint16 binStep = key.parameters.getBinStep();
        if (binStep < MIN_BIN_STEP) revert BinStepTooSmall();
        if (binStep > MAX_BIN_STEP) revert BinStepTooLarge();
        if (key.currency0 >= key.currency1) revert CurrenciesInitializedOutOfOrder();

        uint24 lpFee = key.fee.getInitialLPFee();
        lpFee.validate(LPFeeLibrary.TEN_PERCENT_FEE);

        PoolId id = key.toId();
        pools[id].initialize(activeId, protocolFee, lpFee);

        poolIdToPoolKey[id] = key;
    }

    
    function mint(PoolKey memory key, IMartabakPoolManager.MintParams calldata params)
        external
        override
        returns (BalanceDelta delta, MartabakPool.MintArrays memory mintArray)
    {
        PoolId id = key.toId();
        MartabakPool.State storage pool = pools[id];
        pool.checkPoolInitialized();

        bytes32 feeForProtocol;
        bytes32 compositionFee;
        (delta, feeForProtocol, mintArray, compositionFee) = pool.mint(
            MartabakPool.MintParams({
                to: msg.sender,
                liquidityConfigs: params.liquidityConfigs,
                amountIn: params.amountIn,
                binStep: key.parameters.getBinStep(),
                salt: params.salt
            })
        );

        unchecked {
            if (feeForProtocol > 0) {
                protocolFeesAccrued[key.currency0] += feeForProtocol.decodeX();
                protocolFeesAccrued[key.currency1] += feeForProtocol.decodeY();
            }
        }

        settleDelta(key, delta, msg.sender);
    }

    
    function burn(PoolKey memory key, IMartabakPoolManager.BurnParams memory params)
        external
        override
        returns (BalanceDelta delta)
    {
        PoolId id = key.toId();
        MartabakPool.State storage pool = pools[id];
        pool.checkPoolInitialized();

        uint256[] memory binIds;
        bytes32[] memory amountRemoved;
        (delta, binIds, amountRemoved) = pool.burn(
            MartabakPool.BurnParams({
                from: msg.sender,
                ids: params.ids,
                amountsToBurn: params.amountsToBurn,
                salt: params.salt
            })
        );
        
        settleDelta(key, delta, msg.sender);
    }

    function donate(PoolKey memory key, uint128 amount0, uint128 amount1)
        external
        override
        returns (BalanceDelta delta, uint24 binId)
    {
        PoolId id = key.toId();
        MartabakPool.State storage pool = pools[id];
        pool.checkPoolInitialized();

        (delta, binId) = pool.donate(key.parameters.getBinStep(), amount0, amount1);

        settleDelta(key, delta, msg.sender);
    }

    function settleDelta(PoolKey memory key, BalanceDelta delta, address settler) internal {
        int128 delta0 = delta.amount0();
        int128 delta1 = delta.amount1();
        if (delta0 <= 0) {
            IERC20Minimal(key.currency0.toAddress()).transferFrom(settler, address(this), uint256(uint128(-delta0)));
        } else {
            IERC20Minimal(key.currency0.toAddress()).transfer(settler, uint256(uint128(delta0)));
        }

        if (delta1 <= 0) {
            IERC20Minimal(key.currency1.toAddress()).transferFrom(settler, address(this), uint256(uint128(-delta1)));
        } else {
            IERC20Minimal(key.currency1.toAddress()).transfer(settler, uint256(uint128(delta1)));
        }
    }
}
