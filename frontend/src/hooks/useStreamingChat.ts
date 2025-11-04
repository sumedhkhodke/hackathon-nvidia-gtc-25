import { useState, useCallback } from 'react';
import type { ChatMessage } from '../types/index';

export const useStreamingChat = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isStreaming, setIsStreaming] = useState(false);
  const [currentStreamingMessage, setCurrentStreamingMessage] = useState<string>("");

  const sendMessage = useCallback(async (message: string) => {
    setIsStreaming(true);
    setCurrentStreamingMessage("");
    
    // Add user message
    const userMessage: ChatMessage = { 
      role: 'user', 
      content: message, 
      timestamp: new Date() 
    };
    setMessages(prev => [...prev, userMessage]);
    
    try {
      const response = await fetch('http://localhost:8000/api/chat/stream', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message })
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const reader = response.body?.getReader();
      if (!reader) {
        throw new Error('No reader available');
      }
      
      const decoder = new TextDecoder();
      
      let fullResponse = "";
      let reasoningSteps: any[] = [];
      let safetyChecks: any[] = [];
      
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        
        const chunk = decoder.decode(value, { stream: true });
        const lines = chunk.split('\n');
        
        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const data = JSON.parse(line.slice(6));
              
              if (data.type === 'intermediate') {
                // Update streaming message with node info
                if (data.data?.response) {
                  fullResponse = data.data.response;
                  setCurrentStreamingMessage(fullResponse);
                }
                if (data.data?.reasoning_steps) {
                  reasoningSteps = data.data.reasoning_steps;
                }
                if (data.data?.safety_checks) {
                  safetyChecks = data.data.safety_checks;
                }
                
                // Show intermediate states in streaming message
                if (data.node && !fullResponse) {
                  setCurrentStreamingMessage(`Processing: ${data.node}...`);
                }
              } else if (data.type === 'done') {
                // Add final message
                const assistantMessage: ChatMessage = {
                  role: 'assistant',
                  content: fullResponse || "I'm sorry, I couldn't generate a response.",
                  reasoning_steps: reasoningSteps.length > 0 ? reasoningSteps : undefined,
                  safety_checks: safetyChecks.length > 0 ? safetyChecks : undefined,
                  timestamp: new Date()
                };
                setMessages(prev => [...prev, assistantMessage]);
                setCurrentStreamingMessage("");
              } else if (data.type === 'error') {
                // Handle error
                const errorMessage: ChatMessage = {
                  role: 'assistant',
                  content: `Error: ${data.error || 'An unknown error occurred'}`,
                  timestamp: new Date()
                };
                setMessages(prev => [...prev, errorMessage]);
                setCurrentStreamingMessage("");
              }
            } catch (parseError) {
              console.error('Error parsing SSE data:', parseError);
            }
          }
        }
      }
    } catch (error) {
      console.error('Streaming error:', error);
      const errorMessage: ChatMessage = {
        role: 'assistant',
        content: `Error: ${error instanceof Error ? error.message : 'Failed to connect to server'}`,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsStreaming(false);
      setCurrentStreamingMessage("");
    }
  }, []);
  
  const clearMessages = useCallback(() => {
    setMessages([]);
    setCurrentStreamingMessage("");
  }, []);
  
  return { 
    messages, 
    isStreaming, 
    currentStreamingMessage, 
    sendMessage,
    clearMessages 
  };
};
