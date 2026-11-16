// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title ReceiptAnchor — the on-chain half of Foreguild's Verification Receipt.
/// Stores keccak256 digests of issued receipts; verify() is the entire
/// Verification-as-a-Service check: does this digest exist on-chain?
contract ReceiptAnchor {
    mapping(bytes32 => bool) public anchored;
    event Anchored(bytes32 indexed receiptHash, uint256 timestamp);

    function anchor(bytes32 receiptHash) external {
        anchored[receiptHash] = true;
        emit Anchored(receiptHash, block.timestamp);
    }

    function verify(bytes32 receiptHash) external view returns (bool) {
        return anchored[receiptHash];
    }
}
