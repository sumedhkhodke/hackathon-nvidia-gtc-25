import React, { useState, useRef, useEffect } from 'react';
import { Send, Loader2 } from 'lucide-react';
import { useStreamingChat } from '../../hooks/useStreamingChat';
import { ChatMessage } from './ChatMessage';

interface SimpleStreamingChatProps {
  demoQuestion?: string | null;
  onDemoQuestionHandled?: () => void;
}

export const SimpleStreamingChat: React.FC<SimpleStreamingChatProps> = ({ 
  demoQuestion, 
  onDemoQuestionHandled 
}) => {
  const { messages, isStreaming, currentStreamingMessage, sendMessage } = useStreamingChat();
  const [input, setInput] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);
  
  // Show welcome message if no messages
  const showWelcome = messages.length === 0;
  
  // Handle demo questions - auto send them
  useEffect(() => {
    if (demoQuestion && !isStreaming) {
      setInput(demoQuestion);
      // Auto-send the demo question
      setTimeout(() => {
        sendMessage(demoQuestion);
        setInput('');
        onDemoQuestionHandled?.();
        // Scroll to bottom after sending demo question
        setTimeout(() => {
          messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
        }, 100);
      }, 100);
    }
  }, [demoQuestion, isStreaming, sendMessage, onDemoQuestionHandled]);
  
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (input.trim() && !isStreaming) {
      sendMessage(input);
      setInput('');
      // Scroll to bottom only when user sends a message
      setTimeout(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
      }, 100);
    }
  };
  
  // Don't auto-scroll - let user control their position
  // Only scroll on initial load if there are messages
  useEffect(() => {
    if (messages.length === 1) {
      messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }
  }, []);
  
  return (
    <div className="flex flex-col h-full relative">
      {/* Messages Container - Only this scrolls */}
      <div className="absolute top-0 bottom-20 left-0 right-0 overflow-y-auto p-6 space-y-4 chat-scroll">
        {showWelcome && (
          <div className="flex items-center justify-center min-h-[60vh]">
            <div className="text-center max-w-3xl">
              <h2 className="text-3xl font-bold text-gray-900 mb-3">Welcome to Your AI Life Coach! 🤖</h2>
              <p className="text-lg text-gray-600 mb-6">I'm powered by NVIDIA Nemotron and ready to help you analyze your lifelog data.</p>
              <div className="bg-gray-50 border-2 border-gray-200 rounded-xl p-6 text-left">
                <p className="text-base font-semibold text-gray-800 mb-3">I can help you with:</p>
                <ul className="text-gray-700 space-y-2">
                  <li className="flex items-start gap-2">
                    <span className="text-nvidia-green mt-1">•</span>
                    <span>Analyzing patterns in your sleep, mood, and exercise data</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-nvidia-green mt-1">•</span>
                    <span>Finding correlations between different aspects of your life</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-nvidia-green mt-1">•</span>
                    <span>Providing personalized recommendations based on your data</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-nvidia-green mt-1">•</span>
                    <span>Answering questions about your daily habits and trends</span>
                  </li>
                </ul>
                <div className="mt-4 p-3 bg-white rounded-lg border border-gray-200">
                  <p className="text-sm text-gray-600 italic">
                    💡 Try asking: <span className="text-gray-800 font-medium">"What patterns do you see in my sleep?"</span> or <span className="text-gray-800 font-medium">"How does exercise impact my mood?"</span>
                  </p>
                </div>
              </div>
            </div>
          </div>
        )}
        
        {messages.map((message, idx) => (
          <ChatMessage key={idx} message={message} />
        ))}
        
        {/* Streaming Indicator */}
        {isStreaming && currentStreamingMessage && (
          <div className="flex gap-3 bg-gray-50 rounded-lg p-4 shadow-sm border border-gray-200">
            <div className="flex-shrink-0">
              <div className="w-8 h-8 rounded-full bg-nvidia-green flex items-center justify-center">
                <Loader2 className="w-5 h-5 text-white animate-spin" />
              </div>
            </div>
            <div className="flex-1 space-y-2">
              <div className="flex items-center gap-2">
                <span className="font-semibold text-sm">lifelog-assistant</span>
                <span className="text-xs text-gray-500 italic">Thinking...</span>
              </div>
              <div className="text-gray-800 whitespace-pre-wrap text-sm">{currentStreamingMessage}</div>
            </div>
          </div>
        )}
        
        {isStreaming && !currentStreamingMessage && (
          <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-4">
            <div className="flex items-center gap-3">
              <Loader2 className="w-5 h-5 animate-spin text-nvidia-green" />
              <span className="text-gray-600">Thinking...</span>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>
      
      {/* Input Form - Fixed at bottom */}
      <div className="absolute bottom-0 left-0 right-0 border-t-2 border-gray-200 bg-white p-3">
        <div className="max-w-4xl mx-auto">
          <form onSubmit={handleSubmit} className="flex gap-2">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              disabled={isStreaming}
              className="flex-1 px-4 py-2.5 border-2 border-gray-300 rounded-xl 
                       focus:outline-none focus:ring-2 focus:ring-nvidia-green focus:border-nvidia-green
                       disabled:bg-gray-100 disabled:cursor-not-allowed
                       transition-all duration-200 text-base"
              placeholder={isStreaming ? "Processing your request..." : "Type your message and press Enter or click Send..."}
              autoFocus
            />
            <button
              type="submit"
              disabled={isStreaming || !input.trim()}
              className="px-5 py-2.5 bg-nvidia-green text-white rounded-xl font-medium
                       hover:bg-green-600 transition-colors shadow-md hover:shadow-lg
                       disabled:bg-gray-300 disabled:cursor-not-allowed disabled:shadow-none
                       flex items-center gap-2"
              title={isStreaming ? "Processing..." : !input.trim() ? "Type a message first" : "Send message"}
            >
              {isStreaming ? (
                <Loader2 className="w-5 h-5 animate-spin" />
              ) : (
                <Send className="w-5 h-5" />
              )}
              <span className="hidden sm:inline">Send</span>
            </button>
          </form>
          <p className="mt-2 text-xs text-gray-500 text-center">
            Powered by NVIDIA NeMo
          </p>
        </div>
      </div>
    </div>
  );
};
