import React, { useState, useEffect } from 'react';
import Head from 'next/head';
import {
  Search,
  ShoppingCart,
  Shield,
  User,
  Wallet,
  TrendingUp,
  Star,
  ArrowRight,
  Play,
  BookOpen,
  Heart,
  GraduationCap,
  Scale,
  Code,
  Store,
  Users,
  Bell,
  ChevronRight,
  ChevronLeft
} from 'lucide-react';

interface Service {
  id: number;
  name: string;
  description: string;
  price: number;
  rating: number;
  category: string;
  image: string;
  featured: boolean;
}

interface User {
  id: number;
  name: string;
  sqlLevel: string;
  verified: boolean;
  avatar: string;
}

export default function EHBHomePage() {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [currentSlide, setCurrentSlide] = useState(0);
  const [user, setUser] = useState<User | null>(null);

  // Mock data for services
  const services: Service[] = [
    {
      id: 1,
      name: "Personal Security System (PSS)",
      description: "Advanced personal security and verification system",
      price: 29.99,
      rating: 4.8,
      category: "security",
      image: "/images/pss.png",
      featured: true
    },
    {
      id: 2,
      name: "Easy Management Office (EMO)",
      description: "Comprehensive office management solution",
      price: 49.99,
      rating: 4.6,
      category: "business",
      image: "/images/emo.png",
      featured: true
    },
    {
      id: 3,
      name: "Exam Decision Registration (EDR)",
      description: "Educational examination and decision system",
      price: 39.99,
      rating: 4.7,
      category: "education",
      image: "/images/edr.png",
      featured: true
    },
    {
      id: 4,
      name: "Job Profile System (JPS)",
      description: "Professional job profile and career management",
      price: 19.99,
      rating: 4.5,
      category: "career",
      image: "/images/jps.png",
      featured: true
    },
    {
      id: 5,
      name: "GoSellr E-commerce",
      description: "Complete e-commerce platform for businesses",
      price: 79.99,
      rating: 4.9,
      category: "ecommerce",
      image: "/images/gosellr.png",
      featured: true
    }
  ];

  const categories = [
    { id: 'all', name: 'All Services', icon: Store },
    { id: 'security', name: 'Security', icon: Shield },
    { id: 'business', name: 'Business', icon: TrendingUp },
    { id: 'education', name: 'Education', icon: GraduationCap },
    { id: 'career', name: 'Career', icon: User },
    { id: 'ecommerce', name: 'E-commerce', icon: ShoppingCart }
  ];

  const heroSlides = [
    {
      title: "Franchise Opportunities",
      subtitle: "Join the EHB ecosystem and grow your business",
      image: "/images/franchise.jpg",
      cta: "Explore Franchises"
    },
    {
      title: "EHB Services",
      subtitle: "Discover our comprehensive service suite",
      image: "/images/services.jpg",
      cta: "View Services"
    },
    {
      title: "Blockchain Integration",
      subtitle: "Secure transactions with blockchain technology",
      image: "/images/blockchain.jpg",
      cta: "Learn More"
    }
  ];

  const filteredServices = services.filter(service =>
    selectedCategory === 'all' || service.category === selectedCategory
  );

  const featuredServices = services.filter(service => service.featured);

  useEffect(() => {
    // Auto-advance hero slider
    const interval = setInterval(() => {
      setCurrentSlide((prev) => (prev + 1) % heroSlides.length);
    }, 5000);
    return () => clearInterval(interval);
  }, [heroSlides.length]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <Head>
        <title>EHB - Home Page</title>
        <meta name="description" content="EHB Home Page - Your gateway to comprehensive services" />
      </Head>

      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            {/* Logo */}
            <div className="flex items-center">
              <div className="text-2xl font-bold text-indigo-600">EHB</div>
            </div>

            {/* AI Search Bar */}
            <div className="flex-1 max-w-2xl mx-8">
              <div className="relative">
                <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-5 w-5" />
                <input
                  type="text"
                  placeholder="Search services, dashboards, users..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                />
              </div>
            </div>

            {/* Navigation */}
            <nav className="flex items-center space-x-4">
              <button className="text-gray-600 hover:text-indigo-600">
                <Bell className="h-5 w-5" />
              </button>
              {user ? (
                <div className="flex items-center space-x-2">
                  <img src={user.avatar} alt={user.name} className="w-8 h-8 rounded-full" />
                  <span className="text-sm font-medium">{user.name}</span>
                  <a href="/dashboard" className="px-3 py-1 bg-indigo-600 text-white rounded text-sm hover:bg-indigo-700">
                    Dashboard
                  </a>
                  <a href="/sql-system" className="px-3 py-1 bg-green-600 text-white rounded text-sm hover:bg-green-700">
                    SQL System
                  </a>
                  <a href="/pss" className="px-3 py-1 bg-blue-600 text-white rounded text-sm hover:bg-blue-700">
                    PSS
                  </a>
                </div>
              ) : (
                <div className="flex space-x-2">
                  <button className="px-4 py-2 text-gray-600 hover:text-indigo-600">Login</button>
                  <button className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700">
                    Register
                  </button>
                </div>
              )}
            </nav>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="relative h-96 overflow-hidden">
        <div className="relative h-full">
          {heroSlides.map((slide, index) => (
            <div
              key={index}
              className={`absolute inset-0 transition-opacity duration-1000 ${
                index === currentSlide ? 'opacity-100' : 'opacity-0'
              }`}
            >
              <div className="absolute inset-0 bg-gradient-to-r from-black/50 to-transparent z-10" />
              <div className="absolute inset-0 bg-cover bg-center" style={{ backgroundImage: `url(${slide.image})` }} />
              <div className="relative z-20 h-full flex items-center">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                  <div className="max-w-2xl">
                    <h1 className="text-4xl md:text-6xl font-bold text-white mb-4">
                      {slide.title}
                    </h1>
                    <p className="text-xl text-white/90 mb-8">
                      {slide.subtitle}
                    </p>
                    <button className="px-8 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors">
                      {slide.cta}
                    </button>
                  </div>
                </div>
              </div>
            </div>
          ))}

          {/* Slider Controls */}
          <div className="absolute bottom-4 left-1/2 transform -translate-x-1/2 z-30 flex space-x-2">
            {heroSlides.map((_, index) => (
              <button
                key={index}
                onClick={() => setCurrentSlide(index)}
                className={`w-3 h-3 rounded-full transition-colors ${
                  index === currentSlide ? 'bg-white' : 'bg-white/50'
                }`}
              />
            ))}
          </div>
        </div>
      </section>

      {/* Service Categories */}
      <section className="py-12 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-center mb-8">Browse by Category</h2>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
            {categories.map((category) => {
              const Icon = category.icon;
              return (
                <button
                  key={category.id}
                  onClick={() => setSelectedCategory(category.id)}
                  className={`p-4 rounded-lg border-2 transition-colors ${
                    selectedCategory === category.id
                      ? 'border-indigo-500 bg-indigo-50'
                      : 'border-gray-200 hover:border-indigo-300'
                  }`}
                >
                  <Icon className="h-8 w-8 mx-auto mb-2 text-indigo-600" />
                  <p className="text-sm font-medium text-center">{category.name}</p>
                </button>
              );
            })}
          </div>
        </div>
      </section>

      {/* Featured Services */}
      <section className="py-12 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-center mb-8">Featured Services</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {featuredServices.map((service) => (
              <div key={service.id} className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow">
                <div className="h-48 bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center">
                  <div className="text-white text-4xl font-bold">{service.name.split(' ')[0]}</div>
                </div>
                <div className="p-6">
                  <h3 className="text-xl font-semibold mb-2">{service.name}</h3>
                  <p className="text-gray-600 mb-4">{service.description}</p>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-1">
                      <Star className="h-4 w-4 text-yellow-400 fill-current" />
                      <span className="text-sm text-gray-600">{service.rating}</span>
                    </div>
                    <div className="text-lg font-bold text-indigo-600">${service.price}/month</div>
                  </div>
                  <button className="w-full mt-4 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors">
                    Learn More
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Quick Access Cards */}
      <section className="py-12 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl font-bold text-center mb-8">Quick Access</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
            {[
              { name: 'GoSellr', icon: ShoppingCart, color: 'bg-green-500' },
              { name: 'PSS', icon: Shield, color: 'bg-blue-500' },
              { name: 'JPS', icon: User, color: 'bg-purple-500' },
              { name: 'Wallet', icon: Wallet, color: 'bg-yellow-500' }
            ].map((item) => {
              const Icon = item.icon;
              return (
                <div key={item.name} className="text-center">
                  <div className={`${item.color} w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4`}>
                    <Icon className="h-8 w-8 text-white" />
                  </div>
                  <h3 className="font-semibold">{item.name}</h3>
                </div>
              );
            })}
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-800 text-white py-8">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div>
              <h3 className="text-lg font-semibold mb-4">EHB</h3>
              <p className="text-gray-300">Your gateway to comprehensive services</p>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Services</h4>
              <ul className="space-y-2 text-gray-300">
                <li>GoSellr</li>
                <li>PSS</li>
                <li>EMO</li>
                <li>EDR</li>
                <li>JPS</li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Support</h4>
              <ul className="space-y-2 text-gray-300">
                <li>Help Center</li>
                <li>Contact Us</li>
                <li>Documentation</li>
                <li>Status</li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Company</h4>
              <ul className="space-y-2 text-gray-300">
                <li>About</li>
                <li>Careers</li>
                <li>Privacy</li>
                <li>Terms</li>
              </ul>
            </div>
          </div>
          <div className="border-t border-gray-700 mt-8 pt-8 text-center text-gray-300">
            <p>&copy; 2024 EHB. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}
