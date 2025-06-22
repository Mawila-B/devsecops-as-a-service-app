import React, { useState } from 'react';
import PaymentSelector from '@/components/payment/PaymentSelector';
import { useNotification } from '@/contexts/NotificationContext';
import api from '@/services/api';

const SubscriptionCard = ({ subscription }) => {
  const [showPayment, setShowPayment] = useState(false);
  const [selectedTier, setSelectedTier] = useState(null);
  const { showNotification } = useNotification();
  
  const tiers = [
    { id: 'free', name: 'Free', price: 0, scans: 10 },
    { id: 'pro', name: 'Pro', price: 99, scans: 500 },
    { id: 'enterprise', name: 'Enterprise', price: 499, scans: 'Unlimited' },
  ];
  
  const handleUpgrade = (tier) => {
    setSelectedTier(tier);
    setShowPayment(true);
  };
  
  const handlePaymentSuccess = (paymentId) => {
    // Call backend to confirm subscription upgrade
    api.post('/subscription/upgrade', { tier: selectedTier.id })
      .then(() => {
        showNotification('success', `Upgraded to ${selectedTier.name} tier!`);
        setShowPayment(false);
      })
      .catch(error => {
        showNotification('error', 'Subscription upgrade failed');
      });
  };

  return (
    <div className="bg-white rounded-xl shadow-md p-6">
      <h2 className="text-xl font-semibold mb-4">Your Subscription</h2>
      
      {subscription ? (
        <div className="mb-4">
          <p>
            <span className="font-semibold">Current Plan:</span> {subscription.tier}
          </p>
          <p>
            <span className="font-semibold">Scans Remaining:</span> {subscription.scans_remaining}
          </p>
          <p>
            <span className="font-semibold">Renewal Date:</span> {subscription.renewal_date}
          </p>
        </div>
      ) : (
        <p>Loading subscription details...</p>
      )}
      
      {!showPayment ? (
        <div>
          <h3 className="font-semibold mb-2">Upgrade Plan</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {tiers.map(tier => (
              <div 
                key={tier.id}
                className={`border rounded-lg p-4 ${
                  subscription?.tier === tier.id ? 'border-blue-500 border-2' : ''
                }`}
              >
                <h4 className="font-semibold">{tier.name}</h4>
                <p className="text-2xl my-2">
                  ${tier.price}{tier.price > 0 ? '/mo' : ''}
                </p>
                <p>{tier.scans} scans/month</p>
                <button
                  onClick={() => handleUpgrade(tier)}
                  disabled={subscription?.tier === tier.id}
                  className={`mt-3 w-full py-1 rounded ${
                    subscription?.tier === tier.id 
                      ? 'bg-gray-300 cursor-not-allowed' 
                      : 'bg-blue-500 hover:bg-blue-600 text-white'
                  }`}
                >
                  {subscription?.tier === tier.id ? 'Current Plan' : 'Upgrade'}
                </button>
              </div>
            ))}
          </div>
        </div>
      ) : (
        <div>
          <h3 className="font-semibold mb-4">Payment for {selectedTier.name} Plan</h3>
          <PaymentSelector 
            amount={selectedTier.price} 
            currency="USD"
            onSuccess={handlePaymentSuccess}
          />
          <button
            onClick={() => setShowPayment(false)}
            className="mt-3 text-blue-500 hover:underline"
          >
            Cancel Payment
          </button>
        </div>
      )}
    </div>
  );
};

export default SubscriptionCard;