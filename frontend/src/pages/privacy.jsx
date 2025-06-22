import React from 'react';
import Layout from '@/components/Layout';

export default function PrivacyPolicy() {
  return (
    <Layout>
      <div className="max-w-3xl mx-auto py-8 px-4">
        <h1 className="text-3xl font-bold mb-6">Privacy Policy</h1>
        
        <section className="mb-6">
          <h2 className="text-xl font-semibold mb-2">1. Data Collection</h2>
          <p className="mb-4">
            We collect only essential data required to provide our security scanning services:
          </p>
          <ul className="list-disc pl-6 mb-4">
            <li>Email address for account creation</li>
            <li>Scan targets provided by users</li>
            <li>Scan results and reports</li>
            <li>Payment information (processed by secure third parties)</li>
          </ul>
        </section>
        
        <section className="mb-6">
          <h2 className="text-xl font-semibold mb-2">2. Data Usage</h2>
          <p>
            Your data is used exclusively to:
          </p>
          <ul className="list-disc pl-6 mb-4">
            <li>Perform security scans as requested</li>
            <li>Generate and deliver reports</li>
            <li>Process payments for services</li>
            <li>Improve our service quality</li>
          </ul>
        </section>
        
        <section className="mb-6">
          <h2 className="text-xl font-semibold mb-2">3. Data Retention</h2>
          <p className="mb-4">
            Scan results are retained for 30 days unless otherwise specified in enterprise agreements.
            Account information is retained until account deletion is requested.
          </p>
        </section>
        
        <section className="mb-6">
          <h2 className="text-xl font-semibold mb-2">4. GDPR Compliance</h2>
          <p className="mb-4">
            We comply with the General Data Protection Regulation (GDPR):
          </p>
          <ul className="list-disc pl-6 mb-4">
            <li>Right to access your personal data</li>
            <li>Right to rectification of inaccurate data</li>
            <li>Right to erasure ("right to be forgotten")</li>
            <li>Right to data portability</li>
          </ul>
          <p>
            To exercise these rights, contact us at privacy@yourdevsecops.com.
          </p>
        </section>
        
        <section>
          <h2 className="text-xl font-semibold mb-2">5. Cookie Policy</h2>
          <p className="mb-4">
            We use cookies only for essential functionality and service improvement. 
            We do not use tracking cookies without explicit consent.
          </p>
        </section>
      </div>
    </Layout>
  );
}