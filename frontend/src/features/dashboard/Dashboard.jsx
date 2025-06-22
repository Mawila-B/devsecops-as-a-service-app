import React from 'react';
import ScanStats from './ScanStats';
import RecentScans from './RecentScans';
import QuickActions from './QuickActions';

const Dashboard = () => {
  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h1>Security Dashboard</h1>
        <p>Monitor and manage your security scans</p>
      </div>
      
      <div className="dashboard-grid">
        <div className="dashboard-main">
          <ScanStats />
          <RecentScans />
        </div>
        
        <div className="dashboard-sidebar">
          <QuickActions />
        </div>
      </div>
    </div>
  );
};

export default Dashboard;