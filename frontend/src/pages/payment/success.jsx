import React, { useEffect } from 'react';
import { useRouter } from 'next/router';
import { CheckCircleIcon } from '@heroicons/react/24/solid';
import Layout from '@/components/Layout';

export default function PaymentSuccess() {
  const router = useRouter();
  const { txHash, amount, currency } = router.query;
  
  return (
    <Layout>
      <div className="max-w-3xl mx-auto py-16 px-4 text-center">
        <CheckCircleIcon className="h-24 w-24 text-green-500 mx-auto" />
        <h1 className="text-3xl font-bold mt-4">Payment Successful!</h1>
        
        <div className="mt-8 bg-gray-50 rounded-lg p-6 text-left max-w-md mx-auto">
          <h2 className="text-xl font-semibold mb-4">Payment Details</h2>
          
          <div className="space-y-3">
            <div className="flex justify-between">
              <span className="text-gray-600">Amount:</span>
              <span className="font-medium">{amount} {currency}</span>
            </div>
            
            {txHash && (
              <div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Transaction:</span>
                  <span className="font-mono text-sm">
                    {txHash.slice(0,6)}...{txHash.slice(-4)}
                  </span>
                </div>
                <a 
                  href={`https://etherscan.io/tx/${txHash}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-500 text-sm hover:underline"
                >
                  View on Etherscan
                </a>
              </div>
            )}
          </div>
        </div>
        
        <div className="mt-10">
          <button
            onClick={() => router.push('/dashboard')}
            className="bg-blue-600 text-white py-2 px-6 rounded-md hover:bg-blue-700"
          >
            Go to Dashboard
          </button>
        </div>
      </div>
    </Layout>
  );
}