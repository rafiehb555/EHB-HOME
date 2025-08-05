import { useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/router';
import {
  LayoutDashboard,
  Users,
  Settings,
  BarChart3,
  ShoppingCart,
  Wallet,
  Shield,
  Building,
  Brain,
  Bot,
  LogOut,
  Menu,
  X
} from 'lucide-react';

interface SidebarProps {
  isOpen: boolean;
  onToggle: () => void;
}

const Sidebar = ({ isOpen, onToggle }: SidebarProps) => {
  const router = useRouter();
  const [collapsed, setCollapsed] = useState(false);

  const menuItems = [
    {
      title: 'Dashboard',
      icon: LayoutDashboard,
      href: '/admin',
      color: 'text-blue-600'
    },
    {
      title: 'User Management',
      icon: Users,
      href: '/admin/users',
      color: 'text-green-600'
    },
    {
      title: 'Services',
      icon: Settings,
      href: '/admin/services',
      color: 'text-purple-600'
    },
    {
      title: 'Analytics',
      icon: BarChart3,
      href: '/admin/analytics',
      color: 'text-orange-600'
    }
  ];

  const serviceItems = [
    {
      title: 'GoSellr',
      icon: ShoppingCart,
      href: '/admin/services/gosellr',
      color: 'text-blue-600'
    },
    {
      title: 'Wallet',
      icon: Wallet,
      href: '/admin/services/wallet',
      color: 'text-green-600'
    },
    {
      title: 'PSS',
      icon: Shield,
      href: '/admin/services/pss',
      color: 'text-red-600'
    },
    {
      title: 'EMO',
      icon: Building,
      href: '/admin/services/emo',
      color: 'text-purple-600'
    },
    {
      title: 'EDR',
      icon: Brain,
      href: '/admin/services/edr',
      color: 'text-indigo-600'
    },
    {
      title: 'AI Agent',
      icon: Bot,
      href: '/admin/services/ai-agent',
      color: 'text-pink-600'
    }
  ];

  const isActive = (href: string) => router.pathname === href;

  return (
    <>
      {/* Mobile Overlay */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-black bg-opacity-50 z-40 lg:hidden"
          onClick={onToggle}
        />
      )}

      {/* Sidebar */}
      <div
        className={`fixed top-0 left-0 h-full bg-white shadow-lg z-50 transition-transform duration-300 ease-in-out ${
          isOpen ? 'translate-x-0' : '-translate-x-full'
        } lg:translate-x-0 lg:static lg:z-auto w-64`}
      >
        <div className="flex flex-col h-full">
          {/* Header */}
          <div className="flex items-center justify-between p-4 border-b border-gray-200">
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-sm">E</span>
              </div>
              <span className="font-semibold text-gray-900">EHB Admin</span>
            </div>
            <button
              onClick={() => setCollapsed(!collapsed)}
              className="hidden lg:block p-1 rounded-md hover:bg-gray-100"
            >
              {collapsed ? <Menu className="h-4 w-4" /> : <X className="h-4 w-4" />}
            </button>
            <button
              onClick={onToggle}
              className="lg:hidden p-1 rounded-md hover:bg-gray-100"
            >
              <X className="h-4 w-4" />
            </button>
          </div>

          {/* Navigation */}
          <nav className="flex-1 overflow-y-auto p-4">
            {/* Main Menu */}
            <div className="mb-6">
              <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-3">
                Main Menu
              </h3>
              <ul className="space-y-1">
                {menuItems.map((item) => {
                  const Icon = item.icon;
                  return (
                    <li key={item.href}>
                      <Link
                        href={item.href}
                        className={`flex items-center space-x-3 px-3 py-2 rounded-lg transition-colors duration-200 ${
                          isActive(item.href)
                            ? 'bg-blue-50 text-blue-700 border-r-2 border-blue-700'
                            : 'text-gray-700 hover:bg-gray-50'
                        }`}
                      >
                        <Icon className={`h-5 w-5 ${item.color}`} />
                        <span className="font-medium">{item.title}</span>
                      </Link>
                    </li>
                  );
                })}
              </ul>
            </div>

            {/* Services */}
            <div className="mb-6">
              <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-3">
                Services
              </h3>
              <ul className="space-y-1">
                {serviceItems.map((item) => {
                  const Icon = item.icon;
                  return (
                    <li key={item.href}>
                      <Link
                        href={item.href}
                        className={`flex items-center space-x-3 px-3 py-2 rounded-lg transition-colors duration-200 ${
                          isActive(item.href)
                            ? 'bg-blue-50 text-blue-700 border-r-2 border-blue-700'
                            : 'text-gray-700 hover:bg-gray-50'
                        }`}
                      >
                        <Icon className={`h-5 w-5 ${item.color}`} />
                        <span className="font-medium">{item.title}</span>
                      </Link>
                    </li>
                  );
                })}
              </ul>
            </div>

            {/* Quick Stats */}
            <div className="bg-gray-50 rounded-lg p-4 mb-6">
              <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-3">
                Quick Stats
              </h3>
              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span className="text-gray-600">Total Users</span>
                  <span className="font-semibold text-gray-900">1,250</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-gray-600">Active Services</span>
                  <span className="font-semibold text-green-600">8/8</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span className="text-gray-600">Revenue Today</span>
                  <span className="font-semibold text-green-600">$12,500</span>
                </div>
              </div>
            </div>
          </nav>

          {/* Footer */}
          <div className="p-4 border-t border-gray-200">
            <button className="flex items-center space-x-3 w-full px-3 py-2 text-gray-700 hover:bg-gray-50 rounded-lg transition-colors duration-200">
              <LogOut className="h-5 w-5 text-red-600" />
              <span className="font-medium">Logout</span>
            </button>
          </div>
        </div>
      </div>
    </>
  );
};

export default Sidebar;
