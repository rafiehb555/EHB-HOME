import { useState } from 'react';
import Layout from '../components/Layout';
import { motion } from 'framer-motion';
import {
  Shield,
  Building,
  GraduationCap,
  ShoppingCart,
  Wallet,
  Store,
  Brain,
  Bot,
  Database,
  Users,
  CheckCircle,
  ArrowRight,
  Star,
  Zap,
  Globe,
  Lock
} from 'lucide-react';

const ServicesPage = () => {
  const [selectedService, setSelectedService] = useState<string | null>(null);

  const services = [
    {
      id: 'sql',
      name: 'EHB SQL',
      description: 'User quality level determination system',
      longDescription: 'The core system that determines user quality levels and controls access to premium features across all EHB services.',
      icon: Database,
      color: 'from-blue-500 to-blue-600',
      features: [
        'Level-based access control',
        'Service quality monitoring',
        'User verification tracking',
        'Premium feature management'
      ],
      benefits: [
        'Enhanced security',
        'Quality assurance',
        'Scalable access control',
        'Centralized user management'
      ],
      status: 'Active',
      port: 'Shared Logic'
    },
    {
      id: 'pss',
      name: 'PSS',
      description: 'Personal Security System - KYC & ID verification',
      longDescription: 'Comprehensive identity verification system that ensures secure and compliant user onboarding.',
      icon: Shield,
      color: 'from-green-500 to-green-600',
      features: [
        'Identity verification',
        'Document validation',
        'Biometric authentication',
        'Compliance monitoring'
      ],
      benefits: [
        'Fraud prevention',
        'Regulatory compliance',
        'Trust building',
        'Secure onboarding'
      ],
      status: 'Active',
      port: '4001'
    },
    {
      id: 'emo',
      name: 'EMO',
      description: 'Enterprise Management Organization - Business verification',
      longDescription: 'Business verification and management system for enterprise clients and commercial entities.',
      icon: Building,
      color: 'from-purple-500 to-purple-600',
      features: [
        'Business verification',
        'Company validation',
        'Enterprise onboarding',
        'Corporate compliance'
      ],
      benefits: [
        'Enterprise security',
        'Business validation',
        'Corporate trust',
        'Scalable operations'
      ],
      status: 'Active',
      port: '4003'
    },
    {
      id: 'edr',
      name: 'EDR',
      description: 'Education & Development Records - Skill testing',
      longDescription: 'Comprehensive skill assessment and certification system for professionals and service providers.',
      icon: GraduationCap,
      color: 'from-orange-500 to-orange-600',
      features: [
        'Skill assessment',
        'Professional certification',
        'Competency testing',
        'Credential verification'
      ],
      benefits: [
        'Quality assurance',
        'Professional validation',
        'Skill verification',
        'Trust building'
      ],
      status: 'Active',
      port: '4002'
    },
    {
      id: 'jps',
      name: 'JPS',
      description: 'Job Profile System - User profiles & resumes',
      longDescription: 'Comprehensive profile management system for job seekers and service providers.',
      icon: Users,
      color: 'from-indigo-500 to-indigo-600',
      features: [
        'Profile management',
        'Resume builder',
        'Job matching',
        'Professional networking'
      ],
      benefits: [
        'Career advancement',
        'Professional networking',
        'Job opportunities',
        'Skill showcase'
      ],
      status: 'Active',
      port: '4005'
    },
    {
      id: 'gosellr',
      name: 'GoSellr',
      description: 'E-commerce platform & order management',
      longDescription: 'Complete e-commerce solution with integrated payment processing and inventory management.',
      icon: ShoppingCart,
      color: 'from-pink-500 to-pink-600',
      features: [
        'Online store creation',
        'Order processing',
        'Inventory management',
        'Payment integration'
      ],
      benefits: [
        'Revenue generation',
        'Business growth',
        'Customer reach',
        'Operational efficiency'
      ],
      status: 'Active',
      port: '4004'
    },
    {
      id: 'wallet',
      name: 'Wallet',
      description: 'Blockchain wallet & transaction management',
      longDescription: 'Secure blockchain wallet supporting multiple cryptocurrencies and digital asset management.',
      icon: Wallet,
      color: 'from-yellow-500 to-yellow-600',
      features: [
        'Multi-crypto support',
        'Secure transactions',
        'Digital asset management',
        'Blockchain integration'
      ],
      benefits: [
        'Financial freedom',
        'Secure transactions',
        'Global access',
        'Asset protection'
      ],
      status: 'Active',
      port: '5001'
    },
    {
      id: 'franchise',
      name: 'Franchise',
      description: 'Franchise management & local operations',
      longDescription: 'Comprehensive franchise management system for business expansion and local operations.',
      icon: Store,
      color: 'from-red-500 to-red-600',
      features: [
        'Franchise management',
        'Local operations',
        'Business expansion',
        'Operational control'
      ],
      benefits: [
        'Business expansion',
        'Operational efficiency',
        'Local control',
        'Scalable growth'
      ],
      status: 'Active',
      port: '4006'
    },
    {
      id: 'ai-marketplace',
      name: 'AI Marketplace',
      description: 'AI-powered marketplace & services',
      longDescription: 'Intelligent marketplace platform powered by artificial intelligence for enhanced user experience.',
      icon: Brain,
      color: 'from-teal-500 to-teal-600',
      features: [
        'AI-powered recommendations',
        'Intelligent matching',
        'Predictive analytics',
        'Smart automation'
      ],
      benefits: [
        'Enhanced user experience',
        'Intelligent insights',
        'Automated processes',
        'Data-driven decisions'
      ],
      status: 'Active',
      port: 'AI Services'
    },
    {
      id: 'ai-agent',
      name: 'AI Agent',
      description: 'Intelligent agent system',
      longDescription: 'Advanced AI agent system providing automated assistance and intelligent responses.',
      icon: Bot,
      color: 'from-cyan-500 to-cyan-600',
      features: [
        'Automated assistance',
        'Intelligent responses',
        'Process automation',
        '24/7 support'
      ],
      benefits: [
        'Improved efficiency',
        'Reduced costs',
        'Better user experience',
        'Scalable support'
      ],
      status: 'Active',
      port: 'AI Services'
    }
  ];

  const selectedServiceData = services.find(s => s.id === selectedService);

  return (
    <Layout title="EHB Services - Complete Ecosystem">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="text-center mb-12">
          <motion.h1
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-4xl font-bold text-gray-900 mb-4"
          >
            EHB Services
          </motion.h1>
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="text-xl text-gray-600 max-w-3xl mx-auto"
          >
            Complete ecosystem of integrated services for modern business solutions.
            From verification to blockchain, we provide everything you need.
          </motion.p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Services List */}
          <div className="lg:col-span-2">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {services.map((service, index) => (
                <motion.div
                  key={service.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.1 }}
                  className={`bg-white rounded-xl shadow-sm border-2 cursor-pointer transition-all duration-300 hover:shadow-lg ${
                    selectedService === service.id
                      ? 'border-blue-500 shadow-lg'
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                  onClick={() => setSelectedService(service.id)}
                >
                  <div className={`bg-gradient-to-r ${service.color} p-6 rounded-t-xl`}>
                    <div className="flex items-center justify-between">
                      <div className="text-white">
                        <service.icon className="w-8 h-8" />
                      </div>
                      <span className="text-white/80 text-sm font-medium bg-white/20 px-3 py-1 rounded-full">
                        Port {service.port}
                      </span>
                    </div>
                    <h3 className="text-white text-xl font-bold mt-4">{service.name}</h3>
                    <p className="text-white/90 mt-2">{service.description}</p>
                  </div>
                  <div className="p-6">
                    <div className="flex items-center justify-between mb-4">
                      <span className="text-sm text-gray-600">Status</span>
                      <span className="text-sm text-green-600 font-medium">{service.status}</span>
                    </div>
                    <button className="w-full bg-gray-100 text-gray-700 py-2 px-4 rounded-lg hover:bg-gray-200 transition-colors text-sm font-medium">
                      Learn More
                    </button>
                  </div>
                </motion.div>
              ))}
            </div>
          </div>

          {/* Service Details */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 sticky top-8">
              {selectedServiceData ? (
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  className="space-y-6"
                >
                  <div className={`bg-gradient-to-r ${selectedServiceData.color} p-6 rounded-lg text-white`}>
                    <selectedServiceData.icon className="w-12 h-12 mb-4" />
                    <h3 className="text-2xl font-bold mb-2">{selectedServiceData.name}</h3>
                    <p className="text-white/90">{selectedServiceData.longDescription}</p>
                  </div>

                  <div>
                    <h4 className="font-semibold text-gray-900 mb-3 flex items-center">
                      <Zap className="w-5 h-5 mr-2 text-blue-600" />
                      Key Features
                    </h4>
                    <ul className="space-y-2">
                      {selectedServiceData.features.map((feature, index) => (
                        <li key={index} className="flex items-center text-gray-600">
                          <CheckCircle className="w-4 h-4 text-green-500 mr-2" />
                          {feature}
                        </li>
                      ))}
                    </ul>
                  </div>

                  <div>
                    <h4 className="font-semibold text-gray-900 mb-3 flex items-center">
                      <Star className="w-5 h-5 mr-2 text-yellow-600" />
                      Benefits
                    </h4>
                    <ul className="space-y-2">
                      {selectedServiceData.benefits.map((benefit, index) => (
                        <li key={index} className="flex items-center text-gray-600">
                          <CheckCircle className="w-4 h-4 text-green-500 mr-2" />
                          {benefit}
                        </li>
                      ))}
                    </ul>
                  </div>

                  <div className="pt-4 border-t border-gray-200">
                    <button className="w-full bg-blue-600 text-white py-3 px-4 rounded-lg hover:bg-blue-700 transition-colors font-medium flex items-center justify-center">
                      <span>Get Started</span>
                      <ArrowRight className="w-4 h-4 ml-2" />
                    </button>
                  </div>
                </motion.div>
              ) : (
                <div className="text-center py-12">
                  <Globe className="w-16 h-16 text-gray-400 mx-auto mb-4" />
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">
                    Select a Service
                  </h3>
                  <p className="text-gray-600">
                    Choose a service from the list to view detailed information and features.
                  </p>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Call to Action */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.8 }}
          className="text-center mt-16"
        >
          <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-2xl p-8 text-white">
            <h3 className="text-2xl font-bold mb-4">
              Ready to Get Started?
            </h3>
            <p className="text-blue-100 mb-6 max-w-2xl mx-auto">
              Join thousands of users who trust EHB Technologies for their
              digital transformation needs. Start your journey today.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <button className="bg-white text-blue-600 px-6 py-3 rounded-lg font-semibold hover:bg-gray-100 transition-colors">
                Start Free Trial
              </button>
              <button className="border-2 border-white text-white px-6 py-3 rounded-lg font-semibold hover:bg-white hover:text-blue-600 transition-colors">
                Contact Sales
              </button>
            </div>
          </div>
        </motion.div>
      </div>
    </Layout>
  );
};

export default ServicesPage;
