import { useState } from 'react';
import { useQuery } from 'react-query';
import axios from 'axios';
import Layout from '../components/Layout';
import Hero from '../components/Hero';
import Services from '../components/Services';
import {
  Users,
  TrendingUp,
  Wallet,
  ShoppingCart,
  Shield,
  Building,
  Brain,
  Bot
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

// Helper functions
const getServiceIcon = (service: string) => {
  const icons: { [key: string]: any } = {
    gosellr: ShoppingCart,
    wallet: Wallet,
    pss: Shield,
    emo: Building,
    edr: Brain,
    jps: Users,
    ai_agent: Bot,
    ai_robot: Bot,
    sql: Brain,
    franchise: Building
  };
  return icons[service] || Users;
};

const getServicePort = (service: string) => {
  const ports: { [key: string]: number } = {
    gosellr: 4004,
    wallet: 5001,
    pss: 4001,
    emo: 4003,
    edr: 4002,
    jps: 4005,
    ai_agent: 4007,
    ai_robot: 4008,
    franchise: 4006
  };
  return ports[service] || 0;
};

// Components
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
  <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow">
    <div className="flex items-start space-x-4">
      <div className="flex-shrink-0">
        <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
          <Icon className="w-6 h-6 text-blue-600" />
        </div>
      </div>
      <div className="flex-1 min-w-0">
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-semibold text-gray-900">{title}</h3>
          <span className="text-sm text-gray-500">Port {port}</span>
        </div>
        <p className="text-sm text-gray-600 mt-1">{description}</p>
        <div className="flex items-center mt-3">
          <div className={`w-2 h-2 rounded-full mr-2 ${
            status === 'ready' ? 'bg-green-500' :
            status === 'initializing' ? 'bg-yellow-500' : 'bg-red-500'
          }`}></div>
          <span className="text-sm text-gray-600 capitalize">{status}</span>
        </div>
      </div>
    </div>
  </div>
);

const StatsCard = ({
  title,
  value,
  change,
  icon: Icon
}: {
  title: string;
  value: string | number;
  change?: string;
  icon: any;
}) => (
  <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
    <div className="flex items-center">
      <div className="flex-shrink-0">
        <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
          <Icon className="w-6 h-6 text-blue-600" />
        </div>
      </div>
      <div className="ml-4 flex-1">
        <p className="text-sm font-medium text-gray-600">{title}</p>
        <p className="text-2xl font-bold text-gray-900">{value}</p>
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

export default function HomePage() {
  const { data: servicesStatus, isLoading: servicesLoading } = useQuery(
    'servicesStatus',
    fetchServicesStatus,
    {
      refetchInterval: 30000, // Refetch every 30 seconds
    }
  );

  const { data: dashboardData, isLoading: dashboardLoading } = useQuery(
    'dashboardData',
    fetchDashboardData,
    {
      refetchInterval: 60000, // Refetch every minute
    }
  );

  return (
    <Layout title="EHB Technologies - Home Page">
      <Hero />
      <Services />

      {/* Dashboard Section */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              Live System Status
            </h2>
            <p className="text-gray-600">
              Real-time monitoring of all EHB services and system metrics
            </p>
          </div>

          {/* Services Status */}
          {servicesLoading ? (
            <div className="text-center py-8">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
              <p className="mt-4 text-gray-600">Loading services status...</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
              {servicesStatus?.services && Object.entries(servicesStatus.services).map(([service, status]) => (
                <ServiceCard
                  key={service}
                  title={service.toUpperCase()}
                  description={`${service} service status`}
                  icon={getServiceIcon(service)}
                  status={status as string}
                  port={getServicePort(service)}
                />
              ))}
            </div>
          )}

          {/* Dashboard Stats */}
          {dashboardLoading ? (
            <div className="text-center py-8">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
              <p className="mt-4 text-gray-600">Loading dashboard data...</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
              {dashboardData && (
                <>
                  <StatsCard
                    title="Total Users"
                    value={dashboardData.user_stats.total_users}
                    icon={Users}
                  />
                  <StatsCard
                    title="Active Users"
                    value={dashboardData.user_stats.active_users}
                    icon={TrendingUp}
                  />
                  <StatsCard
                    title="Daily Revenue"
                    value={`$${dashboardData.revenue_stats.daily_revenue.toLocaleString()}`}
                    icon={Wallet}
                  />
                  <StatsCard
                    title="GoSellr Orders"
                    value={dashboardData.service_stats.gosellr_orders}
                    icon={ShoppingCart}
                  />
                </>
              )}
            </div>
          )}

          {/* Quick Actions */}
          <div className="bg-gray-50 rounded-lg p-6 mb-8">
            <h3 className="text-xl font-bold text-gray-900 mb-4">Quick Actions</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <button className="flex items-center justify-center space-x-2 bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors">
                <Shield className="w-5 h-5" />
                <span>Start Verification</span>
              </button>
              <button className="flex items-center justify-center space-x-2 bg-green-600 text-white px-6 py-3 rounded-lg hover:bg-green-700 transition-colors">
                <ShoppingCart className="w-5 h-5" />
                <span>Create Store</span>
              </button>
              <button className="flex items-center justify-center space-x-2 bg-purple-600 text-white px-6 py-3 rounded-lg hover:bg-purple-700 transition-colors">
                <Wallet className="w-5 h-5" />
                <span>Access Wallet</span>
              </button>
            </div>
          </div>

          {/* System Health */}
          <div className="bg-gray-50 rounded-lg p-6">
            <h3 className="text-xl font-bold text-gray-900 mb-4">System Health</h3>
            {dashboardData && (
              <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div className="text-center">
                  <div className="text-2xl font-bold text-gray-900">
                    {dashboardData.system_metrics.cpu_usage}%
                  </div>
                  <div className="text-sm text-gray-600">CPU Usage</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-gray-900">
                    {dashboardData.system_metrics.memory_usage}%
                  </div>
                  <div className="text-sm text-gray-600">Memory Usage</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-gray-900">
                    {dashboardData.system_metrics.disk_usage}%
                  </div>
                  <div className="text-sm text-gray-600">Disk Usage</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-gray-900">
                    {dashboardData.system_metrics.network_traffic} MB
                  </div>
                  <div className="text-sm text-gray-600">Network Traffic</div>
                </div>
              </div>
            )}
          </div>
        </div>
      </section>
    </Layout>
  );
}
