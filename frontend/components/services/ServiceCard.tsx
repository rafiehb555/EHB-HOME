import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Progress } from '@/components/ui/progress';
import {
  Shield,
  Building,
  Brain,
  User,
  ShoppingCart,
  Wallet,
  Bot,
  Settings,
  CheckCircle,
  Clock,
  AlertCircle,
  ExternalLink
} from 'lucide-react';

interface ServiceCardProps {
  service: {
    name: string;
    display_name: string;
    url: string;
    description: string;
    status?: 'ready' | 'pending' | 'error';
    verification_status?: 'verified' | 'pending' | 'failed';
    score?: number;
  };
  onVerify?: (serviceName: string) => void;
  onViewDetails?: (serviceName: string) => void;
}

const ServiceCard = ({ service, onVerify, onViewDetails }: ServiceCardProps) => {
  const [loading, setLoading] = useState(false);

  const getServiceIcon = (serviceName: string) => {
    switch (serviceName) {
      case 'pss':
        return <Shield className="h-6 w-6" />;
      case 'emo':
        return <Building className="h-6 w-6" />;
      case 'edr':
        return <Brain className="h-6 w-6" />;
      case 'jps':
        return <User className="h-6 w-6" />;
      case 'gosellr':
        return <ShoppingCart className="h-6 w-6" />;
      case 'wallet':
        return <Wallet className="h-6 w-6" />;
      case 'ai-agent':
        return <Bot className="h-6 w-6" />;
      case 'ai-robot':
        return <Bot className="h-6 w-6" />;
      default:
        return <Settings className="h-6 w-6" />;
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'verified':
        return <CheckCircle className="h-4 w-4 text-green-600" />;
      case 'pending':
        return <Clock className="h-4 w-4 text-yellow-600" />;
      case 'failed':
        return <AlertCircle className="h-4 w-4 text-red-600" />;
      default:
        return <Clock className="h-4 w-4 text-gray-400" />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'verified':
        return 'bg-green-100 text-green-800';
      case 'pending':
        return 'bg-yellow-100 text-yellow-800';
      case 'failed':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const handleVerify = async () => {
    if (onVerify) {
      setLoading(true);
      try {
        await onVerify(service.name);
      } finally {
        setLoading(false);
      }
    }
  };

  return (
    <Card className="hover:shadow-md transition-shadow">
      <CardHeader className="pb-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-blue-100 rounded-lg">
              {getServiceIcon(service.name)}
            </div>
            <div>
              <CardTitle className="text-lg">{service.display_name}</CardTitle>
              <p className="text-sm text-gray-600">{service.description}</p>
            </div>
          </div>
          <div className="flex items-center space-x-2">
            {service.verification_status && (
              <Badge className={getStatusColor(service.verification_status)}>
                {getStatusIcon(service.verification_status)}
                <span className="ml-1">{service.verification_status}</span>
              </Badge>
            )}
            {service.status && (
              <Badge variant={service.status === 'ready' ? 'default' : 'secondary'}>
                {service.status}
              </Badge>
            )}
          </div>
        </div>
      </CardHeader>
      <CardContent>
        {service.score !== undefined && (
          <div className="mb-4">
            <div className="flex items-center justify-between text-sm mb-2">
              <span>Verification Score</span>
              <span className="font-medium">{service.score}%</span>
            </div>
            <Progress value={service.score} className="h-2" />
          </div>
        )}

        <div className="flex items-center justify-between">
          <div className="flex space-x-2">
            {onVerify && service.verification_status !== 'verified' && (
              <Button
                size="sm"
                onClick={handleVerify}
                disabled={loading}
                className="flex items-center space-x-1"
              >
                {loading ? (
                  <div className="animate-spin rounded-full h-3 w-3 border-b-2 border-white"></div>
                ) : (
                  <Shield className="h-3 w-3" />
                )}
                <span>Verify</span>
              </Button>
            )}

            {onViewDetails && (
              <Button
                size="sm"
                variant="outline"
                onClick={() => onViewDetails(service.name)}
                className="flex items-center space-x-1"
              >
                <ExternalLink className="h-3 w-3" />
                <span>Details</span>
              </Button>
            )}
          </div>

          <div className="text-xs text-gray-500">
            Port: {service.url.split(':').pop()}
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default ServiceCard;
