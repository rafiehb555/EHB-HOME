import { useState, useEffect } from 'react';
import Head from 'next/head';
import { useAuth } from '@/hooks/useAuth';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import ServiceCard from '@/components/services/ServiceCard';
import {
  Activity,
  CheckCircle,
  Clock,
  AlertCircle,
  RefreshCw,
  TrendingUp
} from 'lucide-react';
import toast from 'react-hot-toast';

interface Service {
  name: string;
  display_name: string;
  url: string;
  description: string;
  status?: 'ready' | 'pending' | 'error';
  verification_status?: 'verified' | 'pending' | 'failed';
  score?: number;
}

const ServicesPage = () => {
  const { user } = useAuth();
  const [services, setServices] = useState<Service[]>([]);
  const [loading, setLoading] = useState(true);
  const [verificationStatus, setVerificationStatus] = useState<any>(null);

  useEffect(() => {
    fetchServices();
    if (user) {
      fetchVerificationStatus();
    }
  }, [user]);

  const fetchServices = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/v1/services/available-services');
      if (response.ok) {
        const data = await response.json();
        setServices(data.services);
      }
    } catch (error) {
      console.error('Error fetching services:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchVerificationStatus = async () => {
    if (!user) return;

    try {
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
    }
  };

  const handleVerify = async (serviceName: string) => {
    if (!user) return;

    try {
      const token = localStorage.getItem('token');
      const verificationData = getVerificationData(serviceName);

      const response = await fetch(`http://localhost:8000/api/v1/services/${serviceName}/verify`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(verificationData)
      });

      if (response.ok) {
        const result = await response.json();
        toast.success(`Verification submitted for ${serviceName}`);
        fetchVerificationStatus(); // Refresh status
      } else {
        toast.error('Verification failed');
      }
    } catch (error) {
      console.error('Error during verification:', error);
      toast.error('Verification failed');
    }
  };

  const getVerificationData = (serviceName: string) => {
    switch (serviceName) {
      case 'pss':
        return {
          document_type: 'id_card',
          document_data: 'mock_document_data',
          verification_method: 'document_upload'
        };
      case 'emo':
        return {
          business_name: 'Sample Business',
          business_type: 'technology',
          license_number: 'BL-2024-001',
          tax_id: 'TAX-001',
          documents: ['business_license.pdf', 'tax_certificate.pdf']
        };
      case 'edr':
        return {
          exam_name: 'Professional Certification',
          exam_type: 'certification',
          exam_date: '2024-03-15',
          exam_center: 'Tech Center A',
          registration_fee: 150.00
        };
      default:
        return {};
    }
  };

  const handleViewDetails = (serviceName: string) => {
    // Navigate to service details page
    window.open(`http://localhost:${getServicePort(serviceName)}`, '_blank');
  };

  const getServicePort = (serviceName: string) => {
    const ports = {
      'pss': 4001,
      'emo': 4003,
      'edr': 4002,
      'jps': 4005,
      'gosellr': 4004,
      'wallet': 5001,
      'ai-agent': 4007,
      'ai-robot': 4008
    };
    return ports[serviceName as keyof typeof ports] || 8000;
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

  const getServiceWithStatus = (service: Service) => {
    if (!verificationStatus?.verification_status) return service;

    const status = verificationStatus.verification_status[service.name];
    if (status) {
      return {
        ...service,
        verification_status: status.status,
        score: status.score
      };
    }
    return service;
  };

  if (loading) {
    return (
      <ProtectedRoute>
        <div className="min-h-screen bg-gray-50 flex items-center justify-center">
          <div className="text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
            <p className="mt-4 text-gray-600">Loading services...</p>
          </div>
        </div>
      </ProtectedRoute>
    );
  }

  return (
    <ProtectedRoute>
      <Head>
        <title>Services - EHB Technologies</title>
        <meta name="description" content="EHB Services Dashboard" />
      </Head>

      <div className="min-h-screen bg-gray-50">
        {/* Header */}
        <header className="bg-white shadow-sm border-b border-gray-200">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center py-4">
              <div>
                <h1 className="text-2xl font-semibold text-gray-900">EHB Services</h1>
                <p className="text-sm text-gray-600">Manage your service verifications</p>
              </div>
              <button
                onClick={() => {
                  fetchServices();
                  fetchVerificationStatus();
                }}
                className="flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
              >
                <RefreshCw className="h-4 w-4" />
                <span>Refresh</span>
              </button>
            </div>
          </div>
        </header>

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {/* Progress Overview */}
          {verificationStatus && (
            <div className="mb-8">
              <div className="bg-white rounded-lg shadow p-6">
                <div className="flex items-center justify-between mb-4">
                  <h2 className="text-lg font-semibold text-gray-900">Verification Progress</h2>
                  <div className="flex items-center space-x-4">
                    <div className="flex items-center space-x-2">
                      <CheckCircle className="h-4 w-4 text-green-600" />
                      <span className="text-sm text-gray-600">
                        {getVerifiedCount()} of {getTotalServices()} verified
                      </span>
                    </div>
                    <div className="text-2xl font-bold text-blue-600">
                      {Math.round(getOverallProgress())}%
                    </div>
                  </div>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-3">
                  <div
                    className="bg-blue-600 h-3 rounded-full transition-all duration-300"
                    style={{ width: `${getOverallProgress()}%` }}
                  ></div>
                </div>
              </div>
            </div>
          )}

          {/* Services Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {services.map((service) => (
              <ServiceCard
                key={service.name}
                service={getServiceWithStatus(service)}
                onVerify={handleVerify}
                onViewDetails={handleViewDetails}
              />
            ))}
          </div>

          {/* Service Status Summary */}
          <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="bg-white rounded-lg shadow p-6">
              <div className="flex items-center">
                <div className="p-2 bg-green-100 rounded-lg">
                  <CheckCircle className="h-6 w-6 text-green-600" />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">Verified Services</p>
                  <p className="text-2xl font-semibold text-gray-900">{getVerifiedCount()}</p>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-lg shadow p-6">
              <div className="flex items-center">
                <div className="p-2 bg-yellow-100 rounded-lg">
                  <Clock className="h-6 w-6 text-yellow-600" />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">Pending Services</p>
                  <p className="text-2xl font-semibold text-gray-900">
                    {getTotalServices() - getVerifiedCount()}
                  </p>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-lg shadow p-6">
              <div className="flex items-center">
                <div className="p-2 bg-blue-100 rounded-lg">
                  <TrendingUp className="h-6 w-6 text-blue-600" />
                </div>
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">Overall Progress</p>
                  <p className="text-2xl font-semibold text-gray-900">
                    {Math.round(getOverallProgress())}%
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </ProtectedRoute>
  );
};

export default ServicesPage;
