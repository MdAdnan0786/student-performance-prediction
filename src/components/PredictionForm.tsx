import { useState } from 'react';
import { Send } from 'lucide-react';

interface PredictionFormProps {
  onSubmit: (data: any) => void;
  loading: boolean;
  disabled: boolean;
}

function PredictionForm({ onSubmit, loading, disabled }: PredictionFormProps) {
  const [formData, setFormData] = useState({
    age: '18',
    gender: 'male',
    study_time_hours: '3',
    absences: '5',
    parental_education: 'college',
    previous_grade: '75',
    extracurricular: 'yes',
    sleep_hours: '7',
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    const data = {
      age: parseInt(formData.age),
      gender: formData.gender,
      study_time_hours: parseFloat(formData.study_time_hours),
      absences: parseInt(formData.absences),
      parental_education: formData.parental_education,
      previous_grade: parseFloat(formData.previous_grade),
      extracurricular: formData.extracurricular,
      sleep_hours: parseFloat(formData.sleep_hours),
    };

    onSubmit(data);
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-2">
            Age
          </label>
          <input
            type="number"
            name="age"
            value={formData.age}
            onChange={handleChange}
            min="15"
            max="25"
            required
            disabled={disabled}
            className="w-full px-4 py-2.5 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors disabled:bg-slate-50 disabled:text-slate-500"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-slate-700 mb-2">
            Gender
          </label>
          <select
            name="gender"
            value={formData.gender}
            onChange={handleChange}
            required
            disabled={disabled}
            className="w-full px-4 py-2.5 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors disabled:bg-slate-50 disabled:text-slate-500"
          >
            <option value="male">Male</option>
            <option value="female">Female</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-slate-700 mb-2">
            Study Time Per Day (hours)
          </label>
          <input
            type="number"
            name="study_time_hours"
            value={formData.study_time_hours}
            onChange={handleChange}
            min="0"
            max="12"
            step="0.5"
            required
            disabled={disabled}
            className="w-full px-4 py-2.5 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors disabled:bg-slate-50 disabled:text-slate-500"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-slate-700 mb-2">
            Absences (per semester)
          </label>
          <input
            type="number"
            name="absences"
            value={formData.absences}
            onChange={handleChange}
            min="0"
            max="50"
            required
            disabled={disabled}
            className="w-full px-4 py-2.5 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors disabled:bg-slate-50 disabled:text-slate-500"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-slate-700 mb-2">
            Parental Education Level
          </label>
          <select
            name="parental_education"
            value={formData.parental_education}
            onChange={handleChange}
            required
            disabled={disabled}
            className="w-full px-4 py-2.5 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors disabled:bg-slate-50 disabled:text-slate-500"
          >
            <option value="none">None</option>
            <option value="primary">Primary School</option>
            <option value="high school">High School</option>
            <option value="college">College</option>
            <option value="bachelor">Bachelor's Degree</option>
            <option value="master">Master's Degree</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-slate-700 mb-2">
            Previous Grade (0-100)
          </label>
          <input
            type="number"
            name="previous_grade"
            value={formData.previous_grade}
            onChange={handleChange}
            min="0"
            max="100"
            step="0.1"
            required
            disabled={disabled}
            className="w-full px-4 py-2.5 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors disabled:bg-slate-50 disabled:text-slate-500"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-slate-700 mb-2">
            Extracurricular Activities
          </label>
          <select
            name="extracurricular"
            value={formData.extracurricular}
            onChange={handleChange}
            required
            disabled={disabled}
            className="w-full px-4 py-2.5 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors disabled:bg-slate-50 disabled:text-slate-500"
          >
            <option value="yes">Yes</option>
            <option value="no">No</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-slate-700 mb-2">
            Sleep Hours Per Night
          </label>
          <input
            type="number"
            name="sleep_hours"
            value={formData.sleep_hours}
            onChange={handleChange}
            min="3"
            max="12"
            step="0.5"
            required
            disabled={disabled}
            className="w-full px-4 py-2.5 border border-slate-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors disabled:bg-slate-50 disabled:text-slate-500"
          />
        </div>
      </div>

      <div className="flex justify-end pt-4">
        <button
          type="submit"
          disabled={loading || disabled}
          className="inline-flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-blue-500 to-blue-600 text-white font-medium rounded-lg hover:from-blue-600 hover:to-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-lg shadow-blue-500/30"
        >
          {loading ? (
            <>
              <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
              Predicting...
            </>
          ) : (
            <>
              <Send className="w-5 h-5" />
              Predict Performance
            </>
          )}
        </button>
      </div>
    </form>
  );
}

export default PredictionForm;
