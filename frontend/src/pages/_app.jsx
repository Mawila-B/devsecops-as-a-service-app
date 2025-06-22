import React, { useEffect, useState } from 'react';
import CookieConsent from 'react-cookie-consent';
import Head from 'next/head';
import { useRouter } from 'next/router';
import Layout from '@/components/Layout';
import { useNotification } from '@/contexts/NotificationContext';
import '@/styles/globals.css';

export default function App({ Component, pageProps }) {
  const [consentGiven, setConsentGiven] = useState(false);
  const { showNotification } = useNotification();
  const router = useRouter();

  useEffect(() => {
    // Check for existing consent
    const hasConsent = localStorage.getItem('cookieConsent') === 'true';
    setConsentGiven(hasConsent);
    
    // Load analytics only if consent given
    if (hasConsent && process.env.NEXT_PUBLIC_GA_TRACKING_ID) {
      import('react-ga').then(({ default: ReactGA }) => {
        ReactGA.initialize(process.env.NEXT_PUBLIC_GA_TRACKING_ID);
        ReactGA.pageview(router.pathname);
        
        // Track route changes
        router.events.on('routeChangeComplete', (url) => {
          ReactGA.pageview(url);
        });
      });
    }
  }, [router]);

  const handleConsent = (accepted) => {
    if (accepted) {
      localStorage.setItem('cookieConsent', 'true');
      setConsentGiven(true);
      showNotification('info', 'Cookies enabled for better experience');
    } else {
      localStorage.setItem('cookieConsent', 'false');
      showNotification('info', 'Cookies disabled - limited functionality');
    }
  };

  return (
    <>
      <Head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <meta name="description" content="Enterprise DevSecOps Platform" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      
      <Layout>
        <Component {...pageProps} />
      </Layout>
      
      {!consentGiven && (
        <CookieConsent
          location="bottom"
          buttonText="Accept"
          declineButtonText="Decline"
          cookieName="cookieConsent"
          style={{ background: "#2B373B" }}
          buttonStyle={{ background: "#4CAF50", color: "#fff", fontSize: "13px" }}
          declineButtonStyle={{ background: "#f44336", color: "#fff", fontSize: "13px" }}
          expires={365}
          onAccept={() => handleConsent(true)}
          onDecline={() => handleConsent(false)}
          enableDeclineButton
        >
          We use cookies to enhance your experience, analyze traffic, and serve targeted ads.{" "}
          <a 
            href="/privacy" 
            style={{ color: "#4CAF50", textDecoration: "underline" }}
          >
            Privacy Policy
          </a>
        </CookieConsent>
      )}
    </>
  );
}