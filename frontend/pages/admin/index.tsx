import ProtectedRoute from '@/components/auth/ProtectedRoute';
import { useAuth } from '@/hooks/useAuth';
import {
    Activity,
    AlertTriangle,
    CheckCircle,
    Clock,
    Database,
    Server,
    Settings,
    Shield,
    TrendingUp,
    Users
} from 'lucide-react';
import Head from 'next/head';
import { useState } from 'react';

interface ServiceStatus {
  name: string;
  status: 'running' | 'stopped' | 'error';
  port: number;
  uptime: string;
  requests: number;
}

export default function AdminDashboard() {
  const { user } = useAuth();
  const [services, setServices] = useState<ServiceStatus[]>([
    {
      name: 'Backend API',
      status: 'running',
      port: 8000,
      uptime: '2h 15m',
      requests: 1247
    },
    {
      name: 'PSS Service',
      status: 'running',
      port: 4001,
      uptime: '1h 45m',
      requests: 892
    },
    {
      name: 'EMO Service',
      status: 'running',
      port: 4003,
      uptime: '1h 30m',
      requests: 654
    },
    {
      name: 'EDR Service',
      status: 'running',
      port: 4002,
      uptime: '1h 20m',
      requests: 543
    }
  ]);

  const [stats, setStats] = useState({
    totalUsers: 1250,
    activeUsers: 890,
    totalRevenue: 2500000,
    pendingVerifications: 45
  });

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'running':
        return <CheckCircle className="h-5 w-5 text-green-500" />;
      case 'stopped':
        return <Clock className="h-5 w-5 text-yellow-500" />;
      case 'error':
        return <AlertTriangle className="h-5 w-5 text-red-500" />;
      default:
        return <Clock className="h-5 w-5 text-gray-400" />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'running':
        return 'bg-green-100 text-green-800';
      case 'stopped':
        return 'bg-yellow-100 text-yellow-800';
      case 'error':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <ProtectedRoute requireAdmin={true}>
      <div className="min-h-screen bg-gray-50">
        <Head>
          <title>Admin Dashboard - EHB Technologies</title>
          <meta name="description" content="EHB Admin Dashboard" />
        </Head>

        {/* Header */}
        <header className="bg-white shadow-sm border-b">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center h-16">
              <div className="flex items-center">
                <div className="text-2xl font-bold text-indigo-600">EHB</div>
                <span className="ml-2 text-gray-500">Admin Dashboard</span>
              </div>

              <div className="flex items-center space-x-4">
                <span className="text-sm text-gray-600">Admin: {user?.email}</span>
              </div>
            </div>
          </div>
        </header>

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {/* Welcome Section */}
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-gray-900">Admin Dashboard</h1>
            <p className="text-gray-600 mt-2">Monitor and manage the EHB ecosystem</p>
          </div>

          {/* Stats Grid */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
            <div className="bg-white rounded-lg shadow p-6">
              <div className="flex items-center">
                <div className="p-2 bg-blue-100 rounded-lg">
                  <Users className="h-6 w-6 text-blue-600" />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">Total Users</p>
                  <p className="text-2xl font-bold text-gray-900">{stats.totalUsers.toLocaleString()}</p>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-lg shadow p-6">
              <div className="flex items-center">
                <div className="p-2 bg-green-100 rounded-lg">
                  <Activity className="h-6 w-6 text-green-600" />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">Active Users</p>
                  <p className="text-2xl font-bold text-gray-900">{stats.activeUsers.toLocaleString()}</p>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-lg shadow p-6">
              <div className="flex items-center">
                <div className="p-2 bg-purple-100 rounded-lg">
                  <TrendingUp className="h-6 w-6 text-purple-600" />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">Revenue</p>
                  <p className="text-2xl font-bold text-gray-900">${(stats.totalRevenue / 1000000).toFixed(1)}M</p>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-lg shadow p-6">
              <div className="flex items-center">
                <div className="p-2 bg-yellow-100 rounded-lg">
                  <Shield className="h-6 w-6 text-yellow-600" />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">Pending</p>
                  <p className="text-2xl font-bold text-gray-900">{stats.pendingVerifications}</p>
                </div>
              </div>
            </div>
          </div>

          {/* Services Status */}
          <div className="bg-white rounded-lg shadow">
            <div className="px-6 py-4 border-b border-gray-200">
              <h2 className="text-lg font-medium text-gray-900">Service Status</h2>
              <p className="text-sm text-gray-600 mt-1">Monitor all EHB services</p>
            </div>

            <div className="p-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {services.map((service) => (
                  <div key={service.name} className="border border-gray-200 rounded-lg p-4">
                    <div className="flex items-center justify-between mb-3">
                      <div className="flex items-center space-x-3">
                        <Server className="h-5 w-5 text-gray-400" />
                        <div>
                          <h3 className="font-medium text-gray-900">{service.name}</h3>
                          <p className="text-sm text-gray-500">Port {service.port}</p>
                        </div>
                      </div>
                      {getStatusIcon(service.status)}
                    </div>

                    <div className="grid grid-cols-2 gap-4 text-sm">
                      <div>
                        <p className="text-gray-600">Uptime</p>
                        <p className="font-medium">{service.uptime}</p>
                      </div>
                      <div>
                        <p className="text-gray-600">Requests</p>
                        <p className="font-medium">{service.requests.toLocaleString()}</p>
                      </div>
                    </div>

                    <div className="mt-3">
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(service.status)}`}>
                        {service.status.charAt(0).toUpperCase() + service.status.slice(1)}
                      </span>
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
              <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                <button className="flex items-center justify-center p-4 border border-gray-200 rounded-lg hover:border-indigo-300 hover:bg-indigo-50 transition-colors">
                  <Users className="h-5 w-5 text-indigo-600 mr-2" />
                  <span className="font-medium">Manage Users</span>
                </button>

                <button className="flex items-center justify-center p-4 border border-gray-200 rounded-lg hover:border-indigo-300 hover:bg-indigo-50 transition-colors">
                  <Shield className="h-5 w-5 text-indigo-600 mr-2" />
                  <span className="font-medium">Verify Users</span>
                </button>

                <button className="flex items-center justify-center p-4 border border-gray-200 rounded-lg hover:border-indigo-300 hover:bg-indigo-50 transition-colors">
                  <Database className="h-5 w-5 text-indigo-600 mr-2" />
                  <span className="font-medium">System Logs</span>
                </button>

                <button className="flex items-center justify-center p-4 border border-gray-200 rounded-lg hover:border-indigo-300 hover:bg-indigo-50 transition-colors">
                  <Settings className="h-5 w-5 text-indigo-600 mr-2" />
                  <span className="font-medium">Settings</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </ProtectedRoute>
  );
}
