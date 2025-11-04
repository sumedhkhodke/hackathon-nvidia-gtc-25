import React, { useState, useMemo } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { ChevronDown, ChevronRight, User, Bot, Brain, Shield } from 'lucide-react';
import type { ChatMessage as ChatMessageType } from '../../types/index';

interface ChatMessageProps {
  message: ChatMessageType;
}

export const ChatMessage: React.FC<ChatMessageProps> = ({ message }) => {
  const [showThinking, setShowThinking] = useState(false);
  const [showReasoningSteps, setShowReasoningSteps] = useState(false);
  const [showSafetyChecks, setShowSafetyChecks] = useState(false);
  
  const isAssistant = message.role === 'assistant';
  
  // Extract thinking content and calculate time using useMemo to avoid re-renders
  const { thinking, mainContent, thinkingTime } = useMemo(() => {
    const thinkRegex = /<think>([\s\S]*?)<\/think>/;
    const match = message.content.match(thinkRegex);
    if (match) {
      // Estimate thinking time based on content length (rough approximation)
      const thinkingContent = match[1].trim();
      const estimatedTime = Math.max(0.1, Math.min(2.5, thinkingContent.length / 1000));
      return {
        thinking: thinkingContent,
        mainContent: message.content.replace(thinkRegex, '').trim(),
        thinkingTime: estimatedTime
      };
    }
    return { thinking: null, mainContent: message.content, thinkingTime: null };
  }, [message.content]);
  
  // Format thinking time display
  const formatThinkingTime = () => {
    if (!thinkingTime) return "Thought for less than a second";
    if (thinkingTime < 1) return `Thought for ${(thinkingTime * 1000).toFixed(0)} milliseconds`;
    return `Thought for ${thinkingTime.toFixed(1)} seconds`;
  };
  
  if (!isAssistant) {
    // User message - right aligned
    return (
      <div className="flex justify-end message-appear">
        <div className="max-w-3xl">
          <div className="flex gap-3 bg-blue-50 rounded-lg p-4 shadow-sm border border-blue-200">
            <div className="flex-1">
              <div className="flex items-center gap-2 justify-end mb-2">
                <span className="text-xs text-gray-500">
                  {new Date(message.timestamp).toLocaleTimeString()}
                </span>
                <span className="font-semibold text-sm">You</span>
              </div>
              <div className="text-right text-gray-800">
                {message.content}
              </div>
            </div>
            <div className="flex-shrink-0">
              <div className="w-8 h-8 rounded-full bg-blue-500 flex items-center justify-center">
                <User className="w-5 h-5 text-white" />
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }
  
  // Assistant message - left aligned
  return (
    <div className="flex gap-3 bg-gray-50 rounded-lg p-4 shadow-sm border border-gray-200 max-w-4xl message-appear">
      <div className="flex-shrink-0">
        {isAssistant ? (
          <div className="w-8 h-8 rounded-full bg-nvidia-green flex items-center justify-center">
            <Bot className="w-5 h-5 text-white" />
          </div>
        ) : (
          <div className="w-8 h-8 rounded-full bg-blue-500 flex items-center justify-center">
            <User className="w-5 h-5 text-white" />
          </div>
        )}
      </div>
      
      <div className="flex-1 space-y-2">
        <div className="flex items-center gap-2">
          <span className="font-semibold text-sm">
            {isAssistant ? 'lifelog-assistant' : 'You'}
          </span>
          <span className="text-xs text-gray-500">
            {new Date(message.timestamp).toLocaleTimeString()}
          </span>
        </div>
        
        {/* Collapsible Thinking Section */}
        {thinking && isAssistant && (
          <div className="border-l-2 border-gray-300 pl-3 mb-3">
            <button
              onClick={() => setShowThinking(!showThinking)}
              className="flex items-center gap-1 text-sm text-gray-600 hover:text-gray-800 mb-1"
            >
              {showThinking ? <ChevronDown className="w-3 h-3" /> : <ChevronRight className="w-3 h-3" />}
              <span className="italic">{formatThinkingTime()}</span>
            </button>
            {showThinking && (
              <div className="text-sm text-gray-600 bg-gray-100 p-2 rounded mt-1 italic">
                {thinking}
              </div>
            )}
          </div>
        )}
        
        {/* Main Message Content with Markdown */}
        <div className="prose prose-sm max-w-none">
          <ReactMarkdown
            remarkPlugins={[remarkGfm]}
            components={{
              h1: ({children}) => <h1 className="text-xl font-bold mt-4 mb-2">{children}</h1>,
              h2: ({children}) => <h2 className="text-lg font-bold mt-3 mb-2">{children}</h2>,
              h3: ({children}) => <h3 className="text-base font-bold mt-2 mb-1">{children}</h3>,
              p: ({children}) => <p className="mb-3 leading-relaxed">{children}</p>,
              ul: ({children}) => <ul className="list-disc pl-5 mb-3 space-y-1">{children}</ul>,
              ol: ({children}) => <ol className="list-decimal pl-5 mb-3 space-y-1">{children}</ol>,
              li: ({children}) => <li className="leading-relaxed">{children}</li>,
              strong: ({children}) => <strong className="font-semibold text-gray-900">{children}</strong>,
              code: ({children, ...props}) => {
                const inline = !('className' in props && props.className?.includes('language-'));
                return inline ? (
                  <code className="px-1 py-0.5 bg-gray-100 text-sm rounded">{children}</code>
                ) : (
                  <pre className="block p-3 bg-gray-900 text-gray-100 rounded-lg overflow-x-auto">
                    <code>{children}</code>
                  </pre>
                );
              },
              blockquote: ({children}) => (
                <blockquote className="border-l-4 border-gray-300 pl-4 italic my-3">{children}</blockquote>
              ),
            }}
          >
            {mainContent}
          </ReactMarkdown>
        </div>
        
        {/* Reasoning Steps (if present) */}
        {message.reasoning_steps && message.reasoning_steps.length > 0 && (
          <div className="mt-3 border-t pt-3">
            <button
              onClick={() => setShowReasoningSteps(!showReasoningSteps)}
              className="flex items-center gap-2 text-sm font-medium text-gray-700 hover:text-gray-900"
            >
              {showReasoningSteps ? <ChevronDown className="w-4 h-4" /> : <ChevronRight className="w-4 h-4" />}
              <Brain className="w-4 h-4" />
              Reasoning Steps ({message.reasoning_steps.length})
            </button>
            {showReasoningSteps && (
              <div className="mt-2 space-y-2">
                {message.reasoning_steps.map((step, idx) => (
                  <div key={idx} className="flex gap-2 text-sm bg-blue-50 p-2 rounded">
                    <span className="font-medium text-blue-700">{step.step}:</span>
                    <span className="text-gray-700">{step.description}</span>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
        
        {/* Safety Checks (if present) */}
        {message.safety_checks && message.safety_checks.length > 0 && (
          <div className="mt-3 border-t pt-3">
            <button
              onClick={() => setShowSafetyChecks(!showSafetyChecks)}
              className="flex items-center gap-2 text-sm font-medium text-gray-700 hover:text-gray-900"
            >
              {showSafetyChecks ? <ChevronDown className="w-4 h-4" /> : <ChevronRight className="w-4 h-4" />}
              <Shield className="w-4 h-4" />
              Safety Checks ({message.safety_checks.length})
            </button>
            {showSafetyChecks && (
              <div className="mt-2 space-y-2">
                {message.safety_checks.map((check, idx) => (
                  <div key={idx} className="flex items-center gap-2 text-sm bg-green-50 p-2 rounded">
                    <span className={`w-2 h-2 rounded-full ${check.is_safe ? 'bg-green-500' : 'bg-red-500'}`} />
                    <span className="font-medium">{check.type}:</span>
                    <span className="text-gray-700">
                      {check.is_safe ? '✓ Safe' : '⚠ Needs Review'}
                    </span>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
        
        {/* Metrics (if present) */}
        {message.metrics && Object.keys(message.metrics).length > 0 && (
          <div className="flex gap-4 text-xs text-gray-500 mt-2">
            {message.metrics.react_cycles !== undefined && (
              <span>🔄 {message.metrics.react_cycles} cycles</span>
            )}
            {message.metrics.retrieved_entries !== undefined && (
              <span>📚 {message.metrics.retrieved_entries} entries</span>
            )}
            {message.metrics.elapsed_time !== undefined && (
              <span>⏱️ {message.metrics.elapsed_time.toFixed(1)}s</span>
            )}
          </div>
        )}
      </div>
    </div>
  );
};