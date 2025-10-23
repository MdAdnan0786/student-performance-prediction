import { TrendingUp, Award, Target, Lightbulb } from 'lucide-react';

interface PredictionResult {
  predicted_grade: number;
  performance_level: string;
  confidence_score: number;
  model_used: string;
  recommendations: string[];
}

interface ResultsDisplayProps {
  result: PredictionResult;
}

function ResultsDisplay({ result }: ResultsDisplayProps) {
  const getGradeColor = (grade: number) => {
    if (grade >= 90) return 'from-green-500 to-green-600';
    if (grade >= 80) return 'from-blue-500 to-blue-600';
    if (grade >= 70) return 'from-yellow-500 to-yellow-600';
    if (grade >= 60) return 'from-orange-500 to-orange-600';
    return 'from-red-500 to-red-600';
  };

  const getPerformanceColor = (level: string) => {
    if (level === 'Excellent') return 'text-green-700 bg-green-50 border-green-200';
    if (level === 'Very Good') return 'text-blue-700 bg-blue-50 border-blue-200';
    if (level === 'Good') return 'text-yellow-700 bg-yellow-50 border-yellow-200';
    if (level === 'Satisfactory') return 'text-orange-700 bg-orange-50 border-orange-200';
    return 'text-red-700 bg-red-50 border-red-200';
  };

  return (
    <div className="mt-8 space-y-6">
      <div className="bg-gradient-to-br from-slate-50 to-slate-100 rounded-xl p-6 border-2 border-slate-200">
        <h3 className="text-lg font-semibold text-slate-900 mb-6 flex items-center gap-2">
          <TrendingUp className="w-5 h-5 text-blue-600" />
          Prediction Results
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-white rounded-xl p-6 shadow-sm border border-slate-200">
            <div className="flex items-center justify-between mb-4">
              <span className="text-sm font-medium text-slate-600">Predicted Grade</span>
              <Award className="w-5 h-5 text-slate-400" />
            </div>
            <div className={`text-5xl font-bold bg-gradient-to-br ${getGradeColor(result.predicted_grade)} bg-clip-text text-transparent mb-2`}>
              {result.predicted_grade.toFixed(1)}
            </div>
            <div className="w-full bg-slate-200 rounded-full h-2.5 mt-3">
              <div
                className={`h-2.5 rounded-full bg-gradient-to-r ${getGradeColor(result.predicted_grade)}`}
                style={{ width: `${result.predicted_grade}%` }}
              />
            </div>
          </div>

          <div className="bg-white rounded-xl p-6 shadow-sm border border-slate-200">
            <div className="flex items-center justify-between mb-4">
              <span className="text-sm font-medium text-slate-600">Performance Level</span>
              <Target className="w-5 h-5 text-slate-400" />
            </div>
            <div className={`inline-flex px-4 py-2 rounded-lg border font-semibold text-lg ${getPerformanceColor(result.performance_level)}`}>
              {result.performance_level}
            </div>
            <p className="text-sm text-slate-500 mt-4">
              Model: <span className="font-medium text-slate-700">{result.model_used}</span>
            </p>
          </div>

          <div className="bg-white rounded-xl p-6 shadow-sm border border-slate-200">
            <div className="flex items-center justify-between mb-4">
              <span className="text-sm font-medium text-slate-600">Confidence Score</span>
              <TrendingUp className="w-5 h-5 text-slate-400" />
            </div>
            <div className="text-5xl font-bold text-slate-900 mb-2">
              {(result.confidence_score * 100).toFixed(0)}%
            </div>
            <div className="w-full bg-slate-200 rounded-full h-2.5 mt-3">
              <div
                className="h-2.5 rounded-full bg-gradient-to-r from-blue-500 to-blue-600"
                style={{ width: `${result.confidence_score * 100}%` }}
              />
            </div>
          </div>
        </div>
      </div>

      {result.recommendations && result.recommendations.length > 0 && (
        <div className="bg-white rounded-xl p-6 shadow-sm border border-slate-200">
          <h4 className="text-lg font-semibold text-slate-900 mb-4 flex items-center gap-2">
            <Lightbulb className="w-5 h-5 text-amber-500" />
            Personalized Recommendations
          </h4>
          <ul className="space-y-3">
            {result.recommendations.map((recommendation, index) => (
              <li
                key={index}
                className="flex items-start gap-3 p-4 bg-slate-50 rounded-lg border border-slate-200 hover:bg-slate-100 transition-colors"
              >
                <div className="flex-shrink-0 w-6 h-6 rounded-full bg-blue-500 text-white flex items-center justify-center text-xs font-bold mt-0.5">
                  {index + 1}
                </div>
                <p className="text-sm text-slate-700 leading-relaxed">{recommendation}</p>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default ResultsDisplay;
