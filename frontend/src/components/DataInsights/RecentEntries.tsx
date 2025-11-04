import React from 'react';
import type { LifelogEntry } from '../../types/index';

interface RecentEntriesProps {
  entries: LifelogEntry[];
}

export const RecentEntries: React.FC<RecentEntriesProps> = ({ entries }) => {
  const getCategoryIcon = (category: string): string => {
    switch (category) {
      case 'sleep': return '😴';
      case 'exercise': return '🏃';
      case 'work': return '💼';
      case 'mood': return '😊';
      default: return '📊';
    }
  };

  const getCategoryColor = (category: string): string => {
    switch (category) {
      case 'sleep': return 'text-blue-600';
      case 'exercise': return 'text-orange-600';
      case 'work': return 'text-purple-600';
      case 'mood': return 'text-nvidia-green';
      default: return 'text-gray-600';
    }
  };

  const getMoodColor = (score: number): string => {
    if (score >= 4) return 'text-green-600';
    if (score >= 3) return 'text-yellow-600';
    return 'text-red-600';
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow">
      <h3 className="text-lg font-semibold mb-4">📝 Recent Lifelog Entries</h3>
      
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="border-b border-gray-200">
              <th className="text-left p-3 font-medium text-gray-700">Date</th>
              <th className="text-left p-3 font-medium text-gray-700">Category</th>
              <th className="text-left p-3 font-medium text-gray-700">Entry</th>
              <th className="text-center p-3 font-medium text-gray-700">Mood Score</th>
            </tr>
          </thead>
          <tbody>
            {entries.map((entry, index) => (
              <tr 
                key={index}
                className="border-b border-gray-100 hover:bg-gray-50 transition-colors"
              >
                <td className="p-3 text-sm text-gray-600">
                  {new Date(entry.date).toLocaleDateString()}
                </td>
                <td className="p-3">
                  <span className={`font-medium ${getCategoryColor(entry.category)}`}>
                    {getCategoryIcon(entry.category)} {entry.category}
                  </span>
                </td>
                <td className="p-3 text-sm text-gray-700 max-w-md">
                  <div className="truncate" title={entry.entry}>
                    {entry.entry}
                  </div>
                </td>
                <td className="p-3 text-center">
                  <span className={`font-bold text-lg ${getMoodColor(entry.mood_score)}`}>
                    {entry.mood_score}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {entries.length === 0 && (
        <div className="text-center py-8 text-gray-500">
          No entries found
        </div>
      )}
    </div>
  );
};
