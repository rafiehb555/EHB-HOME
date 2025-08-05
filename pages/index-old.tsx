import { useState, useEffect } from 'react';
import Head from 'next/head';
import { useQuery } from 'react-query';
import axios from 'axios';
import Layout from '../components/Layout';
import Hero from '../components/Hero';
import Services from '../components/Services';
import {
  Search,
  ShoppingCart,
  Wallet,
  Users,
  Building,
  Shield,
  Brain,
  Bot,
  TrendingUp,
  CheckCircle,
  AlertCircle,
  Clock
} from 'lucide-react';

// Types
interface ServiceStatus {
  [key: string]: string;
}

interface DashboardData {
  user_stats: {
    total_users: number;
    active_users: number;
    new_users_today: number;
    verified_users: number;
  };
  service_stats: {
    gosellr_orders: number;
    wallet_transactions: number;
    franchise_applications: number;
    ai_services_used: number;
  };
  revenue_stats: {
    daily_revenue: number;
    monthly_revenue: number;
    total_revenue: number;
  };
  system_metrics: {
    cpu_usage: number;
    memory_usage: number;
    disk_usage: number;
    network_traffic: number;
  };
}

// API functions
const fetchServicesStatus = async () => {
  const response = await axios.get('http://localhost:8000/api/services/status');
  return response.data;
};

const fetchDashboardData = async () => {
  const response = await axios.get('http://localhost:8000/api/dashboard');
  return response.data;
};

// Components
const Header = () => (
  <header className="bg-white shadow-sm border-b border-gray-200">
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div className="flex justify-between items-center h-16">
        <div className="flex items-center">
          <h1 className="text-2xl font-bold text-gradient">EHB Technologies</h1>
        </div>
        <div className="flex items-center space-x-4">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
            <input
              type="text"
              placeholder="Search services, users, dashboards..."
              className="pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent w-64"
            />
          </div>
          <button className="btn-primary">Login</button>
        </div>
      </div>
    </div>
  </header>
);

const ServiceCard = ({
  title,
  description,
  icon: Icon,
  status,
  port
}: {
  title: string;
  description: string;
  icon: any;
  status: string;
  port: number;
}) => (
  <div className="service-card">
    <div className="flex items-start space-x-4">
      <div className="flex-shrink-0">
        <Icon className="h-8 w-8 text-primary-600" />
      </div>
      <div className="flex-1 min-w-0">
        <h3 className="text-lg font-semibold text-gray-900">{title}</h3>
        <p className="text-sm text-gray-600 mt-1">{description}</p>
        <div className="flex items-center mt-3 space-x-2">
          <span className={`status-badge status-${status === 'ready' ? 'ready' : status === 'pending' ? 'pending' : 'error'}`}>
            {status === 'ready' && <CheckCircle className="h-3 w-3 mr-1" />}
            {status === 'pending' && <Clock className="h-3 w-3 mr-1" />}
            {status === 'error' && <AlertCircle className="h-3 w-3 mr-1" />}
            {status}
          </span>
          <span className="text-xs text-gray-500">Port: {port}</span>
        </div>
      </div>
    </div>
  </div>
);

const StatsCard = ({ title, value, change, icon: Icon }: {
  title: string;
  value: string | number;
  change?: string;
  icon: any;
}) => (
  <div className="card">
    <div className="flex items-center">
      <div className="flex-shrink-0">
        <Icon className="h-8 w-8 text-primary-600" />
      </div>
      <div className="ml-4">
        <p className="text-sm font-medium text-gray-600">{title}</p>
        <p className="text-2xl font-semibold text-gray-900">{value}</p>
        {change && (
          <p className="text-sm text-success-600 flex items-center">
            <TrendingUp className="h-3 w-3 mr-1" />
            {change}
          </p>
        )}
      </div>
    </div>
  </div>
);

