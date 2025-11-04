import React from 'react';

export const Header: React.FC = () => {
  return (
    <header className="bg-white border-b-2 border-gray-200 shadow-sm fixed top-0 left-0 right-0 z-20 h-16">
      <div className="px-6 h-full flex items-center justify-between">
        <div className="flex items-center gap-4">
          <h1 className="text-2xl font-bold text-gray-900">
            🟢 Agentic Lifelog
          </h1>
          <p className="text-sm text-gray-600 hidden lg:block">
            Your Personal AI Coach powered by NVIDIA Nemotron Multi-Agent System
          </p>
        </div>
        <div className="flex items-center gap-3">
          <div className="text-xs text-gray-500 hidden md:flex gap-3">
            <span>ReAct Pattern</span>
            <span>•</span>
            <span>Multi-Agent</span>
            <span>•</span>
            <span>Safety Guardrails</span>
            <span>•</span>
            <span>Agentic RAG</span>
          </div>
          <div className="bg-nvidia-green text-white px-3 py-1.5 rounded-lg text-xs font-semibold">
            🏆 NVIDIA GTC 2025
          </div>
        </div>
      </div>
    </header>
  );
};