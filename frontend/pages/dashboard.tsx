import React, { useState, useEffect } from 'react';
import Head from 'next/head';
import {
  User,
  Shield,
  TrendingUp,
  Wallet,
  ShoppingCart,
  Settings,
  Bell,
  LogOut,
  CheckCircle,
  AlertCircle,
  Clock,
  Star,
  BarChart3,
  Activity,
  CreditCard,
  FileText,
  Users,
  Building,
  Globe,
  Zap
} from 'lucide-react';

interface User {
  id: number;
  username: string;
  email: string;
  sql_level: string;
  sql_points: number;
  sql_rank: string;
  is_verified: boolean;
  verification_progress: number;
  avatar: string;
  created_at: string;
}

interface Service {
  id: number;
  name: string;
  status: string;
  usage: number;
  limit: number;
  price: number;
}

interface Transaction {
  id: number;
  type: string;
  amount: number;
  status: string;
  date: string;
  description: string;
}

export default function EHBDashboard() {
  const [user, setUser] = useState<User | null>(null);
  const [services, setServices] = useState<Service[]>([]);
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [activeTab, setActiveTab] = useState('overview');
  const [loading, setLoading] = useState(true);

  // Mock user data
  const mockUser: User = {
    id: 1,
    username: "john_doe",
    email: "john@example.com",
    sql_level: "Advanced",
    sql_points: 1250,
    sql_rank: "Gold",
    is_verified: true,
    verification_progress: 85,
    avatar: "/avatars/user.jpg",
    created_at: "2024-01-15"
  };

  // Mock services data
  const mockServices: Service[] = [
    {
      id: 1,
      name: "Personal Security System (PSS)",
      status: "active",
      usage: 750,
      limit: 1000,
      price: 29.99
    },
    {
      id: 2,
      name: "Easy Management Office (EMO)",
      status: "active",
      usage: 1200,
      limit: 2000,
      price: 49.99
    },
    {
      id: 3,
      name: "Exam Decision Registration (EDR)",
      status: "inactive",
      usage: 0,
      limit: 1500,
      price: 39.99
    },
    {
      id: 4,
      name: "Job Profile System (JPS)",
      status: "active",
      usage: 450,
      limit: 1000,
      price: 19.99
    },
    {
      id: 5,
      name: "GoSellr E-commerce",
      status: "active",
      usage: 3200,
      limit: 5000,
      price: 79.99
    }
  ];

  // Mock transactions data
  const mockTransactions: Transaction[] = [
    {
      id: 1,
      type: "subscription",
      amount: 29.99,
      status: "completed",
      date: "2024-01-20",
      description: "PSS Monthly Subscription"
    },
    {
      id: 2,
      type: "purchase",
      amount: 49.99,
      status: "completed",
      date: "2024-01-18",
      description: "EMO Service Activation"
    },
    {
      id: 3,
      type: "refund",
      amount: -19.99,
      status: "pending",
      date: "2024-01-15",
      description: "JPS Service Refund"
    }
  ];

  useEffect(() => {
    // Simulate loading
    setTimeout(() => {
      setUser(mockUser);
      setServices(mockServices);
      setTransactions(mockTransactions);
      setLoading(false);
    }, 1000);
  }, []);

  const getSqlLevelColor = (level: string) => {
    switch (level.toLowerCase()) {
      case 'basic': return 'text-blue-600 bg-blue-100';
      case 'intermediate': return 'text-green-600 bg-green-100';
      case 'advanced': return 'text-purple-600 bg-purple-100';
      case 'expert': return 'text-red-600 bg-red-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active': return 'text-green-600 bg-green-100';
      case 'inactive': return 'text-gray-600 bg-gray-100';
      case 'completed': return 'text-green-600 bg-green-100';
      case 'pending': return 'text-yellow-600 bg-yellow-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Head>
        <title>EHB Dashboard</title>
        <meta name="description" content="EHB Dashboard - Your control center" />
      </Head>

      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <div className="text-2xl font-bold text-indigo-600">EHB Dashboard</div>
            </div>

            <div className="flex items-center space-x-4">
              <button className="text-gray-600 hover:text-indigo-600">
                <Bell className="h-5 w-5" />
              </button>
              <div className="flex items-center space-x-2">
                <img src={user?.avatar || "/avatars/default.jpg"} alt="Avatar" className="w-8 h-8 rounded-full" />
                <span className="text-sm font-medium">{user?.username}</span>
              </div>
              <button className="text-gray-600 hover:text-red-600">
                <LogOut className="h-5 w-5" />
              </button>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* User Profile Section */}
        <div className="bg-white rounded-lg shadow-sm p-6 mb-8">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <img src={user?.avatar || "/avatars/default.jpg"} alt="Avatar" className="w-16 h-16 rounded-full" />
              <div>
                <h1 className="text-2xl font-bold text-gray-900">{user?.username}</h1>
                <p className="text-gray-600">{user?.email}</p>
                <div className="flex items-center space-x-2 mt-2">
                  <span className={`px-3 py-1 rounded-full text-sm font-medium ${getSqlLevelColor(user?.sql_level || '')}`}>
                    {user?.sql_level} Level
                  </span>
                  <span className="text-sm text-gray-500">• {user?.sql_points} Points</span>
                  <span className="text-sm text-gray-500">• {user?.sql_rank} Rank</span>
                </div>
              </div>
            </div>

            <div className="text-right">
              <div className="flex items-center space-x-2 mb-2">
                {user?.is_verified ? (
                  <CheckCircle className="h-5 w-5 text-green-600" />
                ) : (
                  <AlertCircle className="h-5 w-5 text-yellow-600" />
                )}
                <span className="text-sm font-medium">
                  {user?.is_verified ? 'Verified' : 'Verification Pending'}
                </span>
              </div>
              <div className="w-32 bg-gray-200 rounded-full h-2">
                <div
                  className="bg-indigo-600 h-2 rounded-full"
                  style={{ width: `${user?.verification_progress || 0}%` }}
                ></div>
              </div>
              <span className="text-xs text-gray-500">{user?.verification_progress}% Complete</span>
            </div>
          </div>
        </div>

        {/* Navigation Tabs */}
        <div className="bg-white rounded-lg shadow-sm mb-8">
          <div className="border-b border-gray-200">
            <nav className="flex space-x-8 px-6">
              {[
                { id: 'overview', name: 'Overview', icon: BarChart3 },
                { id: 'services', name: 'Services', icon: Zap },
                { id: 'transactions', name: 'Transactions', icon: CreditCard },
                { id: 'verification', name: 'Verification', icon: Shield },
                { id: 'settings', name: 'Settings', icon: Settings }
              ].map((tab) => {
                const Icon = tab.icon;
                return (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id)}
                    className={`flex items-center space-x-2 py-4 px-1 border-b-2 font-medium text-sm ${
                      activeTab === tab.id
                        ? 'border-indigo-500 text-indigo-600'
                        : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                    }`}
                  >
                    <Icon className="h-4 w-4" />
                    <span>{tab.name}</span>
                  </button>
                );
              })}
            </nav>
          </div>
        </div>

        {/* Tab Content */}
        <div className="bg-white rounded-lg shadow-sm p-6">
          {activeTab === 'overview' && (
            <div className="space-y-6">
              <h2 className="text-xl font-bold text-gray-900">Dashboard Overview</h2>

              {/* Stats Cards */}
              <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                <div className="bg-gradient-to-r from-blue-500 to-blue-600 rounded-lg p-6 text-white">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-blue-100">Active Services</p>
                      <p className="text-2xl font-bold">{services.filter(s => s.status === 'active').length}</p>
                    </div>
                    <Zap className="h-8 w-8 text-blue-200" />
                  </div>
                </div>

                <div className="bg-gradient-to-r from-green-500 to-green-600 rounded-lg p-6 text-white">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-green-100">SQL Points</p>
                      <p className="text-2xl font-bold">{user?.sql_points}</p>
                    </div>
                    <Star className="h-8 w-8 text-green-200" />
                  </div>
                </div>

                <div className="bg-gradient-to-r from-purple-500 to-purple-600 rounded-lg p-6 text-white">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-purple-100">Monthly Spend</p>
                      <p className="text-2xl font-bold">${services.reduce((sum, s) => sum + (s.status === 'active' ? s.price : 0), 0)}</p>
                    </div>
                    <CreditCard className="h-8 w-8 text-purple-200" />
                  </div>
                </div>

                <div className="bg-gradient-to-r from-orange-500 to-orange-600 rounded-lg p-6 text-white">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-orange-100">Verification</p>
                      <p className="text-2xl font-bold">{user?.verification_progress}%</p>
                    </div>
                    <Shield className="h-8 w-8 text-orange-200" />
                  </div>
                </div>
              </div>

              {/* Recent Activity */}
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Transactions</h3>
                  <div className="space-y-3">
                    {transactions.slice(0, 3).map((transaction) => (
                      <div key={transaction.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                        <div className="flex items-center space-x-3">
                          <div className={`w-2 h-2 rounded-full ${
                            transaction.status === 'completed' ? 'bg-green-500' : 'bg-yellow-500'
                          }`}></div>
                          <div>
                            <p className="font-medium text-gray-900">{transaction.description}</p>
                            <p className="text-sm text-gray-500">{transaction.date}</p>
                          </div>
                        </div>
                        <span className={`font-medium ${
                          transaction.amount > 0 ? 'text-green-600' : 'text-red-600'
                        }`}>
                          ${transaction.amount}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>

                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">Service Usage</h3>
                  <div className="space-y-3">
                    {services.filter(s => s.status === 'active').slice(0, 3).map((service) => (
                      <div key={service.id} className="p-3 bg-gray-50 rounded-lg">
                        <div className="flex items-center justify-between mb-2">
                          <p className="font-medium text-gray-900">{service.name}</p>
                          <span className="text-sm text-gray-500">{service.usage}/{service.limit}</span>
                        </div>
                        <div className="w-full bg-gray-200 rounded-full h-2">
                          <div
                            className="bg-indigo-600 h-2 rounded-full"
                            style={{ width: `${(service.usage / service.limit) * 100}%` }}
                          ></div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'services' && (
            <div className="space-y-6">
              <h2 className="text-xl font-bold text-gray-900">My Services</h2>

              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {services.map((service) => (
                  <div key={service.id} className="border border-gray-200 rounded-lg p-6">
                    <div className="flex items-center justify-between mb-4">
                      <h3 className="font-semibold text-gray-900">{service.name}</h3>
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(service.status)}`}>
                        {service.status}
                      </span>
                    </div>

                    <div className="space-y-3">
                      <div className="flex justify-between text-sm">
                        <span className="text-gray-500">Usage</span>
                        <span className="font-medium">{service.usage}/{service.limit}</span>
                      </div>

                      <div className="w-full bg-gray-200 rounded-full h-2">
                        <div
                          className="bg-indigo-600 h-2 rounded-full"
                          style={{ width: `${(service.usage / service.limit) * 100}%` }}
                        ></div>
                      </div>

                      <div className="flex justify-between text-sm">
                        <span className="text-gray-500">Price</span>
                        <span className="font-medium">${service.price}/month</span>
                      </div>
                    </div>

                    <div className="mt-4 flex space-x-2">
                      <button className="flex-1 px-3 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 text-sm">
                        Manage
                      </button>
                      <button className="px-3 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 text-sm">
                        Settings
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {activeTab === 'transactions' && (
            <div className="space-y-6">
              <h2 className="text-xl font-bold text-gray-900">Transaction History</h2>

              <div className="overflow-x-auto">
                <table className="min-w-full divide-y divide-gray-200">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Date
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Description
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Type
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Amount
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Status
                      </th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    {transactions.map((transaction) => (
                      <tr key={transaction.id}>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                          {transaction.date}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                          {transaction.description}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                          {transaction.type}
                        </td>
                        <td className={`px-6 py-4 whitespace-nowrap text-sm font-medium ${
                          transaction.amount > 0 ? 'text-green-600' : 'text-red-600'
                        }`}>
                          ${transaction.amount}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(transaction.status)}`}>
                            {transaction.status}
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {activeTab === 'verification' && (
            <div className="space-y-6">
              <h2 className="text-xl font-bold text-gray-900">Verification Status</h2>

              <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
                <div className="flex items-center space-x-3 mb-4">
                  <Shield className="h-6 w-6 text-blue-600" />
                  <h3 className="text-lg font-semibold text-blue-900">Identity Verification</h3>
                </div>

                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-blue-700">Verification Progress</span>
                    <span className="text-sm font-medium text-blue-900">{user?.verification_progress}%</span>
                  </div>

                  <div className="w-full bg-blue-200 rounded-full h-3">
                    <div
                      className="bg-blue-600 h-3 rounded-full transition-all duration-300"
                      style={{ width: `${user?.verification_progress || 0}%` }}
                    ></div>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-6">
                    <div className="flex items-center space-x-3">
                      <CheckCircle className="h-5 w-5 text-green-600" />
                      <span className="text-sm text-gray-700">Email Verified</span>
                    </div>
                    <div className="flex items-center space-x-3">
                      <CheckCircle className="h-5 w-5 text-green-600" />
                      <span className="text-sm text-gray-700">Phone Verified</span>
                    </div>
                    <div className="flex items-center space-x-3">
                      <Clock className="h-5 w-5 text-yellow-600" />
                      <span className="text-sm text-gray-700">ID Document Pending</span>
                    </div>
                    <div className="flex items-center space-x-3">
                      <AlertCircle className="h-5 w-5 text-red-600" />
                      <span className="text-sm text-gray-700">Address Verification</span>
                    </div>
                  </div>

                  <button className="mt-6 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
                    Complete Verification
                  </button>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'settings' && (
            <div className="space-y-6">
              <h2 className="text-xl font-bold text-gray-900">Account Settings</h2>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="space-y-4">
                  <h3 className="text-lg font-semibold text-gray-900">Profile Information</h3>

                  <div className="space-y-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700">Username</label>
                      <input
                        type="text"
                        value={user?.username}
                        className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700">Email</label>
                      <input
                        type="email"
                        value={user?.email}
                        className="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                      />
                    </div>

                    <button className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700">
                      Update Profile
                    </button>
                  </div>
                </div>

                <div className="space-y-4">
                  <h3 className="text-lg font-semibold text-gray-900">Security</h3>

                  <div className="space-y-4">
                    <button className="w-full px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 text-left">
                      Change Password
                    </button>
                    <button className="w-full px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 text-left">
                      Two-Factor Authentication
                    </button>
                    <button className="w-full px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 text-left">
                      Connected Devices
                    </button>
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
