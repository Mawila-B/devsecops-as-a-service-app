import React, { useState } from 'react';
import { useNotification } from '../../contexts/NotificationContext';

const ScanForm = () => {
  const [target, setTarget] = useState('');
  const [scanType, setScanType] = useState('web');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const { showNotification } = useNotification();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    
    try {
      const response = await fetch('/api/scans', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ target, scanType })
      });
      
      if (!response.ok) throw new Error('Scan failed to start');
      
      const { scan_id } = await response.json();
      showNotification('success', `Scan started: ${scan_id}`);
      // Redirect to results page
      window.location.href = `/scans/${scan_id}`;
      
    } catch (error) {
      showNotification('error', error.message);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="scan-form">
      <div className="form-group">
        <label>Target URL/Repository</label>
        <input 
          type="text" 
          value={target} 
          onChange={(e) => setTarget(e.target.value)} 
          placeholder="https://example.com or git@repo.com"
          required
        />
      </div>
      
      <div className="form-group">
        <label>Scan Type</label>
        <select value={scanType} onChange={(e) => setScanType(e.target.value)}>
          <option value="web">Web Application</option>
          <option value="infra">Infrastructure</option>
          <option value="container">Container</option>
          <option value="full">Full Scan</option>
        </select>
      </div>
      
      <button 
        type="submit" 
        disabled={isSubmitting}
        className="primary-button"
      >
        {isSubmitting ? 'Starting Scan...' : 'Start Security Scan'}
      </button>
    </form>
  );
};

export default ScanForm;