export default function HomePage() {
  const [searchTerm, setSearchTerm] = useState('');

  // Fetch data
  const { data: servicesStatus, isLoading: servicesLoading } = useQuery(
    'servicesStatus',
    fetchServicesStatus,
    { refetchInterval: 5000 }
  );

  const { data: dashboardData, isLoading: dashboardLoading } = useQuery(
    'dashboardData',
    fetchDashboardData,
    { refetchInterval: 10000 }
  );

  // Services configuration
  const services = [
    {
      title: 'GoSellr',
      description: 'E-commerce marketplace with SQL-based visibility',
      icon: ShoppingCart,
      port: 4004,
      key: 'gosellr'
    },
    {
      title: 'Wallet',
      description: 'Payment & transaction system with EHBGC integration',
      icon: Wallet,
      port: 5001,
      key: 'wallet'
    },
    {
      title: 'PSS',
      description: 'Personal Security System for KYC verification',
      icon: Shield,
      port: 4001,
      key: 'pss'
    },
    {
      title: 'EMO',
      description: 'Easy Management Office for business verification',
      icon: Building,
      port: 4003,
      key: 'emo'
    },
    {
      title: 'EDR',
      description: 'Exam Decision Registration for skill testing',
      icon: Brain,
      port: 4002,
      key: 'edr'
    },
    {
      title: 'JPS',
      description: 'Job Profile System for user profiles',
      icon: Users,
      port: 4005,
      key: 'jps'
    },
    {
      title: 'AI Agent',
      description: 'Intelligent automation engine',
      icon: Bot,
      port: 4007,
      key: 'ai_agent'
    },
    {
      title: 'AI Robot',
      description: 'Advanced autonomous assistant',
      icon: Bot,
      port: 4008,
      key: 'ai_robot'
    }
  ];

  return (
    <>
      <Head>
        <title>EHB Home Page & Dashboard</title>
        <meta name="description" content="Complete ecosystem for EHB Technologies" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <div className="min-h-screen bg-gray-50">
        <Header />

        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {/* Hero Section */}
          <section className="text-center mb-12">
            <h1 className="text-4xl font-bold text-gray-900 mb-4">
              Welcome to <span className="text-gradient">EHB Technologies</span>
            </h1>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Complete ecosystem for decentralized commerce, AI services, and blockchain integration
            </p>
          </section>

          {/* Stats Section */}
          {dashboardData && (
            <section className="mb-12">
              <h2 className="text-2xl font-semibold text-gray-900 mb-6">System Overview</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <StatsCard
                  title="Total Users"
                                      value={(dashboardData.user_stats?.total_users || 0).toLocaleString()}
                  icon={Users}
                />
                <StatsCard
                  title="Active Users"
                  value={dashboardData.user_stats.active_users.toLocaleString()}
                  icon={TrendingUp}
                />
                <StatsCard
                  title="Daily Revenue"
                  value={`$${dashboardData.revenue_stats.daily_revenue.toLocaleString()}`}
                  icon={Wallet}
                />
                <StatsCard
                  title="GoSellr Orders"
                  value={dashboardData.service_stats.gosellr_orders.toLocaleString()}
                  icon={ShoppingCart}
                />
              </div>
            </section>
          )}

          {/* Services Section */}
          <section className="mb-12">
            <h2 className="text-2xl font-semibold text-gray-900 mb-6">EHB Services</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {services.map((service) => (
                <ServiceCard
                  key={service.key}
                  title={service.title}
                  description={service.description}
                  icon={service.icon}
                  status={servicesStatus?.services?.[service.key] || 'pending'}
                  port={service.port}
                />
              ))}
            </div>
          </section>

          {/* System Health */}
          {servicesStatus && (
            <section className="mb-12">
              <h2 className="text-2xl font-semibold text-gray-900 mb-6">System Health</h2>
              <div className="card">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                  <div>
                    <h3 className="text-lg font-medium text-gray-900 mb-2">Services Status</h3>
                    <p className="text-3xl font-bold text-primary-600">
                      {servicesStatus.healthy_services}/{servicesStatus.total_services}
                    </p>
                    <p className="text-sm text-gray-600">Healthy Services</p>
                  </div>
                  <div>
                    <h3 className="text-lg font-medium text-gray-900 mb-2">System Health</h3>
                    <p className={`text-3xl font-bold ${
                      servicesStatus.system_health === 'healthy'
                        ? 'text-success-600'
                        : 'text-warning-600'
                    }`}>
                      {servicesStatus.system_health}
                    </p>
                    <p className="text-sm text-gray-600">Overall Status</p>
                  </div>
                  <div>
                    <h3 className="text-lg font-medium text-gray-900 mb-2">Active Users</h3>
                    <p className="text-3xl font-bold text-primary-600">
                      {dashboardData?.user_stats.active_users || 0}
                    </p>
                    <p className="text-sm text-gray-600">Currently Online</p>
                  </div>
                </div>
              </div>
            </section>
          )}

          {/* Quick Actions */}
          <section>
            <h2 className="text-2xl font-semibold text-gray-900 mb-6">Quick Actions</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              <button className="btn-primary w-full">
                <ShoppingCart className="h-5 w-5 mr-2" />
                Go to GoSellr
              </button>
              <button className="btn-secondary w-full">
                <Wallet className="h-5 w-5 mr-2" />
                Open Wallet
              </button>
              <button className="btn-secondary w-full">
                <Shield className="h-5 w-5 mr-2" />
                Verify Identity
              </button>
              <button className="btn-secondary w-full">
                <Bot className="h-5 w-5 mr-2" />
                AI Assistant
              </button>
            </div>
          </section>
        </main>
      </div>
    </>
  );
}
