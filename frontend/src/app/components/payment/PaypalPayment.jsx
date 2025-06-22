import React, { useState } from 'react';
import { PayPalButtons } from '@paypal/react-paypal-js';
import { useNotification } from '@/contexts/NotificationContext';
import api from '@/services/api';

const PayPalPayment = ({ amountUsd, currency, onSuccess }) => {
  const { showNotification } = useNotification();
  const [orderID, setOrderID] = useState(false);

  const createOrder = (data, actions) => {
    return actions.order.create({
      purchase_units: [
        {
          amount: {
            value: amountUsd,
            currency_code: currency || 'USD'
          }
        }
      ]
    }).then(orderID => {
      setOrderID(orderID);
      return orderID;
    });
  };

  const onApprove = async (data, actions) => {
    try {
      // Capture the transaction
      const details = await actions.order.capture();
      
      // Verify payment with backend
      await api.post('/payment/verify', {
        provider: 'paypal',
        payment_id: details.id
      });
      
      onSuccess(details.id);
      showNotification('success', 'Payment successful!');
    } catch (error) {
      showNotification('error', 'Payment verification failed');
    }
  };

  return (
    <div className="border rounded-lg p-4 bg-gray-50">
      <h3 className="text-lg font-semibold mb-4">Pay with PayPal</h3>
      
      <PayPalButtons
        createOrder={createOrder}
        onApprove={onApprove}
        onError={(err) => showNotification('error', `PayPal error: ${err.message}`)}
        style={{ layout: "vertical" }}
      />
    </div>
  );
};

export default PayPalPayment;