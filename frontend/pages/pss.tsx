import React, { useState, useEffect } from 'react';
import Head from 'next/head';
import {
  Shield,
  User,
  FileText,
  Camera,
  Upload,
  CheckCircle,
  AlertCircle,
  Clock,
  Lock,
  Unlock,
  Eye,
  EyeOff,
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
  X
} from 'lucide-react';

interface KYCData {
  personal_info: {
    full_name: string;
    date_of_birth: string;
    nationality: string;
    phone: string;
    email: string;
    address: string;
    city: string;
    state: string;
    zip_code: string;
    country: string;
  };
  documents: {
    id_card: {
      uploaded: boolean;
      verified: boolean;
      file_name: string;
      upload_date: string;
    };
    passport: {
      uploaded: boolean;
      verified: boolean;
      file_name: string;
      upload_date: string;
    };
    proof_of_address: {
      uploaded: boolean;
      verified: boolean;
      file_name: string;
      upload_date: string;
    };
  };
  verification_status: {
    personal_info_verified: boolean;
    documents_verified: boolean;
    address_verified: boolean;
    overall_progress: number;
    status: string;
  };
}

export default function PSSSystem() {
  const [kycData, setKycData] = useState<KYCData | null>(null);
  const [loading, setLoading] = useState(true);
  const [activeStep, setActiveStep] = useState(1);
  const [showPassword, setShowPassword] = useState(false);
  const [editingField, setEditingField] = useState<string | null>(null);

  // Mock KYC data
  const mockKycData: KYCData = {
    personal_info: {
      full_name: "John Doe",
      date_of_birth: "1990-05-15",
      nationality: "Pakistani",
      phone: "+92 300 1234567",
      email: "john.doe@example.com",
      address: "123 Main Street",
      city: "Karachi",
      state: "Sindh",
      zip_code: "75000",
      country: "Pakistan"
    },
    documents: {
      id_card: {
        uploaded: true,
        verified: true,
        file_name: "id_card_front_back.jpg",
        upload_date: "2024-01-15"
      },
      passport: {
        uploaded: true,
        verified: true,
        file_name: "passport_scan.pdf",
        upload_date: "2024-01-16"
      },
      proof_of_address: {
        uploaded: false,
        verified: false,
        file_name: "",
        upload_date: ""
      }
    },
    verification_status: {
      personal_info_verified: true,
      documents_verified: false,
      address_verified: false,
      overall_progress: 67,
      status: "in_progress"
    }
  };

  useEffect(() => {
    // Simulate loading
    setTimeout(() => {
      setKycData(mockKycData);
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
    setEditingField(fieldName);
  };

  const handleSaveField = (fieldName: string, value: string) => {
    if (kycData) {
      setKycData({
        ...kycData,
        personal_info: {
          ...kycData.personal_info,
          [fieldName]: value
        }
      });
    }
    setEditingField(null);
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading PSS System...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Head>
        <title>PSS - Personal Security System</title>
        <meta name="description" content="EHB Personal Security System - Identity Verification" />
      </Head>

      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <Shield className="h-8 w-8 text-indigo-600 mr-3" />
              <div className="text-2xl font-bold text-indigo-600">PSS</div>
              <span className="ml-2 text-sm text-gray-500">Personal Security System</span>
            </div>

            <div className="flex items-center space-x-4">
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
              <h1 className="text-2xl font-bold text-gray-900">Identity Verification (KYC)</h1>
              <p className="text-gray-600">Complete verification to upgrade your SQL level</p>
            </div>

            <div className="text-right">
              <div className="flex items-center space-x-2 mb-2">
                {getStatusIcon(kycData?.verification_status.overall_progress === 100)}
                <span className={`px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(kycData?.verification_status.status || '')}`}>
                  {kycData?.verification_status.status.replace('_', ' ').toUpperCase()}
                </span>
              </div>
              <div className="w-32 bg-gray-200 rounded-full h-2">
                <div
                  className="bg-indigo-600 h-2 rounded-full"
                  style={{ width: `${kycData?.verification_status.overall_progress || 0}%` }}
                ></div>
              </div>
              <span className="text-xs text-gray-500">{kycData?.verification_status.overall_progress}% Complete</span>
            </div>
          </div>
        </div>

        {/* Steps Navigation */}
        <div className="bg-white rounded-lg shadow-sm mb-8">
          <div className="border-b border-gray-200">
            <nav className="flex space-x-8 px-6">
              {[
                { id: 1, name: 'Personal Info', icon: User },
                { id: 2, name: 'Documents', icon: FileText },
                { id: 3, name: 'Verification', icon: Shield }
              ].map((step) => {
                const Icon = step.icon;
                const isActive = activeStep === step.id;
                const isCompleted = kycData && step.id < activeStep;

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
              <h2 className="text-xl font-bold text-gray-900">Personal Information</h2>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Full Name</label>
                  <div className="flex items-center space-x-2">
                    <input
                      type="text"
                      value={kycData?.personal_info.full_name}
                      onChange={(e) => handleSaveField('full_name', e.target.value)}
                      className="flex-1 border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                    />
                    <button
                      onClick={() => handleEditField('full_name')}
                      className="text-gray-400 hover:text-gray-600"
                    >
                      <Edit className="h-4 w-4" />
                    </button>
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Date of Birth</label>
                  <input
                    type="date"
                    value={kycData?.personal_info.date_of_birth}
                    onChange={(e) => handleSaveField('date_of_birth', e.target.value)}
                    className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Nationality</label>
                  <input
                    type="text"
                    value={kycData?.personal_info.nationality}
                    onChange={(e) => handleSaveField('nationality', e.target.value)}
                    className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Phone Number</label>
                  <div className="flex items-center space-x-2">
                    <Phone className="h-4 w-4 text-gray-400" />
                    <input
                      type="tel"
                      value={kycData?.personal_info.phone}
                      onChange={(e) => handleSaveField('phone', e.target.value)}
                      className="flex-1 border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Email Address</label>
                  <div className="flex items-center space-x-2">
                    <Mail className="h-4 w-4 text-gray-400" />
                    <input
                      type="email"
                      value={kycData?.personal_info.email}
                      onChange={(e) => handleSaveField('email', e.target.value)}
                      className="flex-1 border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">Country</label>
                  <input
                    type="text"
                    value={kycData?.personal_info.country}
                    onChange={(e) => handleSaveField('country', e.target.value)}
                    className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  />
                </div>
              </div>

              <div className="space-y-4">
                <h3 className="text-lg font-semibold text-gray-900">Address Information</h3>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">Street Address</label>
                    <div className="flex items-center space-x-2">
                      <MapPin className="h-4 w-4 text-gray-400" />
                      <input
                        type="text"
                        value={kycData?.personal_info.address}
                        onChange={(e) => handleSaveField('address', e.target.value)}
                        className="flex-1 border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                      />
                    </div>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">City</label>
                    <input
                      type="text"
                      value={kycData?.personal_info.city}
                      onChange={(e) => handleSaveField('city', e.target.value)}
                      className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">State/Province</label>
                    <input
                      type="text"
                      value={kycData?.personal_info.state}
                      onChange={(e) => handleSaveField('state', e.target.value)}
                      className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">ZIP/Postal Code</label>
                    <input
                      type="text"
                      value={kycData?.personal_info.zip_code}
                      onChange={(e) => handleSaveField('zip_code', e.target.value)}
                      className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                    />
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

              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {/* ID Card */}
                <div className="border border-gray-200 rounded-lg p-6">
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-lg font-semibold text-gray-900">ID Card</h3>
                    {getStatusIcon(kycData?.documents.id_card.verified || false)}
                  </div>

                  {kycData?.documents.id_card.uploaded ? (
                    <div className="space-y-3">
                      <div className="flex items-center space-x-2">
                        <FileText className="h-5 w-5 text-green-600" />
                        <span className="text-sm text-gray-600">{kycData.documents.id_card.file_name}</span>
                      </div>
                      <p className="text-xs text-gray-500">Uploaded: {kycData.documents.id_card.upload_date}</p>
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
                        <p className="text-sm text-gray-600">Upload ID Card</p>
                        <p className="text-xs text-gray-500">JPG, PNG, PDF (Max 5MB)</p>
                      </div>
                      <button
                        onClick={() => handleFileUpload('id_card')}
                        className="w-full px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700"
                      >
                        Choose File
                      </button>
                    </div>
                  )}
                </div>

                {/* Passport */}
                <div className="border border-gray-200 rounded-lg p-6">
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-lg font-semibold text-gray-900">Passport</h3>
                    {getStatusIcon(kycData?.documents.passport.verified || false)}
                  </div>

                  {kycData?.documents.passport.uploaded ? (
                    <div className="space-y-3">
                      <div className="flex items-center space-x-2">
                        <FileText className="h-5 w-5 text-green-600" />
                        <span className="text-sm text-gray-600">{kycData.documents.passport.file_name}</span>
                      </div>
                      <p className="text-xs text-gray-500">Uploaded: {kycData.documents.passport.upload_date}</p>
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
                        <p className="text-sm text-gray-600">Upload Passport</p>
                        <p className="text-xs text-gray-500">JPG, PNG, PDF (Max 5MB)</p>
                      </div>
                      <button
                        onClick={() => handleFileUpload('passport')}
                        className="w-full px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700"
                      >
                        Choose File
                      </button>
                    </div>
                  )}
                </div>

                {/* Proof of Address */}
                <div className="border border-gray-200 rounded-lg p-6">
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-lg font-semibold text-gray-900">Proof of Address</h3>
                    {getStatusIcon(kycData?.documents.proof_of_address.verified || false)}
                  </div>

                  {kycData?.documents.proof_of_address.uploaded ? (
                    <div className="space-y-3">
                      <div className="flex items-center space-x-2">
                        <FileText className="h-5 w-5 text-green-600" />
                        <span className="text-sm text-gray-600">{kycData.documents.proof_of_address.file_name}</span>
                      </div>
                      <p className="text-xs text-gray-500">Uploaded: {kycData.documents.proof_of_address.upload_date}</p>
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
                        <p className="text-sm text-gray-600">Upload Proof of Address</p>
                        <p className="text-xs text-gray-500">Utility bill, bank statement (Max 5MB)</p>
                      </div>
                      <button
                        onClick={() => handleFileUpload('proof_of_address')}
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

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* Verification Summary */}
                <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
                  <div className="flex items-center space-x-3 mb-4">
                    <Shield className="h-6 w-6 text-blue-600" />
                    <h3 className="text-lg font-semibold text-blue-900">Verification Summary</h3>
                  </div>

                  <div className="space-y-4">
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-blue-700">Personal Information</span>
                      {getStatusIcon(kycData?.verification_status.personal_info_verified || false)}
                    </div>

                    <div className="flex items-center justify-between">
                      <span className="text-sm text-blue-700">Documents Verification</span>
                      {getStatusIcon(kycData?.verification_status.documents_verified || false)}
                    </div>

                    <div className="flex items-center justify-between">
                      <span className="text-sm text-blue-700">Address Verification</span>
                      {getStatusIcon(kycData?.verification_status.address_verified || false)}
                    </div>

                    <div className="pt-4 border-t border-blue-200">
                      <div className="flex items-center justify-between">
                        <span className="text-sm font-medium text-blue-700">Overall Progress</span>
                        <span className="text-sm font-medium text-blue-900">{kycData?.verification_status.overall_progress}%</span>
                      </div>
                      <div className="w-full bg-blue-200 rounded-full h-2 mt-2">
                        <div
                          className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                          style={{ width: `${kycData?.verification_status.overall_progress || 0}%` }}
                        ></div>
                      </div>
                    </div>
                  </div>
                </div>

                {/* SQL Level Impact */}
                <div className="bg-green-50 border border-green-200 rounded-lg p-6">
                  <div className="flex items-center space-x-3 mb-4">
                    <User className="h-6 w-6 text-green-600" />
                    <h3 className="text-lg font-semibold text-green-900">SQL Level Impact</h3>
                  </div>

                  <div className="space-y-4">
                    <div className="flex items-center space-x-3">
                      <Lock className="h-5 w-5 text-gray-400" />
                      <div>
                        <p className="text-sm font-medium text-gray-700">Current Level: Free</p>
                        <p className="text-xs text-gray-500">Basic access only</p>
                      </div>
                    </div>

                    <div className="flex items-center space-x-3">
                      <Unlock className="h-5 w-5 text-green-600" />
                      <div>
                        <p className="text-sm font-medium text-gray-700">After Verification: Basic</p>
                        <p className="text-xs text-gray-500">Enhanced access & features</p>
                      </div>
                    </div>

                    <div className="pt-4 border-t border-green-200">
                      <h4 className="text-sm font-medium text-green-700 mb-2">Benefits Unlocked:</h4>
                      <ul className="space-y-1 text-xs text-gray-600">
                        <li>• Enhanced service access</li>
                        <li>• Priority support</li>
                        <li>• Basic analytics</li>
                        <li>• Earning opportunities</li>
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
