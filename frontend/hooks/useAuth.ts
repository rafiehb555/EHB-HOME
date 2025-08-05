import { useState, useEffect, createContext, useContext, ReactNode } from 'react';
import axios from 'axios';

// Types
interface User {
  id: number;
  email: string;
  username: string;
  first_name?: string;
  last_name?: string;
  phone?: string;
  is_verified: boolean;
  is_active: boolean;
  is_admin: boolean;
  sql_level?: string;
  avatar_url?: string;
  company?: string;
  position?: string;
  email_verified: boolean;
  phone_verified: boolean;
  kyc_verified: boolean;
}

interface AuthTokens {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
}

interface AuthContextType {
  user: User | null;
  tokens: AuthTokens | null;
  login: (email: string, password: string) => Promise<void>;
  register: (userData: RegisterData) => Promise<void>;
  logout: () => void;
  loading: boolean;
  error: string | null;
  clearError: () => void;
}

interface RegisterData {
  email: string;
  username: string;
  password: string;
  first_name?: string;
  last_name?: string;
  phone?: string;
}

// Create context
const AuthContext = createContext<AuthContextType | undefined>(undefined);

// API base URL
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
api.interceptors.request.use((config) => {
  const tokens = getStoredTokens();
  if (tokens?.access_token) {
    config.headers.Authorization = `Bearer ${tokens.access_token}`;
  }
  return config;
});

// Handle token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      const tokens = getStoredTokens();
      if (tokens?.refresh_token) {
        try {
          const response = await axios.post(`${API_BASE_URL}/auth/refresh`, {
            refresh_token: tokens.refresh_token,
          });

          const newTokens = response.data;
          storeTokens(newTokens);

          // Retry original request
          originalRequest.headers.Authorization = `Bearer ${newTokens.access_token}`;
          return api(originalRequest);
        } catch (refreshError) {
          // Refresh failed, logout user
          logout();
          return Promise.reject(refreshError);
        }
      }
    }

    return Promise.reject(error);
  }
);

// Token storage functions
const getStoredTokens = (): AuthTokens | null => {
  if (typeof window === 'undefined') return null;

  const tokens = localStorage.getItem('ehb_tokens');
  return tokens ? JSON.parse(tokens) : null;
};

const storeTokens = (tokens: AuthTokens): void => {
  if (typeof window === 'undefined') return;
  localStorage.setItem('ehb_tokens', JSON.stringify(tokens));
};

const removeTokens = (): void => {
  if (typeof window === 'undefined') return;
  localStorage.removeItem('ehb_tokens');
};

const logout = (): void => {
  removeTokens();
  window.location.href = '/login';
};

// Auth Provider Component
export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);
  const [tokens, setTokens] = useState<AuthTokens | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Initialize auth state
  useEffect(() => {
    const initializeAuth = async () => {
      try {
        const storedTokens = getStoredTokens();
        if (storedTokens) {
          setTokens(storedTokens);

          // Get user info
          const response = await api.get('/auth/me');
          setUser(response.data);
        }
      } catch (error) {
        console.error('Auth initialization failed:', error);
        removeTokens();
      } finally {
        setLoading(false);
      }
    };

    initializeAuth();
  }, []);

  const login = async (email: string, password: string) => {
    try {
      setLoading(true);
      setError(null);

      const response = await api.post('/auth/login', { email, password });
      const authTokens = response.data;

      storeTokens(authTokens);
      setTokens(authTokens);

      // Get user info
      const userResponse = await api.get('/auth/me');
      setUser(userResponse.data);

    } catch (error: any) {
      const errorMessage = error.response?.data?.detail || 'Login failed';
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const register = async (userData: RegisterData) => {
    try {
      setLoading(true);
      setError(null);

      const response = await api.post('/auth/register', userData);
      const authTokens = response.data;

      storeTokens(authTokens);
      setTokens(authTokens);

      // Get user info
      const userResponse = await api.get('/auth/me');
      setUser(userResponse.data);

    } catch (error: any) {
      const errorMessage = error.response?.data?.detail || 'Registration failed';
      setError(errorMessage);
      throw new Error(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const logoutUser = () => {
    setUser(null);
    setTokens(null);
    removeTokens();
  };

  const clearError = () => {
    setError(null);
  };

  const value: AuthContextType = {
    user,
    tokens,
    login,
    register,
    logout: logoutUser,
    loading,
    error,
    clearError,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

// Hook to use auth context
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

// Protected route component
export const ProtectedRoute = ({ children }: { children: ReactNode }) => {
  const { user, loading } = useAuth();

  if (loading) {
    return <div>Loading...</div>;
  }

  if (!user) {
    window.location.href = '/login';
    return null;
  }

  return <>{children}</>;
};

// Admin route component
export const AdminRoute = ({ children }: { children: ReactNode }) => {
  const { user, loading } = useAuth();

  if (loading) {
    return <div>Loading...</div>;
  }

  if (!user) {
    window.location.href = '/login';
    return null;
  }

  if (!user.is_admin) {
    window.location.href = '/dashboard';
    return null;
  }

  return <>{children}</>;
};
