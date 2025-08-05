import React, { useState, useEffect } from 'react';
import Head from 'next/head';
import {
  Building,
  Users,
  FileText,
  Upload,
  CheckCircle,
  AlertCircle,
  Clock,
  ArrowRight,
  ArrowLeft,
  Home,
  CreditCard,
  MapPin,
  Phone,
  Mail,
  Calendar,
  Camera as CameraIcon,
  Upload as UploadIcon,
  Download,
  Trash2,
  Edit,
  Save,
  X,
  Shield,
  TrendingUp,
  Star,
  Award,
  Crown,
  Briefcase,
  Globe,
  Zap,
  Target,
  BarChart3
} from 'lucide-react';

interface BusinessData {
  business_info: {
    business_name: string;
    business_type: string;
    registration_number: string;
    tax_id: string;
    industry: string;
    founded_date: string;
    employee_count: number;
    annual_revenue: number;
    website: string;
    phone: string;
    email: string;
    address: string;
    city: string;
    state: string;
    zip_code: string;
    country: string;
  };
  franchise_info: {
    is_franchise: boolean;
    franchise_name: string;
    franchise_type: string;
    franchise_number: string;
    parent_company: string;
    franchise_fee: number;
    royalty_fee: number;
    territory: string;
    start_date: string;
    contract_end_date: string;
  };
  documents: {
    business_license: {
      uploaded: boolean;
      verified: boolean;
      file_name: string;
      upload_date: string;
    };
    tax_certificate: {
      uploaded: boolean;
      verified: boolean;
      file_name: string;
      upload_date: string;
    };
    franchise_agreement: {
      uploaded: boolean;
      verified: boolean;
      file_name: string;
      upload_date: string;
    };
    financial_statements: {
      uploaded: boolean;
      verified: boolean;
      file_name: string;
      upload_date: string;
    };
  };
  verification_status: {
    business_verified: boolean;
    franchise_verified: boolean;
    documents_verified: boolean;
    financial_verified: boolean;
    overall_progress: number;
    status: string;
    sql_level_impact: string;
  };
}

