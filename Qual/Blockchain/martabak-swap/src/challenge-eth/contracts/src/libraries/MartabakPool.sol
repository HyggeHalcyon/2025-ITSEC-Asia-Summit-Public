// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {BalanceDelta, toBalanceDelta} from "../types/BalanceDelta.sol";
import {LiquidityConfigurations} from "./math/LiquidityConfigurations.sol";
import {PackedUint128Math} from "./math/PackedUint128Math.sol";
import {Uint256x256Math} from "./math/Uint256x256Math.sol";
import {TreeMath} from "./math/TreeMath.sol";
import {PriceHelper} from "./PriceHelper.sol";
import {BinHelper} from "./BinHelper.sol";
import {BinPosition} from "./BinPosition.sol";
import {SafeCast} from "./math/SafeCast.sol";
import {Constants} from "./Constants.sol";
import {FeeHelper} from "./FeeHelper.sol";
import {LPFeeLibrary} from "./LPFeeLibrary.sol";

library MartabakPool {
    using BinHelper for bytes32;
    using LiquidityConfigurations for bytes32;
    using PackedUint128Math for bytes32;
    using PackedUint128Math for uint128;
    using PriceHelper for uint24;
    using Uint256x256Math for uint256;
    using BinPosition for mapping(bytes32 => BinPosition.Info);
    using BinPosition for BinPosition.Info;
    using TreeMath for bytes32;
    using SafeCast for uint256;
    using SafeCast for uint128;
    using FeeHelper for uint128;
    using MartabakPool for State;
    using LPFeeLibrary for uint24;

    error PoolNotInitialized();
    error PoolAlreadyInitialized();
    error MartabakPool__EmptyLiquidityConfigs();
    error MartabakPool__ZeroShares(uint24 id);
    error MartabakPool__InvalidBurnInput();
    error MartabakPool__BurnZeroAmount(uint24 id);
    error MartabakPool__ZeroAmountsOut(uint24 id);
    error MartabakPool__OutOfLiquidity();
    error MartabakPool__NoLiquidityToReceiveFees();
    error MartabakPool__InsufficientAmountUnSpecified();

    struct Slot0 {
        uint24 activeId;
        uint24 protocolFee;
        uint24 lpFee;
    }

    struct State {
        Slot0 slot0;
        mapping(uint256 binId => bytes32 reserve) reserveOfBin;
        mapping(uint256 binId => uint256 share) shareOfBin;
        mapping(bytes32 => BinPosition.Info) positions;
        bytes32 level0;
        mapping(bytes32 => bytes32) level1;
        mapping(bytes32 => bytes32) level2;
    }

    struct MintParams {
        address to; // nft minted to
        bytes32[] liquidityConfigs;
        bytes32 amountIn;
        uint16 binStep;
        bytes32 salt;
    }

    struct MintArrays {
        uint256[] ids;
        bytes32[] amounts;
        uint256[] liquidityMinted;
    }

    function getBin(State storage self, uint16 binStep, uint24 id)
        internal
        view
        returns (uint128 binReserveX, uint128 binReserveY, uint256 binLiquidity)
    {
        bytes32 binReserves = self.reserveOfBin[id];

        (binReserveX, binReserveY) = binReserves.decode();
        binLiquidity = binReserves.getLiquidity(id.getPriceFromId(binStep));
    }

    function getNextNonEmptyBin(State storage self, bool swapForY, uint24 id) internal view returns (uint24) {
        return swapForY
            ? TreeMath.findFirstRight(self.level0, self.level1, self.level2, id)
            : TreeMath.findFirstLeft(self.level0, self.level1, self.level2, id);
    }

    function initialize(State storage self, uint24 activeId, uint24 protocolFee, uint24 lpFee) internal {
        if (self.slot0.activeId != 0) revert PoolAlreadyInitialized();
        self.slot0 = Slot0({activeId: activeId, protocolFee: protocolFee, lpFee: lpFee});
    }

    function mint(State storage self, MintParams memory params)
        internal
        returns (BalanceDelta result, bytes32 feeForProtocol, MintArrays memory arrays, bytes32 compositionFee)
    {
        if (params.liquidityConfigs.length == 0) revert ("empty params");

        arrays = MintArrays({
            ids: new uint256[](params.liquidityConfigs.length),
            amounts: new bytes32[](params.liquidityConfigs.length),
            liquidityMinted: new uint256[](params.liquidityConfigs.length)
        });

        (bytes32 amountsLeft, bytes32 fee, bytes32 compoFee) = _mintBins(self, params, arrays);
        feeForProtocol = fee;
        compositionFee = compoFee;

        (uint128 x1, uint128 x2) = params.amountIn.sub(amountsLeft).decode();
        result = toBalanceDelta(-(x1.safeInt128()), -(x2.safeInt128()));
    }

    function _mintBins(State storage self, MintParams memory params, MintArrays memory arrays)
        private
        returns (bytes32 amountsLeft, bytes32 feeForProtocol, bytes32 compositionFee)
    {
        amountsLeft = params.amountIn;

        uint24 id;
        uint256 shares;
        bytes32 amountsIn;
        bytes32 amountsInToBin;
        bytes32 binFeeAmt;
        bytes32 binCompositionFee;
        for (uint256 i; i < params.liquidityConfigs.length;) {
            // fix stack too deep
            {
                bytes32 maxAmountsInToBin;
                (maxAmountsInToBin, id) = params.liquidityConfigs[i].getAmountsAndId(params.amountIn);

                (shares, amountsIn, amountsInToBin, binFeeAmt, binCompositionFee) =
                    _updateBin(self, params, id, maxAmountsInToBin);
            }

            amountsLeft = amountsLeft.sub(amountsIn);
            feeForProtocol = feeForProtocol.add(binFeeAmt);

            arrays.ids[i] = id;
            arrays.amounts[i] = amountsInToBin;
            arrays.liquidityMinted[i] = shares;

            _addShare(self, params.to, id, params.salt, shares);

            compositionFee = compositionFee.add(binCompositionFee);

            unchecked {
                ++i;
            }
        }
    }

    function _addShare(State storage self, address owner, uint24 binId, bytes32 salt, uint256 shares) internal {
        self.positions.get(owner, binId, salt).addShare(shares);
        self.shareOfBin[binId] += shares;
    }

    function _updateBin(State storage self, MintParams memory params, uint24 id, bytes32 maxAmountsInToBin)
        internal
        returns (
            uint256 shares,
            bytes32 amountsIn,
            bytes32 amountsInToBin,
            bytes32 feeForProtocol,
            bytes32 compositionFee
        )
    {
        Slot0 memory slot0Cache = self.slot0;
        uint24 activeId = slot0Cache.activeId;
        bytes32 binReserves = self.reserveOfBin[id];

        uint256 price = id.getPriceFromId(params.binStep);
        uint256 supply = self.shareOfBin[id];
        (shares, amountsIn) = binReserves.getSharesAndEffectiveAmountsIn(maxAmountsInToBin, price, supply);
        amountsInToBin = amountsIn;

        if (id == activeId) {
            bytes32 fees;
            (fees, feeForProtocol) =
                binReserves.getCompositionFees(slot0Cache.protocolFee, slot0Cache.lpFee, amountsIn, supply, shares);
            compositionFee = fees;
            if (fees != 0) {
                {
                    uint256 userLiquidity = amountsIn.sub(fees).getLiquidity(price);
                    uint256 binLiquidity = binReserves.getLiquidity(price);
                    shares = userLiquidity.mulDivRoundDown(supply, binLiquidity);
                }

                if (feeForProtocol != 0) {
                    amountsInToBin = amountsInToBin.sub(feeForProtocol);
                }
            }
        } else {
            amountsIn.verifyAmounts(activeId, id);
        }

        if (shares == 0 || amountsInToBin == 0) revert MartabakPool__ZeroShares(id);
        if (supply == 0) _addBinIdToTree(self, id);

        self.reserveOfBin[id] = binReserves.add(amountsInToBin);
    }

    function _addBinIdToTree(State storage self, uint24 binId) internal {
        (, self.level0) = TreeMath.add(self.level0, self.level1, self.level2, binId);
    }

    struct BurnParams {
        address from;
        uint256[] ids;
        uint256[] amountsToBurn;
        bytes32 salt;
    }

    /// @notice Burn user's share and withdraw tokens form the pool.
    /// @return result the delta of the token balance of the pool
    function burn(State storage self, BurnParams memory params)
        internal
        returns (BalanceDelta result, uint256[] memory ids, bytes32[] memory amounts)
    {
        ids = params.ids;
        uint256[] memory amountsToBurn = params.amountsToBurn;

        if (ids.length == 0 || ids.length != amountsToBurn.length) revert MartabakPool__InvalidBurnInput();

        bytes32 amountsOut;
        amounts = new bytes32[](ids.length);
        for (uint256 i; i < ids.length;) {
            uint24 id = ids[i].safe24();
            uint256 amountToBurn = amountsToBurn[i];

            if (amountToBurn == 0) revert MartabakPool__BurnZeroAmount(id);

            bytes32 binReserves = self.reserveOfBin[id];
            uint256 supply = self.shareOfBin[id];

            _subShare(self, params.from, id, params.salt, amountToBurn);

            bytes32 amountsOutFromBin = binReserves.getAmountOutOfBin(amountToBurn, supply);

            if (amountsOutFromBin == 0) revert MartabakPool__ZeroAmountsOut(id);

            binReserves = binReserves.sub(amountsOutFromBin);

            if (supply == amountToBurn) _removeBinIdToTree(self, id);

            self.reserveOfBin[id] = binReserves;
            amounts[i] = amountsOutFromBin;
            amountsOut = amountsOut.add(amountsOutFromBin);

            unchecked {
                ++i;
            }
        }
        result = toBalanceDelta(amountsOut.decodeX().safeInt128(), amountsOut.decodeY().safeInt128());
    }

    /// @notice Subtract share from user's position and update total share supply of bin
    function _subShare(State storage self, address owner, uint24 binId, bytes32 salt, uint256 shares) internal {
        self.positions.get(owner, binId, salt).subShare(shares);
        self.shareOfBin[binId] -= shares;
    }

    /// @notice remove bin id for a pool
    function _removeBinIdToTree(State storage self, uint24 binId) internal {
        (, self.level0) = TreeMath.remove(self.level0, self.level1, self.level2, binId);
    }

    function donate(State storage self, uint16 binStep, uint128 amount0, uint128 amount1)
        internal
        returns (BalanceDelta result, uint24 activeId)
    {
        activeId = self.slot0.activeId;
        bytes32 amountIn = amount0.encode(amount1);

        bytes32 binReserves = self.reserveOfBin[activeId];
        if (binReserves == 0) revert MartabakPool__NoLiquidityToReceiveFees();

        /// @dev overflow check on total reserves and the resulting liquidity
        uint256 price = activeId.getPriceFromId(binStep);
        binReserves.add(amountIn).getLiquidity(price);

        self.reserveOfBin[activeId] = binReserves.add(amountIn);
        result = toBalanceDelta(-(amount0.safeInt128()), -(amount1.safeInt128()));
    }

    function checkPoolInitialized(State storage self) internal view {
        if (self.slot0.activeId == 0) {
            revert("not initialized");
        }
    }
}
