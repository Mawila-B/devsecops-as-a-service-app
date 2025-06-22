import React, { useState } from 'react';
import StripePayment from './StripePayment';
import PaystackPayment from './PaystackPayment';
import PayPalPayment from './PayPalPayment';
import MetaMaskPayment from './MetaMaskPayment';
import { Tab } from '@headlessui/react';

function classNames(...classes) {
  return classes.filter(Boolean).join(' ');
}

const PaymentSelector = ({ amount, currency, onSuccess }) => {
  const [paymentMethods] = useState([
    { id: 'stripe', name: 'Credit Card', component: StripePayment },
    { id: 'paystack', name: 'Paystack', component: PaystackPayment },
    { id: 'paypal', name: 'PayPal', component: PayPalPayment },
    { id: 'metamask', name: 'Crypto (MetaMask)', component: MetaMaskPayment },
  ]);

  return (
    <div className="w-full max-w-md">
      <Tab.Group>
        <Tab.List className="flex space-x-1 rounded-xl bg-blue-100 p-1">
          {paymentMethods.map((method) => (
            <Tab
              key={method.id}
              className={({ selected }) =>
                classNames(
                  'w-full rounded-lg py-2 text-sm font-medium leading-5',
                  'ring-white ring-opacity-60 ring-offset-2 ring-offset-blue-400 focus:outline-none focus:ring-2',
                  selected
                    ? 'bg-white shadow text-blue-700'
                    : 'text-blue-500 hover:bg-white/[0.12] hover:text-blue-700'
                )
              }
            >
              {method.name}
            </Tab>
          ))}
        </Tab.List>
        <Tab.Panels className="mt-2">
          {paymentMethods.map((method) => (
            <Tab.Panel
              key={method.id}
              className={classNames(
                'rounded-xl bg-white p-3',
                'ring-white ring-opacity-60 ring-offset-2 ring-offset-blue-400 focus:outline-none focus:ring-2'
              )}
            >
              <method.component 
                amountUsd={amount} 
                currency={currency}
                onSuccess={onSuccess}
              />
            </Tab.Panel>
          ))}
        </Tab.Panels>
      </Tab.Group>
    </div>
  );
};

export default PaymentSelector;