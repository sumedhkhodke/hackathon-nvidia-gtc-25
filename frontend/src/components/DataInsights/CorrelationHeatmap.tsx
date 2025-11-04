import React from 'react';
import type { CorrelationData } from '../../types/index';

interface CorrelationHeatmapProps {
  data: CorrelationData;
}

export const CorrelationHeatmap: React.FC<CorrelationHeatmapProps> = ({ data }) => {
  const getColor = (value: number | null): string => {
    if (value === null) return '#f5f5f5';
    
    // Convert correlation value (-1 to 1) to color
    // Red for negative, green for positive
    const normalized = (value + 1) / 2; // Normalize to 0-1
    const hue = normalized * 120; // 0 (red) to 120 (green)
    const saturation = Math.abs(value) * 100; // Stronger correlation = more saturated
    
    return `hsl(${hue}, ${saturation}%, 50%)`;
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow">
      <h3 className="text-lg font-semibold mb-4">Category Correlation Matrix</h3>
      
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr>
              <th className="p-2"></th>
              {data.categories.map((category) => (
                <th 
                  key={category}
                  className="p-2 text-sm font-medium text-gray-700"
                >
                  {category.charAt(0).toUpperCase() + category.slice(1)}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {data.categories.map((rowCategory, rowIndex) => (
              <tr key={rowCategory}>
                <td className="p-2 text-sm font-medium text-gray-700">
                  {rowCategory.charAt(0).toUpperCase() + rowCategory.slice(1)}
                </td>
                {data.correlation_matrix[rowIndex].map((value, colIndex) => (
                  <td 
                    key={`${rowIndex}-${colIndex}`}
                    className="p-2 text-center"
                  >
                    <div
                      className="w-full h-10 rounded flex items-center justify-center text-white font-medium text-sm"
                      style={{ 
                        backgroundColor: getColor(value),
                        color: value !== null && Math.abs(value) > 0.5 ? 'white' : 'black'
                      }}
                      title={`Correlation: ${value !== null ? value.toFixed(3) : 'N/A'}`}
                    >
                      {value !== null ? value.toFixed(2) : '-'}
                    </div>
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="mt-4 flex items-center justify-center text-sm text-gray-600">
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2">
            <div 
              className="w-6 h-6 rounded"
              style={{ backgroundColor: 'hsl(0, 100%, 50%)' }}
            />
            <span>Strong negative</span>
          </div>
          <div className="flex items-center gap-2">
            <div 
              className="w-6 h-6 rounded"
              style={{ backgroundColor: 'hsl(60, 0%, 50%)' }}
            />
            <span>No correlation</span>
          </div>
          <div className="flex items-center gap-2">
            <div 
              className="w-6 h-6 rounded"
              style={{ backgroundColor: 'hsl(120, 100%, 50%)' }}
            />
            <span>Strong positive</span>
          </div>
        </div>
      </div>
    </div>
  );
};
