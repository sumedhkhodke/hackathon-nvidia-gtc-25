import React from 'react';
import type { ReasoningStep } from '../../types/index';

interface ReasoningStepsProps {
  steps: ReasoningStep[];
}

export const ReasoningSteps: React.FC<ReasoningStepsProps> = ({ steps }) => {
  const getStepClass = (step: string): string => {
    if (step.includes('Safety')) {
      return 'safety-check';
    } else if (step.includes('ReAct')) {
      return 'react-cycle';
    } else if (step.includes('Synthesis')) {
      return 'synthesis';
    }
    return '';
  };

  const getStepIcon = (step: string): string => {
    if (step.includes('Safety')) {
      return '🛡️';
    } else if (step.includes('ReAct')) {
      return '🔄';
    } else if (step.includes('Synthesis')) {
      return '🎨';
    } else if (step.includes('Reason')) {
      return '🧠';
    } else if (step.includes('Act')) {
      return '⚡';
    } else if (step.includes('Observe')) {
      return '👁️';
    } else if (step.includes('Retrieved')) {
      return '📊';
    }
    return '•';
  };

  return (
    <div className="space-y-2">
      {steps.map((step, index) => (
        <div 
          key={index}
          className={`reasoning-step ${getStepClass(step.step)}`}
        >
          <div className="flex items-start gap-2">
            <span className="text-lg">{getStepIcon(step.step)}</span>
            <div className="flex-1">
              <div className="font-semibold text-sm text-nvidia-green">
                {step.step}
              </div>
              <div className="text-sm text-gray-700 mt-1">
                {step.description}
              </div>
            </div>
          </div>
        </div>
      ))}
    </div>
  );
};