export default function EMOSystem() {
  const [businessData, setBusinessData] = useState<BusinessData | null>(null);
  const [loading, setLoading] = useState(true);
  const [activeStep, setActiveStep] = useState(1);
  const [businessType, setBusinessType] = useState('business');

  // Mock business data
  const mockBusinessData: BusinessData = {
    business_info: {
      business_name: "Tech Solutions Pakistan",
      business_type: "Private Limited",
      registration_number: "REG-2024-001234",
      tax_id: "TAX-2024-567890",
      industry: "Technology",
      founded_date: "2020-03-15",
      employee_count: 25,
      annual_revenue: 5000000,
      website: "https://techsolutions.pk",
      phone: "+92 300 1234567",
      email: "info@techsolutions.pk",
      address: "123 Business Park",
      city: "Karachi",
      state: "Sindh",
      zip_code: "75000",
      country: "Pakistan"
    },
    franchise_info: {
      is_franchise: false,
      franchise_name: "",
      franchise_type: "",
      franchise_number: "",
      parent_company: "",
      franchise_fee: 0,
      royalty_fee: 0,
      territory: "",
      start_date: "",
      contract_end_date: ""
    },
    documents: {
      business_license: {
        uploaded: true,
        verified: true,
        file_name: "business_license_2024.pdf",
        upload_date: "2024-01-15"
      },
      tax_certificate: {
        uploaded: true,
        verified: true,
        file_name: "tax_certificate_2024.pdf",
        upload_date: "2024-01-16"
      },
      franchise_agreement: {
        uploaded: false,
        verified: false,
        file_name: "",
        upload_date: ""
      },
      financial_statements: {
        uploaded: false,
        verified: false,
        file_name: "",
        upload_date: ""
      }
    },
    verification_status: {
      business_verified: true,
      franchise_verified: false,
      documents_verified: false,
      financial_verified: false,
      overall_progress: 67,
      status: "in_progress",
      sql_level_impact: "Normal"
    }
  };

  useEffect(() => {
    // Simulate loading
    setTimeout(() => {
      setBusinessData(mockBusinessData);
      setLoading(false);
    }, 1000);
  }, []);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'verified': return 'text-green-600 bg-green-100';
      case 'pending': return 'text-yellow-600 bg-yellow-100';
      case 'failed': return 'text-red-600 bg-red-100';
      case 'in_progress': return 'text-blue-600 bg-blue-100';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  const getStatusIcon = (verified: boolean) => {
    return verified ? (
      <CheckCircle className="h-5 w-5 text-green-600" />
    ) : (
      <Clock className="h-5 w-5 text-yellow-600" />
    );
  };

  const handleFileUpload = (documentType: string) => {
    // Simulate file upload
    console.log(`Uploading ${documentType}`);
  };

  const handleEditField = (fieldName: string) => {
    console.log(`Editing ${fieldName}`);
  };

  const getSQLLevelBenefits = (level: string) => {
    switch (level) {
      case 'Normal':
        return [
          'Full service access',
          'Advanced features',
          'Premium support',
          'Earning opportunities',
          'Business analytics'
        ];
      case 'High':
        return [
          'VIP features',
          'Exclusive services',
          'High earning potential',
          'Priority access',
          'Custom solutions'
        ];
      default:
        return [];
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading EMO System...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Head>
        <title>EMO - Easy Management Office</title>
        <meta name="description" content="EHB Easy Management Office - Business & Franchise Verification" />
      </Head>

      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <Building className="h-8 w-8 text-indigo-600 mr-3" />
              <div className="text-2xl font-bold text-indigo-600">EMO</div>
              <span className="ml-2 text-sm text-gray-500">Easy Management Office</span>
            </div>

            <div className="flex items-center space-x-4">
              <a href="/pss" className="text-gray-600 hover:text-indigo-600">
                PSS
              </a>
              <a href="/sql-system" className="text-gray-600 hover:text-indigo-600">
                SQL System
              </a>
              <a href="/dashboard" className="text-gray-600 hover:text-indigo-600">
                Dashboard
              </a>
              <a href="/" className="text-gray-600 hover:text-indigo-600">
                Home
              </a>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Progress Header */}
        <div className="bg-white rounded-lg shadow-sm p-6 mb-8">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Business & Franchise Verification</h1>
              <p className="text-gray-600">Complete verification to upgrade your SQL level</p>
            </div>

            <div className="text-right">
              <div className="flex items-center space-x-2 mb-2">
                {getStatusIcon(businessData?.verification_status.overall_progress === 100)}
                <span className={`px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(businessData?.verification_status.status || '')}`}>
                  {businessData?.verification_status.status.replace('_', ' ').toUpperCase()}
                </span>
              </div>
              <div className="w-32 bg-gray-200 rounded-full h-2">
                <div
                  className="bg-indigo-600 h-2 rounded-full"
                  style={{ width: `${businessData?.verification_status.overall_progress || 0}%` }}
                ></div>
              </div>
              <span className="text-xs text-gray-500">{businessData?.verification_status.overall_progress}% Complete</span>
            </div>
          </div>
        </div>

        {/* Steps Navigation */}
        <div className="bg-white rounded-lg shadow-sm mb-8">
          <div className="border-b border-gray-200">
            <nav className="flex space-x-8 px-6">
              {[
                { id: 1, name: 'Business Info', icon: Building },
                { id: 2, name: 'Documents', icon: FileText },
                { id: 3, name: 'Verification', icon: Shield }
              ].map((step) => {
                const Icon = step.icon;
                const isActive = activeStep === step.id;
                const isCompleted = businessData && step.id < activeStep;

                return (
                  <button
                    key={step.id}
                    onClick={() => setActiveStep(step.id)}
                    className={`flex items-center space-x-2 py-4 px-1 border-b-2 font-medium text-sm ${
                      isActive
                        ? 'border-indigo-500 text-indigo-600'
                        : isCompleted
                        ? 'border-green-500 text-green-600'
                        : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                    }`}
                  >
                    <Icon className="h-4 w-4" />
                    <span>{step.name}</span>
                    {isCompleted && <CheckCircle className="h-4 w-4" />}
                  </button>
                );
              })}
            </nav>
          </div>
        </div>

        {/* Step Content */}
        <div className="bg-white rounded-lg shadow-sm p-6">
          {activeStep === 1 && (
            <div className="space-y-6">
              <h2 className="text-xl font-bold text-gray-900">Business Information</h2>

              {/* Business Type Selection */}
              <div className="bg-gray-50 rounded-lg p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Business Type</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <button
                    onClick={() => setBusinessType('business')}
                    className={`p-4 border rounded-lg text-left ${
                      businessType === 'business'
                        ? 'border-indigo-500 bg-indigo-50'
                        : 'border-gray-300 hover:border-gray-400'
                    }`}
                  >
                    <Building className="h-6 w-6 text-indigo-600 mb-2" />
                    <h4 className="font-semibold text-gray-900">Business</h4>
                    <p className="text-sm text-gray-600">Register your own business</p>
                  </button>

                  <button
                    onClick={() => setBusinessType('franchise')}
                    className={`p-4 border rounded-lg text-left ${
                      businessType === 'franchise'
                        ? 'border-indigo-500 bg-indigo-50'
                        : 'border-gray-300 hover:border-gray-400'
                    }`}
                  >
                    <Globe className="h-6 w-6 text-indigo-600 mb-2" />
                    <h4 className="font-semibold text-gray-900">Franchise</h4>
                    <p className="text-sm text-gray-600">Register a franchise business</p>
                  </button>
                </div>
              </div>

              {/* Business Information Form */}
              <div className="space-y-6">
                <h3 className="text-lg font-semibold text-gray-900">Business Details</h3>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Business Name</label>
                    <input
                      type="text"
                      value={businessData?.business_info.business_name}
                      onChange={(e) => console.log('Business name:', e.target.value)}
                      className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Business Type</label>
                    <select
                      value={businessData?.business_info.business_type}
                      onChange={(e) => console.log('Business type:', e.target.value)}
                      className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                    >
                      <option value="Private Limited">Private Limited</option>
                      <option value="Public Limited">Public Limited</option>
                      <option value="Sole Proprietorship">Sole Proprietorship</option>
                      <option value="Partnership">Partnership</option>
                      <option value="LLC">LLC</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Registration Number</label>
                    <input
                      type="text"
                      value={businessData?.business_info.registration_number}
                      onChange={(e) => console.log('Registration number:', e.target.value)}
                      className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Tax ID</label>
                    <input
                      type="text"
                      value={businessData?.business_info.tax_id}
                      onChange={(e) => console.log('Tax ID:', e.target.value)}
                      className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Industry</label>
                    <select
                      value={businessData?.business_info.industry}
                      onChange={(e) => console.log('Industry:', e.target.value)}
                      className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                    >
                      <option value="Technology">Technology</option>
                      <option value="Healthcare">Healthcare</option>
                      <option value="Finance">Finance</option>
                      <option value="Retail">Retail</option>
                      <option value="Manufacturing">Manufacturing</option>
                      <option value="Education">Education</option>
                      <option value="Other">Other</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Founded Date</label>
                    <input
                      type="date"
                      value={businessData?.business_info.founded_date}
                      onChange={(e) => console.log('Founded date:', e.target.value)}
                      className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Employee Count</label>
                    <input
                      type="number"
                      value={businessData?.business_info.employee_count}
                      onChange={(e) => console.log('Employee count:', e.target.value)}
                      className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Annual Revenue (PKR)</label>
                    <input
                      type="number"
                      value={businessData?.business_info.annual_revenue}
                      onChange={(e) => console.log('Annual revenue:', e.target.value)}
                      className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                    />
                  </div>
                </div>

                <div className="space-y-4">
                  <h4 className="text-lg font-semibold text-gray-900">Contact Information</h4>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">Website</label>
                      <input
                        type="url"
                        value={businessData?.business_info.website}
                        onChange={(e) => console.log('Website:', e.target.value)}
                        className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">Phone</label>
                      <input
                        type="tel"
                        value={businessData?.business_info.phone}
                        onChange={(e) => console.log('Phone:', e.target.value)}
                        className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">Email</label>
                      <input
                        type="email"
                        value={businessData?.business_info.email}
                        onChange={(e) => console.log('Email:', e.target.value)}
                        className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                      />
                    </div>
                  </div>
                </div>

                <div className="space-y-4">
                  <h4 className="text-lg font-semibold text-gray-900">Address</h4>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="md:col-span-2">
                      <label className="block text-sm font-medium text-gray-700 mb-2">Street Address</label>
                      <input
                        type="text"
                        value={businessData?.business_info.address}
                        onChange={(e) => console.log('Address:', e.target.value)}
                        className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">City</label>
                      <input
                        type="text"
                        value={businessData?.business_info.city}
                        onChange={(e) => console.log('City:', e.target.value)}
                        className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">State/Province</label>
                      <input
                        type="text"
                        value={businessData?.business_info.state}
                        onChange={(e) => console.log('State:', e.target.value)}
                        className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">ZIP/Postal Code</label>
                      <input
                        type="text"
                        value={businessData?.business_info.zip_code}
                        onChange={(e) => console.log('ZIP:', e.target.value)}
                        className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-2">Country</label>
                      <input
                        type="text"
                        value={businessData?.business_info.country}
                        onChange={(e) => console.log('Country:', e.target.value)}
                        className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                      />
                    </div>
                  </div>
                </div>
              </div>

              <div className="flex justify-end space-x-4">
                <button
                  onClick={() => setActiveStep(2)}
                  className="px-6 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 flex items-center space-x-2"
                >
                  <span>Next</span>
                  <ArrowRight className="h-4 w-4" />
                </button>
              </div>
            </div>
          )}

          {activeStep === 2 && (
            <div className="space-y-6">
              <h2 className="text-xl font-bold text-gray-900">Document Upload</h2>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* Business License */}
                <div className="border border-gray-200 rounded-lg p-6">
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-lg font-semibold text-gray-900">Business License</h3>
                    {getStatusIcon(businessData?.documents.business_license.verified || false)}
                  </div>

                  {businessData?.documents.business_license.uploaded ? (
                    <div className="space-y-3">
                      <div className="flex items-center space-x-2">
                        <FileText className="h-5 w-5 text-green-600" />
                        <span className="text-sm text-gray-600">{businessData.documents.business_license.file_name}</span>
                      </div>
                      <p className="text-xs text-gray-500">Uploaded: {businessData.documents.business_license.upload_date}</p>
                      <div className="flex space-x-2">
                        <button className="px-3 py-1 bg-blue-600 text-white rounded text-sm hover:bg-blue-700">
                          View
                        </button>
                        <button className="px-3 py-1 border border-gray-300 rounded text-sm hover:bg-gray-50">
                          Replace
                        </button>
                      </div>
                    </div>
                  ) : (
                    <div className="space-y-4">
                      <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center">
                        <UploadIcon className="h-8 w-8 text-gray-400 mx-auto mb-2" />
                        <p className="text-sm text-gray-600">Upload Business License</p>
                        <p className="text-xs text-gray-500">PDF, JPG, PNG (Max 5MB)</p>
                      </div>
                      <button
                        onClick={() => handleFileUpload('business_license')}
                        className="w-full px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700"
                      >
                        Choose File
                      </button>
                    </div>
                  )}
                </div>

                {/* Tax Certificate */}
                <div className="border border-gray-200 rounded-lg p-6">
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-lg font-semibold text-gray-900">Tax Certificate</h3>
                    {getStatusIcon(businessData?.documents.tax_certificate.verified || false)}
                  </div>

                  {businessData?.documents.tax_certificate.uploaded ? (
                    <div className="space-y-3">
                      <div className="flex items-center space-x-2">
                        <FileText className="h-5 w-5 text-green-600" />
                        <span className="text-sm text-gray-600">{businessData.documents.tax_certificate.file_name}</span>
                      </div>
                      <p className="text-xs text-gray-500">Uploaded: {businessData.documents.tax_certificate.upload_date}</p>
                      <div className="flex space-x-2">
                        <button className="px-3 py-1 bg-blue-600 text-white rounded text-sm hover:bg-blue-700">
                          View
                        </button>
                        <button className="px-3 py-1 border border-gray-300 rounded text-sm hover:bg-gray-50">
                          Replace
                        </button>
                      </div>
                    </div>
                  ) : (
                    <div className="space-y-4">
                      <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center">
                        <UploadIcon className="h-8 w-8 text-gray-400 mx-auto mb-2" />
                        <p className="text-sm text-gray-600">Upload Tax Certificate</p>
                        <p className="text-xs text-gray-500">PDF, JPG, PNG (Max 5MB)</p>
                      </div>
                      <button
                        onClick={() => handleFileUpload('tax_certificate')}
                        className="w-full px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700"
                      >
                        Choose File
                      </button>
                    </div>
                  )}
                </div>

                {/* Franchise Agreement */}
                <div className="border border-gray-200 rounded-lg p-6">
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-lg font-semibold text-gray-900">Franchise Agreement</h3>
                    {getStatusIcon(businessData?.documents.franchise_agreement.verified || false)}
                  </div>

                  {businessData?.documents.franchise_agreement.uploaded ? (
                    <div className="space-y-3">
                      <div className="flex items-center space-x-2">
                        <FileText className="h-5 w-5 text-green-600" />
                        <span className="text-sm text-gray-600">{businessData.documents.franchise_agreement.file_name}</span>
                      </div>
                      <p className="text-xs text-gray-500">Uploaded: {businessData.documents.franchise_agreement.upload_date}</p>
                      <div className="flex space-x-2">
                        <button className="px-3 py-1 bg-blue-600 text-white rounded text-sm hover:bg-blue-700">
                          View
                        </button>
                        <button className="px-3 py-1 border border-gray-300 rounded text-sm hover:bg-gray-50">
                          Replace
                        </button>
                      </div>
                    </div>
                  ) : (
                    <div className="space-y-4">
                      <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center">
                        <UploadIcon className="h-8 w-8 text-gray-400 mx-auto mb-2" />
                        <p className="text-sm text-gray-600">Upload Franchise Agreement</p>
                        <p className="text-xs text-gray-500">PDF only (Max 10MB)</p>
                      </div>
                      <button
                        onClick={() => handleFileUpload('franchise_agreement')}
                        className="w-full px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700"
                      >
                        Choose File
                      </button>
                    </div>
                  )}
                </div>

                {/* Financial Statements */}
                <div className="border border-gray-200 rounded-lg p-6">
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-lg font-semibold text-gray-900">Financial Statements</h3>
                    {getStatusIcon(businessData?.documents.financial_statements.verified || false)}
                  </div>

                  {businessData?.documents.financial_statements.uploaded ? (
                    <div className="space-y-3">
                      <div className="flex items-center space-x-2">
                        <FileText className="h-5 w-5 text-green-600" />
                        <span className="text-sm text-gray-600">{businessData.documents.financial_statements.file_name}</span>
                      </div>
                      <p className="text-xs text-gray-500">Uploaded: {businessData.documents.financial_statements.upload_date}</p>
                      <div className="flex space-x-2">
                        <button className="px-3 py-1 bg-blue-600 text-white rounded text-sm hover:bg-blue-700">
                          View
                        </button>
                        <button className="px-3 py-1 border border-gray-300 rounded text-sm hover:bg-gray-50">
                          Replace
                        </button>
                      </div>
                    </div>
                  ) : (
                    <div className="space-y-4">
                      <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center">
                        <UploadIcon className="h-8 w-8 text-gray-400 mx-auto mb-2" />
                        <p className="text-sm text-gray-600">Upload Financial Statements</p>
                        <p className="text-xs text-gray-500">PDF, Excel (Max 10MB)</p>
                      </div>
                      <button
                        onClick={() => handleFileUpload('financial_statements')}
                        className="w-full px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700"
                      >
                        Choose File
                      </button>
                    </div>
                  )}
                </div>
              </div>

              <div className="flex justify-between space-x-4">
                <button
                  onClick={() => setActiveStep(1)}
                  className="px-6 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 flex items-center space-x-2"
                >
                  <ArrowLeft className="h-4 w-4" />
                  <span>Previous</span>
                </button>
                <button
                  onClick={() => setActiveStep(3)}
                  className="px-6 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 flex items-center space-x-2"
                >
                  <span>Next</span>
                  <ArrowRight className="h-4 w-4" />
                </button>
              </div>
            </div>
          )}

          {activeStep === 3 && (
            <div className="space-y-6">
              <h2 className="text-xl font-bold text-gray-900">Verification Status</h2>

              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Verification Summary */}
                <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
                  <div className="flex items-center space-x-3 mb-4">
                    <Shield className="h-6 w-6 text-blue-600" />
                    <h3 className="text-lg font-semibold text-blue-900">Verification Summary</h3>
                  </div>

                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-blue-700">Business Verification</span>
                      {getStatusIcon(businessData?.verification_status.business_verified || false)}
                    </div>

                    <div className="flex items-center justify-between">
                      <span className="text-sm text-blue-700">Franchise Verification</span>
                      {getStatusIcon(businessData?.verification_status.franchise_verified || false)}
                    </div>

                    <div className="flex items-center justify-between">
                      <span className="text-sm text-blue-700">Documents Verification</span>
                      {getStatusIcon(businessData?.verification_status.documents_verified || false)}
                    </div>

                    <div className="flex items-center justify-between">
                      <span className="text-sm text-blue-700">Financial Verification</span>
                      {getStatusIcon(businessData?.verification_status.financial_verified || false)}
                    </div>

                    <div className="pt-4 border-t border-blue-200">
                      <div className="flex items-center justify-between">
                        <span className="text-sm font-medium text-blue-700">Overall Progress</span>
                        <span className="text-sm font-medium text-blue-900">{businessData?.verification_status.overall_progress}%</span>
                      </div>
                      <div className="w-full bg-blue-200 rounded-full h-2 mt-2">
                        <div
                          className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                          style={{ width: `${businessData?.verification_status.overall_progress || 0}%` }}
                        ></div>
                      </div>
                    </div>
                  </div>
                </div>

                {/* SQL Level Impact */}
                <div className="bg-green-50 border border-green-200 rounded-lg p-6">
                  <div className="flex items-center space-x-3 mb-4">
                    <TrendingUp className="h-6 w-6 text-green-600" />
                    <h3 className="text-lg font-semibold text-green-900">SQL Level Impact</h3>
                  </div>

                  <div className="space-y-4">
                    <div className="flex items-center space-x-3">
                      <Building className="h-5 w-5 text-gray-400" />
                      <div>
                        <p className="text-sm font-medium text-gray-700">Current Level: Normal</p>
                        <p className="text-xs text-gray-500">Enhanced access & features</p>
                      </div>
                    </div>

                    <div className="flex items-center space-x-3">
                      <Award className="h-5 w-5 text-green-600" />
                      <div>
                        <p className="text-sm font-medium text-gray-700">After Verification: {businessData?.verification_status.sql_level_impact}</p>
                        <p className="text-xs text-gray-500">Advanced features & benefits</p>
                      </div>
                    </div>

                    <div className="pt-4 border-t border-green-200">
                      <h4 className="text-sm font-medium text-green-700 mb-2">Benefits Unlocked:</h4>
                      <ul className="space-y-1 text-xs text-gray-600">
                        {getSQLLevelBenefits(businessData?.verification_status.sql_level_impact || '').map((benefit, index) => (
                          <li key={index}>• {benefit}</li>
                        ))}
                      </ul>
                    </div>
                  </div>
                </div>
              </div>

              <div className="flex justify-between space-x-4">
                <button
                  onClick={() => setActiveStep(2)}
                  className="px-6 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 flex items-center space-x-2"
                >
                  <ArrowLeft className="h-4 w-4" />
                  <span>Previous</span>
                </button>
                <button
                  className="px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 flex items-center space-x-2"
                >
                  <span>Submit for Verification</span>
                  <ArrowRight className="h-4 w-4" />
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
