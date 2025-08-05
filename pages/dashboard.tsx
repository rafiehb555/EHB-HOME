import { useState } from 'react';
import { useQuery } from 'react-query';
import axios from 'axios';
import Layout from '../components/Layout';
import {
  Users,
  TrendingUp,
  Wallet,
  ShoppingCart,
  Shield,
  Building,
  Brain,
  Bot,
  Settings,
  Activity,
  AlertTriangle,
  CheckCircle,
  Clock,
  BarChart3,
  PieChart,
  LineChart
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
const MetricCard = ({
  title,
  value,
  change,
  icon: Icon,
  color = 'blue'
}: {
  title: string;
  value: string | number;
  change?: string;
  icon: any;
  color?: string;
}) => (
  <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
    <div className="flex items-center justify-between">
      <div>
        <p className="text-sm font-medium text-gray-600">{title}</p>
        <p className="text-2xl font-bold text-gray-900">{value}</p>
        {change && (
          <p className="text-sm text-green-600 flex items-center mt-1">
            <TrendingUp className="h-3 w-3 mr-1" />
            {change}
          </p>
        )}
      </div>
      <div className={`w-12 h-12 bg-${color}-100 rounded-lg flex items-center justify-center`}>
        <Icon className={`w-6 h-6 text-${color}-600`} />
      </div>
    </div>
  </div>
);

const ServiceStatusCard = ({
  service,
  status,
  port
}: {
  service: string;
  status: string;
  port: number;
}) => {
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'ready': return 'green';
      case 'initializing': return 'yellow';
      case 'error': return 'red';
      default: return 'gray';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'ready': return <CheckCircle className="w-5 h-5" />;
      case 'initializing': return <Clock className="w-5 h-5" />;
      case 'error': return <AlertTriangle className="w-5 h-5" />;
      default: return <Activity className="w-5 h-5" />;
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="font-semibold text-gray-900">{service.toUpperCase()}</h3>
          <p className="text-sm text-gray-600">Port {port}</p>
        </div>
        <div className={`text-${getStatusColor(status)}-600`}>
          {getStatusIcon(status)}
        </div>
      </div>
      <div className="mt-2">
        <div className={`w-full bg-gray-200 rounded-full h-2`}>
          <div
            className={`bg-${getStatusColor(status)}-500 h-2 rounded-full transition-all duration-300`}
            style={{ width: status === 'ready' ? '100%' : status === 'initializing' ? '50%' : '0%' }}
          ></div>
        </div>
        <p className={`text-sm text-${getStatusColor(status)}-600 mt-1 capitalize`}>
          {status}
        </p>
      </div>
    </div>
  );
};

const ChartCard = ({ title, children }: { title: string; children: React.ReactNode }) => (
  <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
    <h3 className="text-lg font-semibold text-gray-900 mb-4">{title}</h3>
    {children}
  </div>
);

