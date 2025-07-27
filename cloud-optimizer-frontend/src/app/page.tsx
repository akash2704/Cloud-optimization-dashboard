'use client';

import { useState, useEffect } from 'react';
import axios from 'axios';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Skeleton } from '@/components/ui/skeleton';
import { toast } from 'sonner';
import { 
  Server, 
  HardDrive, 
  DollarSign, 
  TrendingDown, 
  AlertTriangle,
  CheckCircle2 
} from 'lucide-react';

interface Resource {
  id: number;
  name: string;
  resource_type: string;
  provider: string;
  instance_type: string;
  cpu_utilization: number | null;
  memory_utilization: number | null;
  storage_gb: number | null;
  monthly_cost: number;
  created_at: string;
}

interface Recommendation {
  resource_id: number;
  resource_name: string;
  type: string;
  current_config: string;
  recommended_config: string;
  reasoning: string;
  monthly_savings: number;
  confidence: string;
}

interface Summary {
  total_resources: number;
  total_monthly_cost: number;
  total_potential_savings: number;
  optimization_opportunities: number;
}

// Try different API endpoints based on your setup
const API_BASE_URL =
  process.env.NODE_ENV === 'development'
    ? 'http://127.0.0.1:8000'
    : 'http://localhost:8000';

export default function Dashboard() {
  const [resources, setResources] = useState<Resource[]>([]);
  const [recommendations, setRecommendations] = useState<Recommendation[]>([]);
  const [summary, setSummary] = useState<Summary | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [implementedRecs, setImplementedRecs] = useState<Set<string>>(new Set());

  useEffect(() => {
    fetchAllData();
  }, []);

  const fetchAllData = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const [resourcesRes, recommendationsRes, summaryRes] = await Promise.all([
        axios.get(`${API_BASE_URL}/resources`),
        axios.get(`${API_BASE_URL}/recommendations`),
        axios.get(`${API_BASE_URL}/summary`)
      ]);

      setResources(resourcesRes.data);
      setRecommendations(recommendationsRes.data);
      setSummary(summaryRes.data);
    } catch (err) {
      setError('Failed to fetch data. Make sure the backend is running on port 8000.');
      console.error('API Error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleImplementRecommendation = (recId: string, recName: string, savings: number) => {
    setImplementedRecs(prev => new Set([...prev, recId]));
    toast.success(`Recommendation implemented for ${recName}! Potential savings: $${savings}/month`);
  };

  const getUtilizationBadge = (utilization: number | null, type: 'cpu' | 'memory') => {
    if (utilization === null) return null;
    
    let variant: "default" | "secondary" | "destructive" | "outline" = "default";
    let text = `${utilization}%`;
    
    if (utilization < 30) {
      variant = "destructive";
      text += " Low";
    } else if (utilization < 70) {
      variant = "secondary";
      text += " Medium";
    } else {
      variant = "default";
      text += " High";
    }
    
    return <Badge variant={variant}>{text}</Badge>;
  };

  const getProviderIcon = (provider: string) => {
    const iconClass = "w-4 h-4 mr-1";
    switch (provider.toLowerCase()) {
      case 'aws': return <div className={`${iconClass} bg-orange-500 rounded`} />;
      case 'azure': return <div className={`${iconClass} bg-blue-500 rounded`} />;
      case 'gcp': return <div className={`${iconClass} bg-green-500 rounded`} />;
      default: return <div className={`${iconClass} bg-gray-500 rounded`} />;
    }
  };

  if (loading) {
    return (
      <div className="container mx-auto p-6 space-y-6">
        <div className="space-y-2">
          <Skeleton className="h-8 w-64" />
          <Skeleton className="h-4 w-96" />
        </div>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          {[...Array(4)].map((_, i) => (
            <Card key={i}>
              <CardContent className="p-6">
                <Skeleton className="h-4 w-32 mb-2" />
                <Skeleton className="h-8 w-20" />
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container mx-auto p-6">
        <Alert className="border-red-200 bg-red-50">
          <AlertTriangle className="h-4 w-4" />
          <AlertDescription className="text-red-800">
            {error}
          </AlertDescription>
        </Alert>
        <Button onClick={fetchAllData} className="mt-4">
          Retry
        </Button>
      </div>
    );
  }

  return (
    <div className="container mx-auto p-6 space-y-6">
      {/* Header */}
      <div className="space-y-2">
        <h1 className="text-3xl font-bold tracking-tight">Cloud Optimization Dashboard</h1>
        <p className="text-muted-foreground">
          Monitor your cloud resources and discover cost optimization opportunities
        </p>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Resources</CardTitle>
            <Server className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{summary?.total_resources || 0}</div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Monthly Cost</CardTitle>
            <DollarSign className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">${summary?.total_monthly_cost || 0}</div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Potential Savings</CardTitle>
            <TrendingDown className="h-4 w-4 text-green-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-green-600">
              ${summary?.total_potential_savings || 0}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Opportunities</CardTitle>
            <AlertTriangle className="h-4 w-4 text-orange-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-orange-600">
              {summary?.optimization_opportunities || 0}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Resources Section */}
      <Card>
        <CardHeader>
          <CardTitle>Cloud Resources</CardTitle>
          <CardDescription>
            Overview of your cloud infrastructure with utilization metrics
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {resources.map((resource) => (
              <div
                key={resource.id}
                className="flex items-center justify-between p-4 border rounded-lg hover:bg-gray-50 transition-colors"
              >
                <div className="flex items-center space-x-4">
                  <div className="flex items-center">
                    {resource.resource_type === 'compute' ? (
                      <Server className="h-5 w-5 text-blue-600" />
                    ) : (
                      <HardDrive className="h-5 w-5 text-green-600" />
                    )}
                    {getProviderIcon(resource.provider)}
                  </div>
                  <div>
                    <h3 className="font-medium">{resource.name}</h3>
                    <p className="text-sm text-muted-foreground">
                      {resource.instance_type} • {resource.provider}
                      {resource.storage_gb && ` • ${resource.storage_gb}GB`}
                    </p>
                  </div>
                </div>
                <div className="flex items-center space-x-4">
                  {resource.cpu_utilization !== null && (
                    <div className="text-center">
                      <p className="text-xs text-muted-foreground">CPU</p>
                      {getUtilizationBadge(resource.cpu_utilization, 'cpu')}
                    </div>
                  )}
                  {resource.memory_utilization !== null && (
                    <div className="text-center">
                      <p className="text-xs text-muted-foreground">Memory</p>
                      {getUtilizationBadge(resource.memory_utilization, 'memory')}
                    </div>
                  )}
                  <div className="text-right">
                    <p className="font-medium">${resource.monthly_cost}/mo</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Recommendations Section */}
      <Card>
        <CardHeader>
          <CardTitle>Optimization Recommendations</CardTitle>
          <CardDescription>
            Cost-saving opportunities based on resource utilization analysis
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {recommendations.length === 0 ? (
              <div className="text-center py-8 text-muted-foreground">
                <CheckCircle2 className="h-12 w-12 mx-auto mb-4 text-green-500" />
                <p>Great! No optimization opportunities found.</p>
                <p className="text-sm">Your resources are well-optimized.</p>
              </div>
            ) : (
              recommendations.map((rec, index) => {
                const recId = `${rec.resource_id}-${rec.type}`;
                const isImplemented = implementedRecs.has(recId);
                
                return (
                  <div
                    key={index}
                    className={`p-4 border rounded-lg ${
                      isImplemented ? 'bg-green-50 border-green-200' : 'hover:bg-gray-50'
                    } transition-colors`}
                  >
                    <div className="flex items-start justify-between">
                      <div className="flex-1 space-y-2">
                        <div className="flex items-center space-x-2">
                          <h3 className="font-medium">{rec.resource_name}</h3>
                          <Badge variant={rec.confidence === 'High' ? 'default' : 'secondary'}>
                            {rec.confidence} Confidence
                          </Badge>
                          {isImplemented && (
                            <Badge variant="outline" className="text-green-600 border-green-600">
                              <CheckCircle2 className="w-3 h-3 mr-1" />
                              Implemented
                            </Badge>
                          )}
                        </div>
                        <p className="text-sm text-muted-foreground">{rec.reasoning}</p>
                        <div className="text-sm">
                          <p><strong>Current:</strong> {rec.current_config}</p>
                          <p><strong>Recommended:</strong> {rec.recommended_config}</p>
                        </div>
                      </div>
                      <div className="text-right space-y-2">
                        <div>
                          <p className="text-lg font-bold text-green-600">
                            ${rec.monthly_savings}/mo
                          </p>
                          <p className="text-xs text-muted-foreground">Potential savings</p>
                        </div>
                        {!isImplemented && (
                          <Button
                            size="sm"
                            onClick={() => handleImplementRecommendation(recId, rec.resource_name, rec.monthly_savings)}
                          >
                            Mark as Implemented
                          </Button>
                        )}
                      </div>
                    </div>
                  </div>
                );
              })
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}