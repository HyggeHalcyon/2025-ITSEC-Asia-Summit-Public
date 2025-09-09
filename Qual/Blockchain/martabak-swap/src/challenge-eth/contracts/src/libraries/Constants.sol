// SPDX-License-Identifier: GPL-2.0-or-later
// KueBandungPool
pragma solidity ^0.8.24;

/// @notice Set of constants for MartabakPool
library Constants {
    uint8 internal constant SCALE_OFFSET = 128;
    uint256 internal constant SCALE = 1 << SCALE_OFFSET;

    uint256 internal constant PRECISION = 1e18;
    uint256 internal constant SQUARED_PRECISION = PRECISION * PRECISION;

    uint256 internal constant BASIS_POINT_MAX = 10_000;
}
