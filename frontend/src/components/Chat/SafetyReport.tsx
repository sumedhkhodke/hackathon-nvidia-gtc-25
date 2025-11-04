import React from 'react';
import type { SafetyCheck } from '../../types/index';

interface SafetyReportProps {
  checks: SafetyCheck[];
}

export const SafetyReport: React.FC<SafetyReportProps> = ({ checks }) => {
  return (
    <div className="bg-gray-50 rounded-lg p-4 space-y-2">
      {checks.map((check, index) => {
        const icon = check.is_safe ? '✅' : '⚠️';
        const status = check.is_safe ? 'Passed' : 'Flagged';
        const bgColor = check.is_safe ? 'bg-green-100' : 'bg-yellow-100';
        const textColor = check.is_safe ? 'text-green-800' : 'text-yellow-800';

        return (
          <div 
            key={index}
            className={`${bgColor} rounded p-3 flex items-start gap-2`}
          >
            <span className="text-lg">{icon}</span>
            <div className="flex-1">
              <div className={`font-medium ${textColor}`}>
                {check.type.toUpperCase()} Check: {status}
              </div>
              {check.category && (
                <div className="text-sm mt-1 text-gray-600">
                  Category: {check.category}
                </div>
              )}
              {check.should_block && (
                <div className="text-sm mt-1 font-medium text-red-600">
                  Action: Message blocked
                </div>
              )}
              {check.needs_modification && (
                <div className="text-sm mt-1 text-yellow-600">
                  Note: Response may need modification
                </div>
              )}
            </div>
          </div>
        );
      })}
    </div>
  );
};
