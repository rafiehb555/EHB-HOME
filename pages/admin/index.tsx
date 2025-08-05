import { useState } from 'react';
import Head from 'next/head';
import { useQuery } from 'react-query';
import axios from 'axios';
import {
  Users,
  TrendingUp,
  DollarSign,
  ShoppingCart,
  Shield,
  Building,
  Brain,
  Bot,
  Activity,
  AlertCircle,
  CheckCircle,
  Clock
} from 'lucide-react';
import Sidebar from '@/components/admin/Sidebar';

interface AdminStats {
  total_users: number;
  active_users: number;
  new_users_today: number;
  revenue_today: number;
  revenue_month: number;
  total_orders: number;
  pending_verifications: number;
  system_health: string;
}

interface ServiceStatus {
  name: string;
  status: 'ready' | 'pending' | 'error';
  port: number;
  users: number;
  uptime: string;
}

const AdminDashboard = () => {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  // Mock data for now - replace with actual API calls
  const { data: stats } = useQuery('adminStats', async () => {
    // In real app, fetch from /api/admin/stats
    return {
      total_users: 1250,
      active_users: 890,
      new_users_today: 45,
      revenue_today: 12500,
      revenue_month: 375000,
      total_orders: 156,
      pending_verifications: 23,
      system_health: 'healthy'
    } as AdminStats;
  });

  const { data: services } = useQuery('serviceStatus', async () => {
    // In real app, fetch from /api/admin/services
    return [
      { name: 'GoSellr', status: 'ready', port: 4004, users: 450, uptime: '99.9%' },
      { name: 'Wallet', status: 'ready', port: 5001, users: 320, uptime: '99.8%' },
      { name: 'PSS', status: 'ready', port: 4001, users: 890, uptime: '99.9%' },
      { name: 'EMO', status: 'ready', port: 4003, users: 234, uptime: '99.7%' },
      { name: 'EDR', status: 'pending', port: 4002, users: 156, uptime: '98.5%' },
      { name: 'JPS', status: 'ready', port: 4005, users: 678, uptime: '99.9%' },
      { name: 'AI Agent', status: 'ready', port: 4007, users: 89, uptime: '99.6%' },
      { name: 'AI Robot', status: 'error', port: 4008, users: 12, uptime: '85.2%' }
    ] as ServiceStatus[];
  });

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'ready':
        return 'bg-green-100 text-green-800';
      case 'pending':
        return 'bg-yellow-100 text-yellow-800';
      case 'error':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'ready':
        return <CheckCircle className="h-4 w-4 text-green-600" />;
      case 'pending':
        return <Clock className="h-4 w-4 text-yellow-600" />;
      case 'error':
        return <AlertCircle className="h-4 w-4 text-red-600" />;
      default:
        return <Activity className="h-4 w-4 text-gray-400" />;
    }
  };

  const StatCard = ({ title, value, change, icon: Icon, color }: {
    title: string;
    value: string | number;
    change?: string;
    icon: any;
    color: string;
  }) => (
    <div className="card">
      <div className="flex items-center">
        <div className="flex-shrink-0">
          <Icon className={`h-8 w-8 ${color}`} />
        </div>
        <div className="ml-4">
          <p className="text-sm font-medium text-gray-600">{title}</p>
          <p className="text-2xl font-semibold text-gray-900">{value}</p>
          {change && (
            <p className="text-sm text-green-600 flex items-center">
              <TrendingUp className="h-3 w-3 mr-1" />
              {change}
            </p>
          )}
        </div>
      </div>
    </div>
  );

  return (
    <>
      <Head>
        <title>Admin Dashboard - EHB Technologies</title>
        <meta name="description" content="EHB Admin Dashboard" />
      </Head>

      <div className="flex h-screen bg-gray-100">
        <Sidebar isOpen={sidebarOpen} onToggle={() => setSidebarOpen(!sidebarOpen)} />

        <div className="flex-1 flex flex-col overflow-hidden">
          {/* Header */}
          <header className="bg-white shadow-sm border-b border-gray-200">
            <div className="flex items-center justify-between px-6 py-4">
              <div className="flex items-center">
                <button
                  onClick={() => setSidebarOpen(true)}
                  className="lg:hidden p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100"
                >
                  <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                  </svg>
                </button>
                <h1 className="text-2xl font-semibold text-gray-900 ml-4">Admin Dashboard</h1>
              </div>
              <div className="flex items-center space-x-4">
                <div className="flex items-center space-x-2">
                  <div className="w-2 h-2 bg-green-400 rounded-full"></div>
                  <span className="text-sm text-gray-600">System Online</span>
                </div>
                <button className="btn-primary">Settings</button>
              </div>
            </div>
          </header>

          {/* Main Content */}
          <main className="flex-1 overflow-y-auto p-6">
            {/* Stats Grid */}
            {stats && (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
                <StatCard
                  title="Total Users"
                  value={stats.total_users.toLocaleString()}
                  change="+12% from last month"
                  icon={Users}
                  color="text-blue-600"
                />
                <StatCard
                  title="Revenue Today"
                  value={`$${stats.revenue_today.toLocaleString()}`}
                  change="+8% from yesterday"
                  icon={DollarSign}
                  color="text-green-600"
                />
                <StatCard
                  title="Total Orders"
                  value={stats.total_orders.toLocaleString()}
                  change="+5% from last week"
                  icon={ShoppingCart}
                  color="text-purple-600"
                />
                <StatCard
                  title="Active Users"
                  value={stats.active_users.toLocaleString()}
                  change="+15% from yesterday"
                  icon={Activity}
                  color="text-orange-600"
                />
              </div>
            )}

            {/* Services Status */}
            {services && (
              <div className="mb-8">
                <h2 className="text-xl font-semibold text-gray-900 mb-4">Services Status</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {services.map((service) => (
                    <div key={service.name} className="card">
                      <div className="flex items-center justify-between mb-4">
                        <h3 className="text-lg font-medium text-gray-900">{service.name}</h3>
                        <span className={`inline-flex items-center px-2 py-1 text-xs font-semibold rounded-full ${getStatusColor(service.status)}`}>
                          {getStatusIcon(service.status)}
                          <span className="ml-1">{service.status}</span>
                        </span>
                      </div>
                      <div className="space-y-2">
                        <div className="flex justify-between text-sm">
                          <span className="text-gray-600">Port</span>
                          <span className="font-medium">{service.port}</span>
                        </div>
                        <div className="flex justify-between text-sm">
                          <span className="text-gray-600">Active Users</span>
                          <span className="font-medium">{service.users}</span>
                        </div>
                        <div className="flex justify-between text-sm">
                          <span className="text-gray-600">Uptime</span>
                          <span className="font-medium">{service.uptime}</span>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Quick Actions */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {/* Recent Activity */}
              <div className="card">
                <h3 className="text-lg font-medium text-gray-900 mb-4">Recent Activity</h3>
                <div className="space-y-3">
                  <div className="flex items-center space-x-3">
                    <div className="w-2 h-2 bg-blue-400 rounded-full"></div>
                    <span className="text-sm text-gray-600">New user registration: John Doe</span>
                    <span className="text-xs text-gray-400">2 min ago</span>
                  </div>
                  <div className="flex items-center space-x-3">
                    <div className="w-2 h-2 bg-green-400 rounded-full"></div>
                    <span className="text-sm text-gray-600">Order completed: #ORD-1234</span>
                    <span className="text-xs text-gray-400">5 min ago</span>
                  </div>
                  <div className="flex items-center space-x-3">
                    <div className="w-2 h-2 bg-yellow-400 rounded-full"></div>
                    <span className="text-sm text-gray-600">PSS verification pending: Jane Smith</span>
                    <span className="text-xs text-gray-400">10 min ago</span>
                  </div>
                </div>
              </div>

              {/* System Health */}
              <div className="card">
                <h3 className="text-lg font-medium text-gray-900 mb-4">System Health</h3>
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-600">CPU Usage</span>
                    <div className="flex items-center space-x-2">
                      <div className="w-16 bg-gray-200 rounded-full h-2">
                        <div className="bg-green-600 h-2 rounded-full" style={{ width: '45%' }}></div>
                      </div>
                      <span className="text-sm font-medium">45%</span>
                    </div>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-600">Memory Usage</span>
                    <div className="flex items-center space-x-2">
                      <div className="w-16 bg-gray-200 rounded-full h-2">
                        <div className="bg-blue-600 h-2 rounded-full" style={{ width: '62%' }}></div>
                      </div>
                      <span className="text-sm font-medium">62%</span>
                    </div>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-600">Disk Usage</span>
                    <div className="flex items-center space-x-2">
                      <div className="w-16 bg-gray-200 rounded-full h-2">
                        <div className="bg-yellow-600 h-2 rounded-full" style={{ width: '38%' }}></div>
                      </div>
                      <span className="text-sm font-medium">38%</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </main>
        </div>
      </div>
    </>
  );
};

export default AdminDashboard;
