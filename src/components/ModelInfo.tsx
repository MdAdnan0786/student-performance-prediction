import { BarChart3, Database, Target, TrendingUp } from 'lucide-react';

interface ModelMetrics {
  model_name: string;
  r2_score: number;
  rmse: number;
  mae: number;
  training_samples: number;
  test_samples: number;
}

interface ModelInfoProps {
  metrics: ModelMetrics;
}

function ModelInfo({ metrics }: ModelInfoProps) {
  return (
    <div className="space-y-6">
      <div>
        <h3 className="text-xl font-bold text-slate-900 mb-2">Model Overview</h3>
        <p className="text-slate-600">
          This system uses machine learning to predict student academic performance based on multiple factors.
          The model is trained on a combined dataset from three sources and uses ensemble methods for accurate predictions.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-gradient-to-br from-blue-50 to-blue-100 rounded-xl p-6 border border-blue-200">
          <div className="flex items-center gap-3 mb-4">
            <div className="bg-blue-500 p-2 rounded-lg">
              <BarChart3 className="w-6 h-6 text-white" />
            </div>
            <div>
              <h4 className="font-semibold text-slate-900">Model Type</h4>
              <p className="text-sm text-slate-600">Algorithm Used</p>
            </div>
          </div>
          <p className="text-2xl font-bold text-slate-900">{metrics.model_name}</p>
          <p className="text-sm text-slate-600 mt-2">
            {metrics.model_name === 'Random Forest'
              ? 'Ensemble method using multiple decision trees for robust predictions'
              : 'Sequential ensemble technique building models iteratively'}
          </p>
        </div>

        <div className="bg-gradient-to-br from-green-50 to-green-100 rounded-xl p-6 border border-green-200">
          <div className="flex items-center gap-3 mb-4">
            <div className="bg-green-500 p-2 rounded-lg">
              <Target className="w-6 h-6 text-white" />
            </div>
            <div>
              <h4 className="font-semibold text-slate-900">R² Score</h4>
              <p className="text-sm text-slate-600">Model Accuracy</p>
            </div>
          </div>
          <p className="text-2xl font-bold text-slate-900">
            {(metrics.r2_score * 100).toFixed(2)}%
          </p>
          <p className="text-sm text-slate-600 mt-2">
            The model explains {(metrics.r2_score * 100).toFixed(1)}% of variance in student grades
          </p>
        </div>

        <div className="bg-gradient-to-br from-orange-50 to-orange-100 rounded-xl p-6 border border-orange-200">
          <div className="flex items-center gap-3 mb-4">
            <div className="bg-orange-500 p-2 rounded-lg">
              <TrendingUp className="w-6 h-6 text-white" />
            </div>
            <div>
              <h4 className="font-semibold text-slate-900">Error Metrics</h4>
              <p className="text-sm text-slate-600">Prediction Accuracy</p>
            </div>
          </div>
          <div className="space-y-2">
            <div className="flex justify-between items-center">
              <span className="text-sm text-slate-600">RMSE:</span>
              <span className="font-bold text-slate-900">{metrics.rmse.toFixed(2)}</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-slate-600">MAE:</span>
              <span className="font-bold text-slate-900">{metrics.mae.toFixed(2)}</span>
            </div>
          </div>
          <p className="text-sm text-slate-600 mt-3">
            Average prediction error: ±{metrics.mae.toFixed(1)} points
          </p>
        </div>

        <div className="bg-gradient-to-br from-purple-50 to-purple-100 rounded-xl p-6 border border-purple-200">
          <div className="flex items-center gap-3 mb-4">
            <div className="bg-purple-500 p-2 rounded-lg">
              <Database className="w-6 h-6 text-white" />
            </div>
            <div>
              <h4 className="font-semibold text-slate-900">Dataset Size</h4>
              <p className="text-sm text-slate-600">Training & Testing</p>
            </div>
          </div>
          <div className="space-y-2">
            <div className="flex justify-between items-center">
              <span className="text-sm text-slate-600">Training:</span>
              <span className="font-bold text-slate-900">{metrics.training_samples}</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-slate-600">Testing:</span>
              <span className="font-bold text-slate-900">{metrics.test_samples}</span>
            </div>
          </div>
          <p className="text-sm text-slate-600 mt-3">
            Total samples: {metrics.training_samples + metrics.test_samples}
          </p>
        </div>
      </div>

      <div className="bg-slate-50 rounded-xl p-6 border border-slate-200">
        <h4 className="font-semibold text-slate-900 mb-3">Features Used for Prediction</h4>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
          {[
            'Age',
            'Gender',
            'Study Time',
            'Absences',
            'Parental Education',
            'Previous Grade',
            'Extracurricular',
            'Sleep Hours'
          ].map((feature, index) => (
            <div
              key={index}
              className="bg-white px-3 py-2 rounded-lg border border-slate-200 text-sm font-medium text-slate-700 text-center"
            >
              {feature}
            </div>
          ))}
        </div>
      </div>

      <div className="bg-blue-50 border border-blue-200 rounded-xl p-6">
        <h4 className="font-semibold text-slate-900 mb-3">About the Data Sources</h4>
        <ul className="space-y-2 text-sm text-slate-700">
          <li className="flex items-start gap-2">
            <span className="text-blue-600 font-bold">1.</span>
            <span>Student Lifestyle Dataset - Demographics and lifestyle factors</span>
          </li>
          <li className="flex items-start gap-2">
            <span className="text-blue-600 font-bold">2.</span>
            <span>Student Performance Data - Academic records and family background</span>
          </li>
          <li className="flex items-start gap-2">
            <span className="text-blue-600 font-bold">3.</span>
            <span>Student Performance Predictions - Behavioral and academic patterns</span>
          </li>
        </ul>
      </div>
    </div>
  );
}

export default ModelInfo;
