// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract CryptoPayment {
    address public owner;
    mapping(string => bool) public processedPayments;
    
    event PaymentReceived(
        string indexed paymentId,
        address indexed from,
        uint256 amount,
        uint256 timestamp
    );
    
    constructor() {
        owner = msg.sender;
    }
    
    function recordPayment(string memory paymentId) external payable {
        require(msg.value > 0, "Payment amount must be greater than 0");
        require(!processedPayments[paymentId], "Payment already processed");
        
        processedPayments[paymentId] = true;
        emit PaymentReceived(paymentId, msg.sender, msg.value, block.timestamp);
    }
    
    function withdraw() external {
        require(msg.sender == owner, "Only owner can withdraw");
        payable(owner).transfer(address(this).balance);
    }
    
    // Fallback function to receive ETH
    receive() external payable {}
}