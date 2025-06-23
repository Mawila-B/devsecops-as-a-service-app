import React, { useState, useEffect } from 'react';
import { useSession } from 'next-auth/react';
import DashboardLayout from '@/components/DashboardLayout';
import ScanForm from '@/components/ScanForm';
import ScanList from '@/components/ScanList';
import SubscriptionCard from '@/components/SubscriptionCard';
import RiskChart from '@/components/RiskChart';
import api from '@/services/api';

export default function Dashboard() {
  const { data: session } = useSession();
  const [scans, setScans] = useState([]);
  const [subscription, setSubscription] = useState(null);
  const [stats, setStats] = useState(null);

  useEffect(() => {
    if (session) {
      // Load user scans
      api.get('/scans')
        .then(res => setScans(res.data))
        .catch(console.error);
      
      // Load subscription
      api.get('/subscription')
        .then(res => setSubscription(res.data))
        .catch(console.error);
      
      // Load stats
      api.get('/stats')
        .then(res => setStats(res.data))
        .catch(console.error);
    }
  }, [session]);

  const handleNewScan = (scanData) => {
    api.post('/scans', scanData)
      .then(res => {
        setScans([res.data, ...scans]);
      })
      .catch(console.error);
  };

  return (
    <DashboardLayout>
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <div className="bg-white rounded-xl shadow-md p-6 mb-6">
            <h1 className="text-2xl font-bold mb-4">Security Dashboard</h1>
            <ScanForm onSubmit={handleNewScan} />
          </div>
          
          <div className="bg-white rounded-xl shadow-md p-6">
            <h2 className="text-xl font-semibold mb-4">Recent Scans</h2>
            <ScanList scans={scans} />
          </div>
        </div>
        
        <div className="space-y-6">
          <SubscriptionCard subscription={subscription} />
          
          {stats && (
            <div className="bg-white rounded-xl shadow-md p-6">
              <h2 className="text-xl font-semibold mb-4">Risk Overview</h2>
              <RiskChart stats={stats} />
              <div className="mt-4">
                <div className="flex justify-between">
                  <span>Critical: {stats.critical_issues}</span>
                  <span>High: {stats.high_issues}</span>
                  <span>Medium: {stats.medium_issues}</span>
                </div>
              </div>
            </div>
          )}
          
          <div className="bg-white rounded-xl shadow-md p-6">
            <h2 className="text-xl font-semibold mb-4">Quick Actions</h2>
            <div className="space-y-3">
              <button className="w-full bg-blue-600 text-white py-2 rounded-lg">
                Schedule Recurring Scan
              </button>
              <button className="w-full bg-green-600 text-white py-2 rounded-lg">
                Generate Compliance Report
              </button>
              <button className="w-full bg-purple-600 text-white py-2 rounded-lg">
                Invite Team Members
              </button>
            </div>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}