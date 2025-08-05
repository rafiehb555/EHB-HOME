import { useState, useEffect } from 'react';
import Head from 'next/head';
import { useAuth } from '@/hooks/useAuth';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import {
  User,
  Shield,
  Building,
  Brain,
  Wallet,
  ShoppingCart,
  Settings,
  LogOut,
  TrendingUp,
  CheckCircle,
  Clock,
  AlertCircle,
  ExternalLink
} from 'lucide-react';
import Link from 'next/link';

const DashboardPage = () => {
  const { user, logout } = useAuth();
  const [activeTab, setActiveTab] = useState('overview');
  const [verificationStatus, setVerificationStatus] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (user) {
      fetchVerificationStatus();
    }
  }, [user]);

  const fetchVerificationStatus = async () => {
    if (!user) return;

    try {
      setLoading(true);
      const token = localStorage.getItem('token');
      const response = await fetch(`http://localhost:8000/api/v1/services/user/${user.id}/verification-status`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        const data = await response.json();
        setVerificationStatus(data);
      }
    } catch (error) {
      console.error('Error fetching verification status:', error);
    } finally {
      setLoading(false);
    }
  };

  const verificationSteps = [
    {
      name: 'PSS Verification',
      icon: Shield,
      service: 'pss',
      description: 'Personal Security System verification',
      color: 'text-blue-600'
    },
    {
      name: 'EMO Verification',
      icon: Building,
      service: 'emo',
      description: 'Easy Management Office verification',
      color: 'text-green-600'
    },
    {
      name: 'EDR Verification',
      icon: Brain,
      service: 'edr',
      description: 'Exam Decision Registration',
      color: 'text-purple-600'
    },
    {
      name: 'JPS Verification',
      icon: User,
      service: 'jps',
      description: 'Job Profile System verification',
      color: 'text-orange-600'
    }
  ];

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'verified':
        return <CheckCircle className="h-5 w-5 text-green-600" />;
      case 'pending':
        return <Clock className="h-5 w-5 text-yellow-600" />;
      case 'failed':
        return <AlertCircle className="h-5 w-5 text-red-600" />;
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

  const getServiceStatus = (serviceName: string) => {
    if (!verificationStatus?.verification_status) return 'pending';
    return verificationStatus.verification_status[serviceName]?.status || 'pending';
  };

  const getServiceScore = (serviceName: string) => {
    if (!verificationStatus?.verification_status) return 0;
    return verificationStatus.verification_status[serviceName]?.score || 0;
  };

  const getOverallProgress = () => {
    if (!verificationStatus) return 0;
    return verificationStatus.overall_progress || 0;
  };

  const getVerifiedCount = () => {
    if (!verificationStatus) return 0;
    return verificationStatus.verified_services || 0;
  };

  const getTotalServices = () => {
    if (!verificationStatus) return 0;
    return verificationStatus.total_services || 0;
  };

  return (
    <ProtectedRoute>
      <Head>
        <title>Dashboard - EHB Technologies</title>
        <meta name="description" content="Your EHB dashboard" />
      </Head>

      <div className="min-h-screen bg-gray-50">
        {/* Header */}
        <header className="bg-white shadow-sm border-b border-gray-200">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center py-4">
              <div className="flex items-center">
                <div className="w-8 h-8 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg flex items-center justify-center">
                  <span className="text-white font-bold text-sm">E</span>
                </div>
                <h1 className="text-xl font-semibold text-gray-900 ml-3">EHB Dashboard</h1>
              </div>
              <div className="flex items-center space-x-4">
                <div className="flex items-center space-x-2">
                  <div className="w-2 h-2 bg-green-400 rounded-full"></div>
                  <span className="text-sm text-gray-600">SQL Level: {user?.sql_level}</span>
                </div>
                <button
                  onClick={logout}
                  className="flex items-center space-x-2 px-3 py-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-md transition-colors"
                >
                  <LogOut className="h-4 w-4" />
                  <span>Logout</span>
                </button>
              </div>
            </div>
          </div>
        </header>

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {/* Welcome Section */}
          <div className="mb-8">
            <h2 className="text-2xl font-bold text-gray-900">
              Welcome back, {user?.full_name}!
            </h2>
            <p className="text-gray-600">
              Your SQL Level: <span className="font-semibold">{user?.sql_level}</span> •
              Points: <span className="font-semibold">{user?.sql_points}</span>
            </p>
          </div>

          {/* Stats Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            <div className="bg-white rounded-lg shadow p-6">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <Shield className="h-8 w-8 text-blue-600" />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">Verification Progress</p>
                  <p className="text-2xl font-semibold text-gray-900">{Math.round(getOverallProgress())}%</p>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-lg shadow p-6">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <TrendingUp className="h-8 w-8 text-green-600" />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">SQL Rank</p>
                  <p className="text-2xl font-semibold text-gray-900">{user?.sql_rank}</p>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-lg shadow p-6">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <Wallet className="h-8 w-8 text-purple-600" />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">Account Status</p>
                  <p className="text-2xl font-semibold text-gray-900">{user?.status}</p>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-lg shadow p-6">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <User className="h-8 w-8 text-indigo-600" />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">User ID</p>
                  <p className="text-2xl font-semibold text-gray-900">#{user?.id}</p>
                </div>
              </div>
            </div>
          </div>

          {/* Verification Steps */}
          <div className="bg-white rounded-lg shadow mb-8">
            <div className="px-6 py-4 border-b border-gray-200">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="text-lg font-medium text-gray-900">Verification Steps</h3>
                  <p className="text-sm text-gray-600">Complete these steps to unlock all features</p>
                </div>
                <Link
                  href="/services"
                  className="flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                >
                  <ExternalLink className="h-4 w-4" />
                  <span>Manage Services</span>
                </Link>
              </div>
            </div>
            <div className="p-6">
              <div className="space-y-4">
                {verificationSteps.map((step) => {
                  const Icon = step.icon;
                  const status = getServiceStatus(step.service);
                  const score = getServiceScore(step.service);

                  return (
                    <div key={step.name} className="flex items-center space-x-4">
                      <div className="flex-shrink-0">
                        <Icon className={`h-6 w-6 ${step.color}`} />
                      </div>
                      <div className="flex-1">
                        <div className="flex items-center justify-between">
                          <div>
                            <p className="text-sm font-medium text-gray-900">{step.name}</p>
                            <p className="text-sm text-gray-500">{step.description}</p>
                            {score > 0 && (
                              <div className="mt-1">
                                <div className="flex items-center space-x-2">
                                  <div className="flex-1 bg-gray-200 rounded-full h-2">
                                    <div
                                      className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                                      style={{ width: `${score}%` }}
                                    ></div>
                                  </div>
                                  <span className="text-xs text-gray-500">{score}%</span>
                                </div>
                              </div>
                            )}
                          </div>
                          <div className="flex items-center space-x-2">
                            {getStatusIcon(status)}
                            <span className={`inline-flex px-2 py-1 text-xs font-semibold rounded-full ${getStatusColor(status)}`}>
                              {status}
                            </span>
                          </div>
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          </div>

          {/* Quick Actions */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <Link href="/services" className="block">
              <div className="bg-white rounded-lg shadow p-6 hover:shadow-md transition-shadow cursor-pointer">
                <div className="flex items-center space-x-3">
                  <Shield className="h-8 w-8 text-blue-600" />
                  <div>
                    <h3 className="text-lg font-medium text-gray-900">Services</h3>
                    <p className="text-sm text-gray-600">Manage verifications</p>
                  </div>
                </div>
              </div>
            </Link>

            <div className="bg-white rounded-lg shadow p-6 hover:shadow-md transition-shadow cursor-pointer">
              <div className="flex items-center space-x-3">
                <ShoppingCart className="h-8 w-8 text-green-600" />
                <div>
                  <h3 className="text-lg font-medium text-gray-900">GoSellr</h3>
                  <p className="text-sm text-gray-600">E-commerce marketplace</p>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-lg shadow p-6 hover:shadow-md transition-shadow cursor-pointer">
              <div className="flex items-center space-x-3">
                <Wallet className="h-8 w-8 text-purple-600" />
                <div>
                  <h3 className="text-lg font-medium text-gray-900">Wallet</h3>
                  <p className="text-sm text-gray-600">Manage your finances</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </ProtectedRoute>
  );
};

export default DashboardPage;
