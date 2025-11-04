import React from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell
} from 'recharts';
import type { CategorySummary } from '../../types/index';

interface CategoryChartProps {
  data: CategorySummary[];
}

export const CategoryChart: React.FC<CategoryChartProps> = ({ data }) => {
  const categoryColors: Record<string, string> = {
    mood: '#76B900',
    sleep: '#2196f3',
    exercise: '#ff9800',
    work: '#9c27b0'
  };

  const chartData = data.map(item => ({
    category: item.category.charAt(0).toUpperCase() + item.category.slice(1),
    score: item.average_score,
    color: categoryColors[item.category] || '#666'
  }));

  return (
    <div className="bg-white p-6 rounded-lg shadow">
      <h3 className="text-lg font-semibold mb-4">Average Score by Category</h3>
      <ResponsiveContainer width="100%" height={400}>
        <BarChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" stroke="#e0e0e0" />
          <XAxis dataKey="category" />
          <YAxis 
            domain={[0, 5]}
            ticks={[0, 1, 2, 3, 4, 5]}
            label={{ value: 'Average Score', angle: -90, position: 'insideLeft' }}
          />
          <Tooltip 
            contentStyle={{
              backgroundColor: 'rgba(255, 255, 255, 0.95)',
              border: '1px solid #ccc',
              borderRadius: '8px'
            }}
            formatter={(value: number) => value.toFixed(2)}
          />
          <Bar dataKey="score" radius={[8, 8, 0, 0]}>
            {chartData.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={entry.color} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};
