import ProtectedRoute from '@/components/auth/ProtectedRoute';
import { useAuth } from '@/hooks/useAuth';
import {
    AlertCircle,
    Bell,
    CheckCircle,
    Clock,
    LogOut,
    Settings,
    Shield,
    TrendingUp,
    User,
    Wallet
} from 'lucide-react';
import Head from 'next/head';
import { useEffect, useState } from 'react';

interface VerificationStatus {
  pss: 'verified' | 'pending' | 'failed';
  emo: 'verified' | 'pending' | 'failed';
  edr: 'verified' | 'pending' | 'failed';
  jps: 'verified' | 'pending' | 'failed';
}

export default function DashboardPage() {
  const { user, logout } = useAuth();
  const [verificationStatus, setVerificationStatus] = useState<VerificationStatus>({
    pss: 'pending',
    emo: 'pending',
    edr: 'pending',
    jps: 'pending'
  });

  const [stats, setStats] = useState({
    sqlLevel: 1,
    points: 150,
    rank: 'Bronze',
    totalServices: 4,
    completedServices: 1
  });

  useEffect(() => {
    // Fetch user verification status
    const fetchVerificationStatus = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/v1/services/verification-status', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        });
        if (response.ok) {
          const data = await response.json();
          setVerificationStatus(data);
        }
      } catch (error) {
        console.error('Error fetching verification status:', error);
      }
    };

    fetchVerificationStatus();
  }, []);

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'verified':
        return <CheckCircle className="h-5 w-5 text-green-500" />;
      case 'pending':
        return <Clock className="h-5 w-5 text-yellow-500" />;
      case 'failed':
        return <AlertCircle className="h-5 w-5 text-red-500" />;
      default:
        return <Clock className="h-5 w-5 text-gray-400" />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'verified':
        return 'bg-green-100 text-green-800';
      case 'pending':
        return 'bg-yellow-100 text-yellow-800';
      case 'failed':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const services = [
    {
      id: 'pss',
      name: 'Personal Security System',
      description: 'Identity verification and KYC',
      status: verificationStatus.pss,
      port: 4001
    },
    {
      id: 'emo',
      name: 'Easy Management Office',
      description: 'Business verification and management',
      status: verificationStatus.emo,
      port: 4003
    },
    {
      id: 'edr',
      name: 'Exam Decision Registration',
      description: 'Skill testing and certification',
      status: verificationStatus.edr,
      port: 4002
    },
    {
      id: 'jps',
      name: 'Job Profile System',
      description: 'Professional profile management',
      status: verificationStatus.jps,
      port: 4004
    }
  ];

  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-gray-50">
        <Head>
          <title>Dashboard - EHB Technologies</title>
          <meta name="description" content="Your EHB dashboard" />
        </Head>

        {/* Header */}
        <header className="bg-white shadow-sm border-b">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center h-16">
              <div className="flex items-center">
                <div className="text-2xl font-bold text-indigo-600">EHB</div>
                <span className="ml-2 text-gray-500">Dashboard</span>
              </div>

              <div className="flex items-center space-x-4">
                <button className="p-2 text-gray-400 hover:text-gray-600">
                  <Bell className="h-5 w-5" />
                </button>
                <div className="flex items-center space-x-2">
                  <div className="w-8 h-8 bg-indigo-600 rounded-full flex items-center justify-center">
                    <User className="h-4 w-4 text-white" />
                  </div>
                  <span className="text-sm font-medium">{user?.email || 'User'}</span>
                </div>
                <button
                  onClick={logout}
                  className="flex items-center space-x-1 text-gray-600 hover:text-gray-800"
                >
                  <LogOut className="h-4 w-4" />
                  <span className="text-sm">Logout</span>
                </button>
              </div>
            </div>
          </div>
        </header>

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {/* Welcome Section */}
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-gray-900">Welcome back!</h1>
            <p className="text-gray-600 mt-2">Here's your EHB ecosystem overview</p>
          </div>

          {/* Stats Grid */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
            <div className="bg-white rounded-lg shadow p-6">
              <div className="flex items-center">
                <div className="p-2 bg-blue-100 rounded-lg">
                  <Shield className="h-6 w-6 text-blue-600" />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">SQL Level</p>
                  <p className="text-2xl font-bold text-gray-900">{stats.sqlLevel}</p>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-lg shadow p-6">
              <div className="flex items-center">
                <div className="p-2 bg-green-100 rounded-lg">
                  <TrendingUp className="h-6 w-6 text-green-600" />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">Points</p>
                  <p className="text-2xl font-bold text-gray-900">{stats.points}</p>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-lg shadow p-6">
              <div className="flex items-center">
                <div className="p-2 bg-purple-100 rounded-lg">
                  <User className="h-6 w-6 text-purple-600" />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">Rank</p>
                  <p className="text-2xl font-bold text-gray-900">{stats.rank}</p>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-lg shadow p-6">
              <div className="flex items-center">
                <div className="p-2 bg-yellow-100 rounded-lg">
                  <Wallet className="h-6 w-6 text-yellow-600" />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">Services</p>
                  <p className="text-2xl font-bold text-gray-900">{stats.completedServices}/{stats.totalServices}</p>
                </div>
              </div>
            </div>
          </div>

          {/* Services Section */}
          <div className="bg-white rounded-lg shadow">
            <div className="px-6 py-4 border-b border-gray-200">
              <h2 className="text-lg font-medium text-gray-900">Verification Services</h2>
              <p className="text-sm text-gray-600 mt-1">Complete your verification to unlock all features</p>
            </div>

            <div className="p-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {services.map((service) => (
                  <div key={service.id} className="border border-gray-200 rounded-lg p-4">
                    <div className="flex items-center justify-between mb-3">
                      <h3 className="font-medium text-gray-900">{service.name}</h3>
                      {getStatusIcon(service.status)}
                    </div>
                    <p className="text-sm text-gray-600 mb-3">{service.description}</p>
                    <div className="flex items-center justify-between">
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(service.status)}`}>
                        {service.status.charAt(0).toUpperCase() + service.status.slice(1)}
                      </span>
                      <span className="text-xs text-gray-500">Port {service.port}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Quick Actions */}
          <div className="mt-8 bg-white rounded-lg shadow">
            <div className="px-6 py-4 border-b border-gray-200">
              <h2 className="text-lg font-medium text-gray-900">Quick Actions</h2>
            </div>

            <div className="p-6">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <button className="flex items-center justify-center p-4 border border-gray-200 rounded-lg hover:border-indigo-300 hover:bg-indigo-50 transition-colors">
                  <Shield className="h-5 w-5 text-indigo-600 mr-2" />
                  <span className="font-medium">Verify Identity</span>
                </button>

                <button className="flex items-center justify-center p-4 border border-gray-200 rounded-lg hover:border-indigo-300 hover:bg-indigo-50 transition-colors">
                  <TrendingUp className="h-5 w-5 text-indigo-600 mr-2" />
                  <span className="font-medium">Upgrade SQL Level</span>
                </button>

                <button className="flex items-center justify-center p-4 border border-gray-200 rounded-lg hover:border-indigo-300 hover:bg-indigo-50 transition-colors">
                  <Settings className="h-5 w-5 text-indigo-600 mr-2" />
                  <span className="font-medium">Account Settings</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </ProtectedRoute>
  );
}
