import React, { useState, useEffect } from 'react';
import Web3 from 'web3';
import api from '@/services/api';
import { useNotification } from '@/contexts/NotificationContext';

const MetaMaskPayment = ({ amountUsd, onSuccess }) => {
  const [paymentInfo, setPaymentInfo] = useState(null);
  const [web3, setWeb3] = useState(null);
  const [account, setAccount] = useState('');
  const [isPaying, setIsPaying] = useState(false);
  const { showNotification } = useNotification();

  // Initialize Web3 and get account
  useEffect(() => {
    const initWeb3 = async () => {
      if (window.ethereum) {
        try {
          await window.ethereum.request({ method: 'eth_requestAccounts' });
          const web3Instance = new Web3(window.ethereum);
          setWeb3(web3Instance);
          
          const accounts = await web3Instance.eth.getAccounts();
          setAccount(accounts[0]);
        } catch (error) {
          showNotification('error', 'Failed to connect MetaMask');
        }
      } else {
        showNotification('error', 'MetaMask not detected');
      }
    };
    
    initWeb3();
  }, []);

  // Create payment request when amount changes
  useEffect(() => {
    if (amountUsd > 0) {
      api.post('/crypto/create-payment', { amount_usd: amountUsd })
        .then(response => {
          setPaymentInfo(response.data);
        })
        .catch(error => {
          showNotification('error', 'Failed to create payment request');
        });
    }
  }, [amountUsd]);

  const handlePayment = async () => {
    if (!web3 || !paymentInfo) return;
    
    setIsPaying(true);
    
    try {
      const amountWei = web3.utils.toWei(paymentInfo.amount_eth.toString(), 'ether');
      
      // Send transaction
      const tx = await web3.eth.sendTransaction({
        from: account,
        to: paymentInfo.wallet_address,
        value: amountWei
      });
      
      // Verify payment
      await api.post('/crypto/verify-payment', {
        payment_id: paymentInfo.payment_id,
        tx_hash: tx.transactionHash
      });
      
      onSuccess(tx.transactionHash);
      showNotification('success', 'Payment successful!');
    } catch (error) {
      console.error('Payment failed:', error);
      showNotification('error', `Payment failed: ${error.message}`);
    } finally {
      setIsPaying(false);
    }
  };

  return (
    <div className="border rounded-lg p-4 bg-gray-50">
      <div className="flex items-center mb-4">
        <img 
          src="/metamask-logo.svg" 
          alt="MetaMask" 
          className="w-8 h-8 mr-2"
        />
        <h3 className="text-lg font-semibold">Pay with MetaMask</h3>
      </div>
      
      {account ? (
        <div>
          <p className="text-sm mb-2">
            Connected: <span className="font-mono">{account.slice(0,6)}...{account.slice(-4)}</span>
          </p>
          
          {paymentInfo && (
            <div className="mb-4">
              <p className="text-sm">
                Amount: <span className="font-semibold">{paymentInfo.amount_eth} ETH</span>
                <span className="text-gray-600 ml-2">
                  (≈ ${paymentInfo.amount_usd} @ ${paymentInfo.eth_usd_price}/ETH)
                </span>
              </p>
              <p className="text-xs text-gray-600 mt-1">
                Send to: <span className="font-mono">{paymentInfo.wallet_address}</span>
              </p>
            </div>
          )}
          
          <button
            onClick={handlePayment}
            disabled={!paymentInfo || isPaying}
            className={`w-full py-2 px-4 rounded-md ${
              !paymentInfo || isPaying 
                ? 'bg-gray-300 cursor-not-allowed' 
                : 'bg-orange-500 hover:bg-orange-600 text-white'
            }`}
          >
            {isPaying ? 'Processing Payment...' : 'Pay with MetaMask'}
          </button>
        </div>
      ) : (
        <div>
          <p className="text-red-500 mb-2">MetaMask not connected</p>
          <button
            onClick={() => window.location.reload()}
            className="bg-blue-500 text-white py-2 px-4 rounded-md hover:bg-blue-600"
          >
            Connect Wallet
          </button>
        </div>
      )}
      
      <p className="text-xs text-gray-500 mt-3">
        Transactions are verified on the Ethereum blockchain. This may take 1-2 minutes.
      </p>
    </div>
  );
};

export default MetaMaskPayment;