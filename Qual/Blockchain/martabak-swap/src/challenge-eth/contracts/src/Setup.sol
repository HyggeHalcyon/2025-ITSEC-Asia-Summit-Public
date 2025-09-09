// SPDX-License-Identifier: GPL-2.0-or-later
pragma solidity ^0.8.24;

import {MartabakPoolManager} from "./MartabakPoolManager.sol";
import {PoolKey} from "./types/PoolKey.sol";
import {Currency} from "./types/Currency.sol";
import {PoolId} from "./types/PoolId.sol";
import {MockERC20} from ".//MockERC20.sol";
import {IPoolManager} from "./interfaces/IPoolManager.sol";
import {IMartabakPoolManager} from "./interfaces/IMartabakPoolManager.sol";
import {LiquidityConfigurations} from "./libraries/math/LiquidityConfigurations.sol";
import {PackedUint128Math} from "./libraries/math/PackedUint128Math.sol";
import {BinHelper} from "./libraries/BinHelper.sol";
import {MartabakPoolParametersHelper} from "./libraries/MartabakPoolParametersHelper.sol";

contract Setup {
    using MartabakPoolParametersHelper for bytes32;

    MartabakPoolManager public immutable poolManager;
    PoolKey public key;

    Currency public currency0;
    Currency public currency1;

    uint24 public constant POOL_FEE = 3000; // 0.3% fee
    uint24 public constant ACTIVE_ID = 2**23;

    bool public mintTokenForUserExecuted;
    bool public mintPoolExecuted;

    bytes32 poolParam;
    address player;

    MockERC20 public token0;
    MockERC20 public token1;

    constructor() {
        poolManager = new MartabakPoolManager();
        MockERC20 eggMartabak = new MockERC20("EggMartabak", "EGG", 18);
        MockERC20 sweetMartabak = new MockERC20("SweetMartabak", "SWEET", 18);
        (token0, token1) = address(eggMartabak) < address(sweetMartabak) 
            ? (eggMartabak, sweetMartabak) 
            : (sweetMartabak, eggMartabak);
        currency0 = Currency.wrap(address(token0));
        currency1 = Currency.wrap(address(token1));
        key = PoolKey({
            currency0: currency0,
            currency1: currency1,
            fee: POOL_FEE,
            parameters: poolParam.setBinStep(10),
            poolManager: IPoolManager(address(poolManager))
        });
        poolManager.initialize(key, ACTIVE_ID, 0);
        token0.mint(address(this), 1000);
        token1.mint(address(this), 1000);
    }

    function mintPool() external {
        require(!mintPoolExecuted, "Mint can only be called once");
        mintPoolExecuted = true;
        token0.approve(address(poolManager), type(uint256).max);
        token1.approve(address(poolManager), type(uint256).max);
        bytes32[] memory liquidityConfigs = new bytes32[](1);
        uint128 amount = 1000;
        liquidityConfigs[0] = LiquidityConfigurations.encodeParams(1e18, 1e18, ACTIVE_ID);
        IMartabakPoolManager.MintParams memory mintParams = IMartabakPoolManager.MintParams({
            liquidityConfigs: liquidityConfigs,
            amountIn: PackedUint128Math.encode(amount, amount),
            salt: 0
        });

        poolManager.mint(key, mintParams);
    }

    function mint() external {
        require(!mintTokenForUserExecuted, "Mint can only be called once");
        mintTokenForUserExecuted = true;
        player = msg.sender;

        uint256 mintAmount = 1000;
        token0.mint(msg.sender, mintAmount);
        token1.mint(msg.sender, mintAmount);
    }

    function isSolved() external view returns (bool) {
        return token0.balanceOf(player) >= 1500 && token1.balanceOf(player) >= 999;
    }
}