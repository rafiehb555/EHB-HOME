import React from 'react';
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
  Users
} from 'lucide-react';

const Services: React.FC = () => {
  const services = [
    {
      icon: <Database className="w-8 h-8" />,
      title: 'EHB SQL',
      description: 'User quality level determination system',
      features: ['Level-based access', 'Service quality control', 'User verification'],
      color: 'from-blue-500 to-blue-600',
      port: 'Shared Logic'
    },
    {
      icon: <Shield className="w-8 h-8" />,
      title: 'PSS',
      description: 'Personal Security System - KYC & ID verification',
      features: ['Identity verification', 'Document validation', 'Security checks'],
      color: 'from-green-500 to-green-600',
      port: '4001'
    },
    {
      icon: <Building className="w-8 h-8" />,
      title: 'EMO',
      description: 'Enterprise Management Organization - Business verification',
      features: ['Business verification', 'Company validation', 'Enterprise checks'],
      color: 'from-purple-500 to-purple-600',
      port: '4003'
    },
    {
      icon: <GraduationCap className="w-8 h-8" />,
      title: 'EDR',
      description: 'Education & Development Records - Skill testing',
      features: ['Skill assessment', 'Certification', 'Professional validation'],
      color: 'from-orange-500 to-orange-600',
      port: '4002'
    },
    {
      icon: <Users className="w-8 h-8" />,
      title: 'JPS',
      description: 'Job Profile System - User profiles & resumes',
      features: ['Profile management', 'Resume builder', 'Job matching'],
      color: 'from-indigo-500 to-indigo-600',
      port: '4005'
    },
    {
      icon: <ShoppingCart className="w-8 h-8" />,
      title: 'GoSellr',
      description: 'E-commerce platform & order management',
      features: ['Online store', 'Order processing', 'Inventory management'],
      color: 'from-pink-500 to-pink-600',
      port: '4004'
    },
    {
      icon: <Wallet className="w-8 h-8" />,
      title: 'Wallet',
      description: 'Blockchain wallet & transaction management',
      features: ['Crypto transactions', 'Payment processing', 'Security'],
      color: 'from-yellow-500 to-yellow-600',
      port: '5001'
    },
    {
      icon: <Store className="w-8 h-8" />,
      title: 'Franchise',
      description: 'Franchise management & local operations',
      features: ['Franchise control', 'Local operations', 'Business management'],
      color: 'from-red-500 to-red-600',
      port: '4006'
    },
    {
      icon: <Brain className="w-8 h-8" />,
      title: 'AI Marketplace',
      description: 'AI-powered marketplace & services',
      features: ['AI services', 'Marketplace', 'Intelligent solutions'],
      color: 'from-teal-500 to-teal-600',
      port: 'AI Services'
    },
    {
      icon: <Bot className="w-8 h-8" />,
      title: 'AI Agent',
      description: 'Intelligent agent system',
      features: ['Automated assistance', 'Smart responses', 'Process automation'],
      color: 'from-cyan-500 to-cyan-600',
      port: 'AI Services'
    }
  ];

  return (
    <section className="py-20 bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          viewport={{ once: true }}
          className="text-center mb-16"
        >
          <h2 className="text-4xl font-bold text-gray-900 mb-4">
            Complete EHB Ecosystem
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Our comprehensive suite of services covers everything from verification
            to blockchain transactions and AI-powered solutions.
          </p>
        </motion.div>

        {/* Services Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {services.map((service, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: index * 0.1 }}
              viewport={{ once: true }}
              className="bg-white rounded-xl shadow-lg hover:shadow-xl transition-shadow duration-300 overflow-hidden"
            >
              {/* Service Header */}
              <div className={`bg-gradient-to-r ${service.color} p-6`}>
                <div className="flex items-center justify-between">
                  <div className="text-white">{service.icon}</div>
                  <span className="text-white/80 text-sm font-medium bg-white/20 px-3 py-1 rounded-full">
                    Port {service.port}
                  </span>
                </div>
                <h3 className="text-white text-xl font-bold mt-4">{service.title}</h3>
                <p className="text-white/90 mt-2">{service.description}</p>
              </div>

              {/* Service Features */}
              <div className="p-6">
                <h4 className="font-semibold text-gray-900 mb-3">Key Features:</h4>
                <ul className="space-y-2">
                  {service.features.map((feature, featureIndex) => (
                    <li key={featureIndex} className="flex items-center text-gray-600">
                      <div className={`w-2 h-2 bg-gradient-to-r ${service.color} rounded-full mr-3`}></div>
                      {feature}
                    </li>
                  ))}
                </ul>

                {/* Action Button */}
                <button className={`mt-6 w-full bg-gradient-to-r ${service.color} text-white py-2 px-4 rounded-lg hover:opacity-90 transition-opacity font-medium`}>
                  Learn More
                </button>
              </div>
            </motion.div>
          ))}
        </div>

        {/* Call to Action */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.4 }}
          viewport={{ once: true }}
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
    </section>
  );
};

export default Services;