export default function Dashboard() {
  const [activeTab, setActiveTab] = useState('overview');

  const { data: servicesStatus, isLoading: servicesLoading } = useQuery(
    'servicesStatus',
    fetchServicesStatus,
    {
      refetchInterval: 30000,
    }
  );

  const { data: dashboardData, isLoading: dashboardLoading } = useQuery(
    'dashboardData',
    fetchDashboardData,
    {
      refetchInterval: 60000,
    }
  );

  const tabs = [
    { id: 'overview', name: 'Overview', icon: BarChart3 },
    { id: 'services', name: 'Services', icon: Settings },
    { id: 'analytics', name: 'Analytics', icon: PieChart },
    { id: 'monitoring', name: 'Monitoring', icon: LineChart },
  ];

  return (
    <Layout title="EHB Dashboard - Admin Panel">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">EHB Dashboard</h1>
          <p className="text-gray-600">Complete system monitoring and administration</p>
        </div>

        {/* Tabs */}
        <div className="border-b border-gray-200 mb-8">
          <nav className="-mb-px flex space-x-8">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`py-2 px-1 border-b-2 font-medium text-sm ${
                  activeTab === tab.id
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                <tab.icon className="w-4 h-4 inline mr-2" />
                {tab.name}
              </button>
            ))}
          </nav>
        </div>

        {/* Content based on active tab */}
        {activeTab === 'overview' && (
          <div className="space-y-6">
            {/* Key Metrics */}
            {dashboardLoading ? (
              <div className="text-center py-8">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
                <p className="mt-4 text-gray-600">Loading dashboard data...</p>
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                {dashboardData ? (
                  <>
                    <MetricCard
                      title="Total Users"
                      value={dashboardData.user_stats?.total_users || 0}
                      icon={Users}
                      color="blue"
                    />
                    <MetricCard
                      title="Active Users"
                      value={dashboardData.user_stats?.active_users || 0}
                      icon={TrendingUp}
                      color="green"
                    />
                    <MetricCard
                      title="Daily Revenue"
                      value={`$${(dashboardData.revenue_stats?.daily_revenue || 0).toLocaleString()}`}
                      icon={Wallet}
                      color="purple"
                    />
                    <MetricCard
                      title="GoSellr Orders"
                      value={dashboardData.service_stats?.gosellr_orders || 0}
                      icon={ShoppingCart}
                      color="orange"
                    />
                  </>
                ) : (
                  <div className="col-span-4 text-center py-8">
                    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
                    <p className="text-gray-600">Loading dashboard data...</p>
                  </div>
                )}
              </div>
            )}

            {/* System Health */}
            <ChartCard title="System Health">
              {dashboardData ? (
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <div className="text-center">
                    <div className="text-2xl font-bold text-gray-900">
                      {dashboardData.system_metrics?.cpu_usage || 0}%
                    </div>
                    <div className="text-sm text-gray-600">CPU</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-gray-900">
                      {dashboardData.system_metrics?.memory_usage || 0}%
                    </div>
                    <div className="text-sm text-gray-600">Memory</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-gray-900">
                      {dashboardData.system_metrics?.disk_usage || 0}%
                    </div>
                    <div className="text-sm text-gray-600">Disk</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-gray-900">
                      {dashboardData.system_metrics?.network_traffic || 0} MB
                    </div>
                    <div className="text-sm text-gray-600">Network</div>
                  </div>
                </div>
              ) : (
                <div className="text-center py-8">
                  <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
                  <p className="text-gray-600">Loading system metrics...</p>
                </div>
              )}
            </ChartCard>
          </div>
        )}

        {activeTab === 'services' && (
          <div className="space-y-6">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">Service Status</h2>
            {servicesLoading ? (
              <div className="text-center py-8">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
                <p className="mt-4 text-gray-600">Loading services status...</p>
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {servicesStatus?.services && Object.entries(servicesStatus.services).map(([service, status]) => (
                  <ServiceStatusCard
                    key={service}
                    service={service}
                    status={status as string}
                    port={getServicePort(service)}
                  />
                ))}
              </div>
            )}
          </div>
        )}

        {activeTab === 'analytics' && (
          <div className="space-y-6">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">Analytics</h2>
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <ChartCard title="Revenue Trends">
                <div className="h-64 bg-gray-50 rounded-lg flex items-center justify-center">
                  <p className="text-gray-500">Chart placeholder</p>
                </div>
              </ChartCard>
              <ChartCard title="User Growth">
                <div className="h-64 bg-gray-50 rounded-lg flex items-center justify-center">
                  <p className="text-gray-500">Chart placeholder</p>
                </div>
              </ChartCard>
            </div>
          </div>
        )}

        {activeTab === 'monitoring' && (
          <div className="space-y-6">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">System Monitoring</h2>
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <ChartCard title="Real-time Metrics">
                <div className="h-64 bg-gray-50 rounded-lg flex items-center justify-center">
                  <p className="text-gray-500">Monitoring dashboard</p>
                </div>
              </ChartCard>
              <ChartCard title="Logs">
                <div className="h-64 bg-gray-50 rounded-lg flex items-center justify-center">
                  <p className="text-gray-500">System logs</p>
                </div>
              </ChartCard>
            </div>
          </div>
        )}
      </div>
    </Layout>
  );
}

// Helper function
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
