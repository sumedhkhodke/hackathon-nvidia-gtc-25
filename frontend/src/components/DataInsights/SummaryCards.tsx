import React from 'react';
import type { CategorySummary } from '../../types/index';

interface SummaryCardsProps {
  categories: CategorySummary[];
}

export const SummaryCards: React.FC<SummaryCardsProps> = ({ categories }) => {
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
      case 'sleep': return '#2196f3';
      case 'exercise': return '#ff9800';
      case 'work': return '#9c27b0';
      case 'mood': return '#76B900';
      default: return '#666';
    }
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      {categories.map((category) => (
        <div 
          key={category.category}
          className="metric-card hover:shadow-lg transition-shadow"
        >
          <div className="text-4xl mb-2" style={{ color: getCategoryColor(category.category) }}>
            {getCategoryIcon(category.category)}
          </div>
          <h3 className="text-3xl font-bold mb-1">
            {category.average_score.toFixed(1)}
          </h3>
          <p className="text-gray-600 text-sm mb-3">
            Avg {category.category.charAt(0).toUpperCase() + category.category.slice(1)} Score
          </p>
          <div className="text-xs text-gray-500 space-y-1">
            <div>Range: {category.min_score} - {category.max_score}</div>
            <div>Entries: {category.entry_count}</div>
          </div>
        </div>
      ))}
    </div>
  );
};
