import React, { useState, useEffect } from 'react';
import Head from 'next/head';
import {
  Shield,
  TrendingUp,
  Star,
  CheckCircle,
  AlertCircle,
  Clock,
  Lock,
  Unlock,
  Award,
  Target,
  Users,
  Building,
  FileText,
  GraduationCap,
  DollarSign,
  Zap,
  Crown,
  Trophy,
  Medal,
  Badge
} from 'lucide-react';

interface SQLLevel {
  name: string;
  color: string;
  bgColor: string;
  icon: any;
  minPoints: number;
  maxPoints: number;
  benefits: string[];
  requirements: string[];
}

interface VerificationData {
  pss: {
    documents_verified: boolean;
    identity_verified: boolean;
    address_verified: boolean;
    progress: number;
  };
  emo: {
    business_verified: boolean;
    franchise_verified: boolean;
    company_registered: boolean;
    progress: number;
  };
  edr: {
    skills_assessed: boolean;
    certifications_verified: boolean;
    experience_verified: boolean;
    progress: number;
  };
}

interface UserSQL {
  current_level: string;
  points: number;
  rank: string;
  next_level: string;
  points_to_next: number;
  total_earnings: number;
  monthly_earnings: number;
  verification_data: VerificationData;
}

export default function EHBSQLSystem() {
  const [userSQL, setUserSQL] = useState<UserSQL | null>(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('overview');

  // Mock SQL levels
  const sqlLevels: SQLLevel[] = [
    {
      name: "Free",
      color: "text-gray-600",
      bgColor: "bg-gray-100",
      icon: Lock,
      minPoints: 0,
      maxPoints: 100,
      benefits: ["Basic access to services", "Limited features", "Community support"],
      requirements: ["Email verification", "Basic profile setup"]
    },
    {
      name: "Basic",
      color: "text-blue-600",
      bgColor: "bg-blue-100",
      icon: Shield,
      minPoints: 101,
      maxPoints: 500,
      benefits: ["Enhanced service access", "Priority support", "Basic analytics"],
      requirements: ["Phone verification", "Document verification", "100 SQL points"]
    },
    {
      name: "Normal",
      color: "text-green-600",
      bgColor: "bg-green-100",
      icon: Star,
      minPoints: 501,
      maxPoints: 1000,
      benefits: ["Full service access", "Advanced features", "Premium support", "Earning opportunities"],
      requirements: ["Business verification", "Skill assessment", "500 SQL points"]
    },
    {
      name: "High",
      color: "text-purple-600",
      bgColor: "bg-purple-100",
      icon: Award,
      minPoints: 1001,
      maxPoints: 2000,
      benefits: ["VIP features", "Exclusive services", "High earning potential", "Priority access"],
      requirements: ["Franchise verification", "Advanced skills", "1000 SQL points"]
    },
    {
      name: "VIP",
      color: "text-yellow-600",
      bgColor: "bg-yellow-100",
      icon: Crown,
      minPoints: 2001,
      maxPoints: 9999,
      benefits: ["Maximum benefits", "Exclusive access", "Highest earnings", "Personal support", "Custom features"],
      requirements: ["Complete verification", "Expert skills", "2000+ SQL points"]
    }
  ];

  // Mock user SQL data
  const mockUserSQL: UserSQL = {
    current_level: "Normal",
    points: 1250,
    rank: "Gold",
    next_level: "High",
    points_to_next: 751,
    total_earnings: 2500.00,
    monthly_earnings: 450.00,
    verification_data: {
      pss: {
        documents_verified: true,
        identity_verified: true,
        address_verified: false,
        progress: 67
      },
      emo: {
        business_verified: true,
        franchise_verified: false,
        company_registered: true,
        progress: 67
      },
      edr: {
        skills_assessed: true,
        certifications_verified: true,
        experience_verified: true,
        progress: 100
      }
    }
  };

  useEffect(() => {
    // Simulate loading
    setTimeout(() => {
      setUserSQL(mockUserSQL);
      setLoading(false);
    }, 1000);
  }, []);

  const getCurrentLevel = () => {
    return sqlLevels.find(level => level.name === userSQL?.current_level);
  };

  const getNextLevel = () => {
    return sqlLevels.find(level => level.name === userSQL?.next_level);
  };

  const getProgressPercentage = () => {
    if (!userSQL) return 0;
    const currentLevel = getCurrentLevel();
    const nextLevel = getNextLevel();
    if (!currentLevel || !nextLevel) return 0;

    const currentPoints = userSQL.points - currentLevel.minPoints;
    const levelRange = nextLevel.minPoints - currentLevel.minPoints;
    return Math.min((currentPoints / levelRange) * 100, 100);
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading SQL System...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Head>
        <title>EHB SQL System</title>
        <meta name="description" content="EHB SQL Level System - Track your progress and earnings" />
      </Head>

      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <div className="text-2xl font-bold text-indigo-600">EHB SQL System</div>
            </div>

            <div className="flex items-center space-x-4">
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
        {/* Current Level Section */}
        <div className="bg-white rounded-lg shadow-sm p-6 mb-8">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              {getCurrentLevel() && (
                <div className={`p-4 rounded-lg ${getCurrentLevel()?.bgColor}`}>
                  <getCurrentLevel()?.icon className={`h-8 w-8 ${getCurrentLevel()?.color}`} />
                </div>
              )}
              <div>
                <h1 className="text-3xl font-bold text-gray-900">{userSQL?.current_level} Level</h1>
                <p className="text-gray-600">SQL Points: {userSQL?.points} • Rank: {userSQL?.rank}</p>
              </div>
            </div>

            <div className="text-right">
              <div className="text-2xl font-bold text-green-600">${userSQL?.total_earnings}</div>
              <p className="text-sm text-gray-500">Total Earnings</p>
              <div className="text-lg font-semibold text-indigo-600">${userSQL?.monthly_earnings}</div>
              <p className="text-sm text-gray-500">This Month</p>
            </div>
          </div>
        </div>

        {/* Navigation Tabs */}
        <div className="bg-white rounded-lg shadow-sm mb-8">
          <div className="border-b border-gray-200">
            <nav className="flex space-x-8 px-6">
              {[
                { id: 'overview', name: 'Overview', icon: Target },
                { id: 'levels', name: 'SQL Levels', icon: Trophy },
                { id: 'verification', name: 'Verification', icon: Shield },
                { id: 'earnings', name: 'Earnings', icon: DollarSign },
                { id: 'progress', name: 'Progress', icon: TrendingUp }
              ].map((tab) => {
                const Icon = tab.icon;
                return (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id)}
                    className={`flex items-center space-x-2 py-4 px-1 border-b-2 font-medium text-sm ${
                      activeTab === tab.id
                        ? 'border-indigo-500 text-indigo-600'
                        : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                    }`}
                  >
                    <Icon className="h-4 w-4" />
                    <span>{tab.name}</span>
                  </button>
                );
              })}
            </nav>
          </div>
        </div>

        {/* Tab Content */}
        <div className="bg-white rounded-lg shadow-sm p-6">
          {activeTab === 'overview' && (
            <div className="space-y-6">
              <h2 className="text-xl font-bold text-gray-900">SQL System Overview</h2>

              {/* Progress to Next Level */}
              <div className="bg-gradient-to-r from-indigo-500 to-purple-600 rounded-lg p-6 text-white">
                <div className="flex items-center justify-between mb-4">
                  <div>
                    <h3 className="text-lg font-semibold">Progress to {userSQL?.next_level} Level</h3>
                    <p className="text-indigo-100">{userSQL?.points_to_next} points needed</p>
                  </div>
                  <div className="text-right">
                    <div className="text-2xl font-bold">{userSQL?.points}</div>
                    <div className="text-indigo-100">Current Points</div>
                  </div>
                </div>

                <div className="w-full bg-indigo-200 rounded-full h-3 mb-2">
                  <div
                    className="bg-white h-3 rounded-full transition-all duration-300"
                    style={{ width: `${getProgressPercentage()}%` }}
                  ></div>
                </div>
                <p className="text-sm text-indigo-100">{getProgressPercentage().toFixed(1)}% complete</p>
              </div>

              {/* Stats Cards */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
                  <div className="flex items-center space-x-3">
                    <Shield className="h-8 w-8 text-blue-600" />
                    <div>
                      <p className="text-sm font-medium text-blue-600">PSS Verification</p>
                      <p className="text-2xl font-bold text-blue-900">{userSQL?.verification_data.pss.progress}%</p>
                    </div>
                  </div>
                </div>

                <div className="bg-green-50 border border-green-200 rounded-lg p-6">
                  <div className="flex items-center space-x-3">
                    <Building className="h-8 w-8 text-green-600" />
                    <div>
                      <p className="text-sm font-medium text-green-600">EMO Verification</p>
                      <p className="text-2xl font-bold text-green-900">{userSQL?.verification_data.emo.progress}%</p>
                    </div>
                  </div>
                </div>

                <div className="bg-purple-50 border border-purple-200 rounded-lg p-6">
                  <div className="flex items-center space-x-3">
                    <GraduationCap className="h-8 w-8 text-purple-600" />
                    <div>
                      <p className="text-sm font-medium text-purple-600">EDR Verification</p>
                      <p className="text-2xl font-bold text-purple-900">{userSQL?.verification_data.edr.progress}%</p>
                    </div>
                  </div>
                </div>
              </div>

              {/* Current Benefits */}
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Current Level Benefits</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {getCurrentLevel()?.benefits.map((benefit, index) => (
                    <div key={index} className="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg">
                      <CheckCircle className="h-5 w-5 text-green-600" />
                      <span className="text-gray-700">{benefit}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {activeTab === 'levels' && (
            <div className="space-y-6">
              <h2 className="text-xl font-bold text-gray-900">SQL Levels</h2>

              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {sqlLevels.map((level) => {
                  const Icon = level.icon;
                  const isCurrentLevel = level.name === userSQL?.current_level;
                  const isUnlocked = userSQL && userSQL.points >= level.minPoints;

                  return (
                    <div key={level.name} className={`border rounded-lg p-6 ${
                      isCurrentLevel
                        ? 'border-indigo-500 bg-indigo-50'
                        : isUnlocked
                          ? 'border-green-300 bg-green-50'
                          : 'border-gray-300 bg-gray-50'
                    }`}>
                      <div className="flex items-center justify-between mb-4">
                        <div className={`p-3 rounded-lg ${level.bgColor}`}>
                          <Icon className={`h-6 w-6 ${level.color}`} />
                        </div>
                        {isCurrentLevel && (
                          <span className="px-2 py-1 bg-indigo-600 text-white text-xs rounded-full">
                            Current
                          </span>
                        )}
                        {!isUnlocked && (
                          <Lock className="h-5 w-5 text-gray-400" />
                        )}
                      </div>

                      <h3 className={`text-lg font-semibold ${level.color}`}>{level.name}</h3>
                      <p className="text-sm text-gray-600 mb-4">
                        {level.minPoints} - {level.maxPoints} points
                      </p>

                      <div className="space-y-2">
                        <h4 className="text-sm font-medium text-gray-700">Benefits:</h4>
                        {level.benefits.map((benefit, index) => (
                          <div key={index} className="flex items-center space-x-2">
                            <CheckCircle className="h-3 w-3 text-green-600" />
                            <span className="text-xs text-gray-600">{benefit}</span>
                          </div>
                        ))}
                      </div>

                      {!isUnlocked && (
                        <div className="mt-4 pt-4 border-t border-gray-200">
                          <h4 className="text-sm font-medium text-gray-700 mb-2">Requirements:</h4>
                          {level.requirements.map((req, index) => (
                            <div key={index} className="flex items-center space-x-2">
                              <AlertCircle className="h-3 w-3 text-yellow-600" />
                              <span className="text-xs text-gray-600">{req}</span>
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>
            </div>
          )}

          {activeTab === 'verification' && (
            <div className="space-y-6">
              <h2 className="text-xl font-bold text-gray-900">Verification Status</h2>

              <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                {/* PSS Verification */}
                <div className="border border-gray-200 rounded-lg p-6">
                  <div className="flex items-center space-x-3 mb-4">
                    <Shield className="h-6 w-6 text-blue-600" />
                    <h3 className="text-lg font-semibold text-gray-900">PSS Verification</h3>
                  </div>

                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-gray-600">Documents Verified</span>
                      {userSQL?.verification_data.pss.documents_verified ? (
                        <CheckCircle className="h-5 w-5 text-green-600" />
                      ) : (
                        <AlertCircle className="h-5 w-5 text-yellow-600" />
                      )}
                    </div>

                    <div className="flex items-center justify-between">
                      <span className="text-sm text-gray-600">Identity Verified</span>
                      {userSQL?.verification_data.pss.identity_verified ? (
                        <CheckCircle className="h-5 w-5 text-green-600" />
                      ) : (
                        <AlertCircle className="h-5 w-5 text-yellow-600" />
                      )}
                    </div>

                    <div className="flex items-center justify-between">
                      <span className="text-sm text-gray-600">Address Verified</span>
                      {userSQL?.verification_data.pss.address_verified ? (
                        <CheckCircle className="h-5 w-5 text-green-600" />
                      ) : (
                        <AlertCircle className="h-5 w-5 text-yellow-600" />
                      )}
                    </div>
                  </div>

                  <div className="mt-4">
                    <div className="flex justify-between text-sm mb-1">
                      <span>Progress</span>
                      <span>{userSQL?.verification_data.pss.progress}%</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div
                        className="bg-blue-600 h-2 rounded-full"
                        style={{ width: `${userSQL?.verification_data.pss.progress}%` }}
                      ></div>
                    </div>
                  </div>
                </div>

                {/* EMO Verification */}
                <div className="border border-gray-200 rounded-lg p-6">
                  <div className="flex items-center space-x-3 mb-4">
                    <Building className="h-6 w-6 text-green-600" />
                    <h3 className="text-lg font-semibold text-gray-900">EMO Verification</h3>
                  </div>

                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-gray-600">Business Verified</span>
                      {userSQL?.verification_data.emo.business_verified ? (
                        <CheckCircle className="h-5 w-5 text-green-600" />
                      ) : (
                        <AlertCircle className="h-5 w-5 text-yellow-600" />
                      )}
                    </div>

                    <div className="flex items-center justify-between">
                      <span className="text-sm text-gray-600">Franchise Verified</span>
                      {userSQL?.verification_data.emo.franchise_verified ? (
                        <CheckCircle className="h-5 w-5 text-green-600" />
                      ) : (
                        <AlertCircle className="h-5 w-5 text-yellow-600" />
                      )}
                    </div>

                    <div className="flex items-center justify-between">
                      <span className="text-sm text-gray-600">Company Registered</span>
                      {userSQL?.verification_data.emo.company_registered ? (
                        <CheckCircle className="h-5 w-5 text-green-600" />
                      ) : (
                        <AlertCircle className="h-5 w-5 text-yellow-600" />
                      )}
                    </div>
                  </div>

                  <div className="mt-4">
                    <div className="flex justify-between text-sm mb-1">
                      <span>Progress</span>
                      <span>{userSQL?.verification_data.emo.progress}%</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div
                        className="bg-green-600 h-2 rounded-full"
                        style={{ width: `${userSQL?.verification_data.emo.progress}%` }}
                      ></div>
                    </div>
                  </div>
                </div>

                {/* EDR Verification */}
                <div className="border border-gray-200 rounded-lg p-6">
                  <div className="flex items-center space-x-3 mb-4">
                    <GraduationCap className="h-6 w-6 text-purple-600" />
                    <h3 className="text-lg font-semibold text-gray-900">EDR Verification</h3>
                  </div>

                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <span className="text-sm text-gray-600">Skills Assessed</span>
                      {userSQL?.verification_data.edr.skills_assessed ? (
                        <CheckCircle className="h-5 w-5 text-green-600" />
                      ) : (
                        <AlertCircle className="h-5 w-5 text-yellow-600" />
                      )}
                    </div>

                    <div className="flex items-center justify-between">
                      <span className="text-sm text-gray-600">Certifications Verified</span>
                      {userSQL?.verification_data.edr.certifications_verified ? (
                        <CheckCircle className="h-5 w-5 text-green-600" />
                      ) : (
                        <AlertCircle className="h-5 w-5 text-yellow-600" />
                      )}
                    </div>

                    <div className="flex items-center justify-between">
                      <span className="text-sm text-gray-600">Experience Verified</span>
                      {userSQL?.verification_data.edr.experience_verified ? (
                        <CheckCircle className="h-5 w-5 text-green-600" />
                      ) : (
                        <AlertCircle className="h-5 w-5 text-yellow-600" />
                      )}
                    </div>
                  </div>

                  <div className="mt-4">
                    <div className="flex justify-between text-sm mb-1">
                      <span>Progress</span>
                      <span>{userSQL?.verification_data.edr.progress}%</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div
                        className="bg-purple-600 h-2 rounded-full"
                        style={{ width: `${userSQL?.verification_data.edr.progress}%` }}
                      ></div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'earnings' && (
            <div className="space-y-6">
              <h2 className="text-xl font-bold text-gray-900">Earnings Overview</h2>

              {/* Earnings Stats */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="bg-green-50 border border-green-200 rounded-lg p-6">
                  <div className="flex items-center space-x-3">
                    <DollarSign className="h-8 w-8 text-green-600" />
                    <div>
                      <p className="text-sm font-medium text-green-600">Total Earnings</p>
                      <p className="text-2xl font-bold text-green-900">${userSQL?.total_earnings}</p>
                    </div>
                  </div>
                </div>

                <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
                  <div className="flex items-center space-x-3">
                    <TrendingUp className="h-8 w-8 text-blue-600" />
                    <div>
                      <p className="text-sm font-medium text-blue-600">Monthly Earnings</p>
                      <p className="text-2xl font-bold text-blue-900">${userSQL?.monthly_earnings}</p>
                    </div>
                  </div>
                </div>

                <div className="bg-purple-50 border border-purple-200 rounded-lg p-6">
                  <div className="flex items-center space-x-3">
                    <Star className="h-8 w-8 text-purple-600" />
                    <div>
                      <p className="text-sm font-medium text-purple-600">SQL Rank</p>
                      <p className="text-2xl font-bold text-purple-900">{userSQL?.rank}</p>
                    </div>
                  </div>
                </div>
              </div>

              {/* Earnings Chart Placeholder */}
              <div className="bg-gray-50 border border-gray-200 rounded-lg p-8">
                <div className="text-center">
                  <TrendingUp className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                  <h3 className="text-lg font-semibold text-gray-700 mb-2">Earnings Chart</h3>
                  <p className="text-gray-500">Visual representation of earnings over time</p>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'progress' && (
            <div className="space-y-6">
              <h2 className="text-xl font-bold text-gray-900">Progress Tracking</h2>

              {/* Level Progress */}
              <div className="bg-white border border-gray-200 rounded-lg p-6">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Level Progress</h3>

                <div className="space-y-4">
                  {sqlLevels.map((level, index) => {
                    const Icon = level.icon;
                    const isCurrentLevel = level.name === userSQL?.current_level;
                    const isCompleted = userSQL && userSQL.points >= level.maxPoints;
                    const isUnlocked = userSQL && userSQL.points >= level.minPoints;

                    return (
                      <div key={level.name} className="flex items-center space-x-4">
                        <div className={`p-2 rounded-lg ${level.bgColor}`}>
                          <Icon className={`h-5 w-5 ${level.color}`} />
                        </div>

                        <div className="flex-1">
                          <div className="flex items-center justify-between mb-1">
                            <span className={`font-medium ${level.color}`}>{level.name}</span>
                            <span className="text-sm text-gray-500">
                              {level.minPoints} - {level.maxPoints} points
                            </span>
                          </div>

                          <div className="w-full bg-gray-200 rounded-full h-2">
                            <div
                              className={`h-2 rounded-full transition-all duration-300 ${
                                isCompleted ? 'bg-green-500' : isUnlocked ? 'bg-blue-500' : 'bg-gray-300'
                              }`}
                              style={{
                                width: isUnlocked
                                  ? `${Math.min(((userSQL?.points || 0) - level.minPoints) / (level.maxPoints - level.minPoints) * 100, 100)}%`
                                  : '0%'
                              }}
                            ></div>
                          </div>
                        </div>

                        <div className="text-right">
                          {isCompleted && <CheckCircle className="h-5 w-5 text-green-600" />}
                          {isCurrentLevel && <Star className="h-5 w-5 text-yellow-600" />}
                          {!isUnlocked && <Lock className="h-5 w-5 text-gray-400" />}
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
