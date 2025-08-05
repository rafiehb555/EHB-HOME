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
          event.message.includes('ethereum') ||
          event.message.includes('web3') ||
          event.message.includes('blockchain') ||
          event.filename?.includes('chrome-extension') ||
          event.filename?.includes('moz-extension') ||
          event.filename?.includes('inpage.js') ||
          event.filename?.includes('content-script') ||
          event.filename?.includes('background-script')) {
        event.preventDefault();
        event.stopPropagation();
        return false;
      }
    };

    const handleUnhandledRejection = (event: PromiseRejectionEvent) => {
      // Handle MetaMask connection rejections
      if (event.reason?.message?.includes('MetaMask') ||
          event.reason?.message?.includes('Failed to connect') ||
          event.reason?.message?.includes('Metamask') ||
          event.reason?.message?.includes('ethereum') ||
          event.reason?.message?.includes('web3') ||
          event.reason?.message?.includes('blockchain')) {
        event.preventDefault();
        event.stopPropagation();
        return false;
      }
    };

    // Suppress console errors for MetaMask
    const originalConsoleError = console.error;
    console.error = (...args) => {
      const message = args.join(' ');
      if (message.includes('MetaMask') ||
          message.includes('Failed to connect') ||
          message.includes('Metamask') ||
          message.includes('ethereum') ||
          message.includes('web3') ||
          message.includes('blockchain') ||
          message.includes('chrome-extension')) {
        return; // Don't log MetaMask errors
      }
      originalConsoleError.apply(console, args);
    };

    // Suppress unhandled runtime errors for MetaMask
    const originalOnError = window.onerror;
    window.onerror = (message, source, lineno, colno, error) => {
      const messageStr = String(message);
      if (messageStr.includes('MetaMask') ||
          messageStr.includes('Failed to connect') ||
          messageStr.includes('Metamask') ||
          messageStr.includes('ethereum') ||
          messageStr.includes('web3') ||
          messageStr.includes('blockchain') ||
          source?.includes('chrome-extension')) {
        return true; // Prevent error from showing
      }
      if (originalOnError) {
        return originalOnError(message, source, lineno, colno, error);
      }
      return false;
    };

    // Add error listeners
    window.addEventListener('error', handleError, true);
    window.addEventListener('unhandledrejection', handleUnhandledRejection);

    // Cleanup
    return () => {
      window.removeEventListener('error', handleError, true);
      window.removeEventListener('unhandledrejection', handleUnhandledRejection);
      console.error = originalConsoleError;
      window.onerror = originalOnError;
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
