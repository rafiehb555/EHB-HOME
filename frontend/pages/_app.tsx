import React from 'react';
import type { AppProps } from 'next/app';
import { QueryClient, QueryClientProvider } from 'react-query';
import { Toaster } from 'react-hot-toast';
import { AuthProvider } from '@/hooks/useAuth';
import ErrorBoundary from '@/components/ErrorBoundary';
import '@/styles/globals.css';

// Create a client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
});

export default function App({ Component, pageProps }: AppProps) {
  // Handle external script errors (like MetaMask)
  React.useEffect(() => {
    const handleError = (event: ErrorEvent) => {
      // Ignore MetaMask and other extension errors
      if (event.message.includes('MetaMask') ||
          event.message.includes('Failed to connect') ||
          event.message.includes('Metamask') ||
          event.message.includes('Netallask') ||
          event.filename?.includes('chrome-extension') ||
          event.filename?.includes('moz-extension') ||
          event.filename?.includes('inpage.js')) {
        event.preventDefault();
        return false;
      }
    };

    const handleUnhandledRejection = (event: PromiseRejectionEvent) => {
      // Handle MetaMask connection rejections
      if (event.reason?.message?.includes('MetaMask') ||
          event.reason?.message?.includes('Failed to connect') ||
          event.reason?.message?.includes('Metamask')) {
        event.preventDefault();
        return false;
      }
    };

    // Add error listeners
    window.addEventListener('error', handleError);
    window.addEventListener('unhandledrejection', handleUnhandledRejection);

    // Cleanup
    return () => {
      window.removeEventListener('error', handleError);
      window.removeEventListener('unhandledrejection', handleUnhandledRejection);
    };
  }, []);

  return (
    <ErrorBoundary>
      <QueryClientProvider client={queryClient}>
        <AuthProvider>
          <Component {...pageProps} />
          <Toaster
            position="top-right"
            toastOptions={{
              duration: 4000,
              style: {
                background: '#363636',
                color: '#fff',
              },
              success: {
                duration: 3000,
                iconTheme: {
                  primary: '#10B981',
                  secondary: '#fff',
                },
              },
              error: {
                duration: 5000,
                iconTheme: {
                  primary: '#EF4444',
                  secondary: '#fff',
                },
              },
            }}
          />
        </AuthProvider>
      </QueryClientProvider>
    </ErrorBoundary>
  );
}
