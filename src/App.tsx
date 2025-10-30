import { useState, useEffect } from 'react';
import { Brain, TrendingUp, Users, Award, AlertCircle, CheckCircle } from 'lucide-react';
import PredictionForm from './components/PredictionForm';
import ResultsDisplay from './components/ResultsDisplay';
import ModelInfo from './components/ModelInfo';

interface ModelMetrics {
  model_name: string;
  r2_score: number;
  rmse: number;
  mae: number;
  training_samples: number;
  test_samples: number;
}

interface PredictionResult {
  predicted_grade: number;
  performance_level: string;
  confidence_score: number;
  model_used: string;
  recommendations: string[];
}

function App() {
  const [activeTab, setActiveTab] = useState<'predict' | 'info'>('predict');
  const [modelMetrics, setModelMetrics] = useState<ModelMetrics | null>(null);
  const [prediction, setPrediction] = useState<PredictionResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [backendStatus, setBackendStatus] = useState<'checking' | 'online' | 'offline'>('checking');

  const API_URL = import.meta.env.VITE_API_URL || 'https://student-performance-prediction-l7zw.vercel.app/';

  useEffect(() => {
    checkBackendStatus();
    fetchModelInfo();
  }, []);

  const checkBackendStatus = async () => {
    try {
      const response = await fetch(`${API_URL}/`);
      if (response.ok) {
        setBackendStatus('online');
      } else {
        setBackendStatus('offline');
      }
    } catch (err) {
      setBackendStatus('offline');
    }
  };

  const fetchModelInfo = async () => {
    try {
      const response = await fetch(`${API_URL}/model-info`);
      if (response.ok) {
        const data = await response.json();
        setModelMetrics(data.metrics);
      }
    } catch (err) {
      console.error('Error fetching model info:', err);
    }
  };

  const handlePredict = async (studentData: any) => {
    setLoading(true);
    setError(null);
    setPrediction(null);

    try {
      const response = await fetch(`${API_URL}/predict`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(studentData),
      });

      if (!response.ok) {
        throw new Error('Prediction failed');
      }

      const result = await response.json();
      setPrediction(result);
      setActiveTab('predict');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
      <header className="bg-white shadow-sm border-b border-slate-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="bg-gradient-to-br from-blue-500 to-blue-600 p-3 rounded-xl shadow-lg">
                <Brain className="w-8 h-8 text-white" />
              </div>
              <div>
                <h1 className="text-3xl font-bold text-slate-900">
                  Student Performance Prediction
                </h1>
                <p className="text-sm text-slate-600 mt-1">
                  ML-Powered Academic Analytics System
                </p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              {backendStatus === 'checking' && (
                <span className="text-sm text-slate-500">Checking backend...</span>
              )}
              {backendStatus === 'online' && (
                <div className="flex items-center gap-2 px-3 py-1.5 bg-green-50 border border-green-200 rounded-lg">
                  <CheckCircle className="w-4 h-4 text-green-600" />
                  <span className="text-sm font-medium text-green-700">Backend Online</span>
                </div>
              )}
              {backendStatus === 'offline' && (
                <div className="flex items-center gap-2 px-3 py-1.5 bg-red-50 border border-red-200 rounded-lg">
                  <AlertCircle className="w-4 h-4 text-red-600" />
                  <span className="text-sm font-medium text-red-700">Backend Offline</span>
                </div>
              )}
            </div>
          </div>
        </div>
      </header>

      {backendStatus === 'offline' && (
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="bg-amber-50 border border-amber-200 rounded-lg p-4">
            <div className="flex items-start gap-3">
              <AlertCircle className="w-5 h-5 text-amber-600 flex-shrink-0 mt-0.5" />
              <div>
                <h3 className="text-sm font-semibold text-amber-900">Backend Not Running</h3>
                <p className="text-sm text-amber-800 mt-1">
                  Please start the Python backend server:
                  <code className="block mt-2 bg-amber-100 px-3 py-2 rounded font-mono text-xs">
                    cd backend && python main.py
                  </code>
                </p>
              </div>
            </div>
          </div>
        </div>
      )}

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {modelMetrics && (
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
            <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-5">
              <div className="flex items-center gap-3">
                <div className="bg-blue-50 p-2.5 rounded-lg">
                  <TrendingUp className="w-5 h-5 text-blue-600" />
                </div>
                <div>
                  <p className="text-xs text-slate-500 uppercase tracking-wide font-medium">R² Score</p>
                  <p className="text-2xl font-bold text-slate-900 mt-0.5">
                    {(modelMetrics.r2_score * 100).toFixed(1)}%
                  </p>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-5">
              <div className="flex items-center gap-3">
                <div className="bg-green-50 p-2.5 rounded-lg">
                  <Award className="w-5 h-5 text-green-600" />
                </div>
                <div>
                  <p className="text-xs text-slate-500 uppercase tracking-wide font-medium">Model</p>
                  <p className="text-lg font-bold text-slate-900 mt-0.5">
                    {modelMetrics.model_name}
                  </p>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-5">
              <div className="flex items-center gap-3">
                <div className="bg-purple-50 p-2.5 rounded-lg">
                  <Users className="w-5 h-5 text-purple-600" />
                </div>
                <div>
                  <p className="text-xs text-slate-500 uppercase tracking-wide font-medium">Training Data</p>
                  <p className="text-2xl font-bold text-slate-900 mt-0.5">
                    {modelMetrics.training_samples}
                  </p>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-5">
              <div className="flex items-center gap-3">
                <div className="bg-orange-50 p-2.5 rounded-lg">
                  <AlertCircle className="w-5 h-5 text-orange-600" />
                </div>
                <div>
                  <p className="text-xs text-slate-500 uppercase tracking-wide font-medium">RMSE</p>
                  <p className="text-2xl font-bold text-slate-900 mt-0.5">
                    {modelMetrics.rmse.toFixed(2)}
                  </p>
                </div>
              </div>
            </div>
          </div>
        )}

        <div className="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
          <div className="border-b border-slate-200">
            <div className="flex">
              <button
                onClick={() => setActiveTab('predict')}
                className={`px-6 py-4 text-sm font-medium transition-colors relative ${
                  activeTab === 'predict'
                    ? 'text-blue-600 bg-blue-50'
                    : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50'
                }`}
              >
                Make Prediction
                {activeTab === 'predict' && (
                  <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-blue-600" />
                )}
              </button>
              <button
                onClick={() => setActiveTab('info')}
                className={`px-6 py-4 text-sm font-medium transition-colors relative ${
                  activeTab === 'info'
                    ? 'text-blue-600 bg-blue-50'
                    : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50'
                }`}
              >
                Model Information
                {activeTab === 'info' && (
                  <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-blue-600" />
                )}
              </button>
            </div>
          </div>

          <div className="p-6">
            {activeTab === 'predict' && (
              <>
                <PredictionForm
                  onSubmit={handlePredict}
                  loading={loading}
                  disabled={backendStatus !== 'online'}
                />
                {error && (
                  <div className="mt-6 bg-red-50 border border-red-200 rounded-lg p-4">
                    <div className="flex items-center gap-2">
                      <AlertCircle className="w-5 h-5 text-red-600" />
                      <p className="text-sm font-medium text-red-900">{error}</p>
                    </div>
                  </div>
                )}
                {prediction && <ResultsDisplay result={prediction} />}
              </>
            )}

            {activeTab === 'info' && modelMetrics && (
              <ModelInfo metrics={modelMetrics} />
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
