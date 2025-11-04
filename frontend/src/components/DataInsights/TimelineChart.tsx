import React from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts';
import type { TimelineDataPoint } from '../../types/index';

interface TimelineChartProps {
  data: TimelineDataPoint[];
}

export const TimelineChart: React.FC<TimelineChartProps> = ({ data }) => {
  // Transform data for Recharts
  const transformedData = data.reduce((acc: any[], point) => {
    const date = new Date(point.date).toLocaleDateString();
    const existingPoint = acc.find(p => p.date === date);
    
    if (existingPoint) {
      existingPoint[point.category] = point.mood_score;
    } else {
      acc.push({
        date,
        [point.category]: point.mood_score
      });
    }
    
    return acc;
  }, []);

  const categoryColors = {
    mood: '#76B900',
    sleep: '#2196f3',
    exercise: '#ff9800',
    work: '#9c27b0'
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow">
      <h3 className="text-lg font-semibold mb-4">Lifelog Timeline - All Categories</h3>
      <ResponsiveContainer width="100%" height={400}>
        <LineChart data={transformedData}>
          <CartesianGrid strokeDasharray="3 3" stroke="#e0e0e0" />
          <XAxis 
            dataKey="date" 
            angle={-45}
            textAnchor="end"
            height={60}
          />
          <YAxis 
            domain={[1, 5]}
            ticks={[1, 2, 3, 4, 5]}
            label={{ value: 'Score (1-5)', angle: -90, position: 'insideLeft' }}
          />
          <Tooltip 
            contentStyle={{
              backgroundColor: 'rgba(255, 255, 255, 0.95)',
              border: '1px solid #ccc',
              borderRadius: '8px'
            }}
          />
          <Legend />
          
          {Object.entries(categoryColors).map(([category, color]) => (
            <Line
              key={category}
              type="monotone"
              dataKey={category}
              stroke={color}
              strokeWidth={2}
              dot={{ r: 4 }}
              activeDot={{ r: 6 }}
              connectNulls
            />
          ))}
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};
