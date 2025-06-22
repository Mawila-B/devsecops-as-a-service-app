import React, { useState } from 'react';
import { usePaystackPayment } from 'react-paystack';
import { useNotification } from '@/contexts/NotificationContext';
import api from '@/services/api';

const PaystackPayment = ({ amountUsd, currency, onSuccess }) => {
  const [email, setEmail] = useState('');
  const { showNotification } = useNotification();
  
  const config = {
    reference: (new Date()).getTime().toString(),
    email: email,
    amount: amountUsd * 100, // Paystack expects amount in kobo
    publicKey: process.env.NEXT_PUBLIC_PAYSTACK_PUBLIC_KEY,
    currency: currency || 'USD',
  };

  const initializePayment = usePaystackPayment(config);
  
  const onSuccessHandler = async (reference) => {
    try {
      // Verify payment with backend
      await api.post('/payment/verify', {
        provider: 'paystack',
        payment_id: reference.reference
      });
      
      onSuccess(reference.reference);
      showNotification('success', 'Payment successful!');
    } catch (error) {
      showNotification('error', 'Payment verification failed');
    }
  };

  const onClose = () => {
    showNotification('info', 'Payment cancelled');
  };

  return (
    <div className="border rounded-lg p-4 bg-gray-50">
      <h3 className="text-lg font-semibold mb-4">Pay with Paystack</h3>
      
      <div className="mb-4">
        <label className="block text-sm mb-1">Email</label>
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="w-full p-2 border rounded"
          placeholder="your@email.com"
          required
        />
      </div>
      
      <button
        onClick={() => initializePayment(onSuccessHandler, onClose)}
        disabled={!email}
        className={`w-full py-2 px-4 rounded-md ${
          !email 
            ? 'bg-gray-300 cursor-not-allowed' 
            : 'bg-green-600 hover:bg-green-700 text-white'
        }`}
      >
        Pay ${amountUsd} with Paystack
      </button>
    </div>
  );
};

export default PaystackPayment;