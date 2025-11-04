import React, { useState } from 'react';
import { ChevronRight, ChevronDown } from 'lucide-react';
import { useChatStore } from '../../store/chatStore';

interface SidebarProps {
  onDemoQuestionClick: (question: string) => void;
  stats: {
    total_entries: number;
  };
}

export const Sidebar: React.FC<SidebarProps> = ({ onDemoQuestionClick, stats }) => {
  const { sidebarOpen, setSidebarOpen } = useChatStore();
  const [expandedSections, setExpandedSections] = useState({
    quickDemo: true,
    systemStatus: true,
    activeAgents: false,
    architecture: false
  });
  
  const toggleSection = (section: keyof typeof expandedSections) => {
    setExpandedSections(prev => ({
      ...prev,
      [section]: !prev[section]
    }));
  };

  const demoQuestions = [
    "What patterns do you see in my sleep?",
    "How does exercise impact my mood and energy levels?",
    "What's the relationship between my work hours and mood?",
    "When do I feel most productive during the day?"
  ];

  const agents = [
    { name: "Super 49B v1.5", icon: "🧠" },
    { name: "Safety 8B v3", icon: "🛡️" },
    { name: "Nano 9B v2", icon: "⚡" },
    { name: "ReAct", icon: "🔄" }
  ];

  if (!sidebarOpen) {
    return (
      <aside className="w-16 bg-gray-50 border-r-2 border-gray-200 flex flex-col items-center py-4 fixed left-0 top-16 bottom-0 z-10">
        <button
          onClick={() => setSidebarOpen(true)}
          className="p-2 hover:bg-gray-200 rounded-lg transition-colors"
        >
          <ChevronRight className="w-6 h-6" />
        </button>
      </aside>
    );
  }

  return (
    <aside className="w-72 bg-gray-50 border-r-2 border-gray-200 flex flex-col h-full fixed left-0 top-16 bottom-0 z-10">
      {/* NVIDIA Logo */}
      <div className="p-3 border-b border-gray-200 flex items-center justify-between bg-white">
        <div className="flex items-center gap-2">
          {/* Official NVIDIA Logo */}
          <img 
            src="/images/NVIDIA-logo-white-16x9.png" 
            alt="NVIDIA" 
            className="h-10 object-contain"
          />
        </div>
        <button
          onClick={() => setSidebarOpen(false)}
          className="hover:bg-gray-200 p-1 rounded transition-colors"
          title="Collapse sidebar"
        >
          <ChevronRight className="w-4 h-4 rotate-180" />
        </button>
      </div>

      <div className="flex-1 overflow-y-auto custom-scrollbar">
        {/* Quick Demo Section */}
        <div className="border-b border-gray-200">
          <button
            onClick={() => toggleSection('quickDemo')}
            className="w-full px-4 py-3 flex items-center justify-between hover:bg-gray-100 transition-colors"
          >
            <span className="font-semibold text-gray-800">🚀 Quick Demo</span>
            {expandedSections.quickDemo ? <ChevronDown className="w-4 h-4" /> : <ChevronRight className="w-4 h-4" />}
          </button>
          {expandedSections.quickDemo && (
            <div className="px-4 pb-3 space-y-2">
              <p className="text-xs text-gray-600">Click to try:</p>
              {demoQuestions.map((question, idx) => (
                <button
                  key={idx}
                  onClick={() => onDemoQuestionClick(question)}
                  className="w-full text-left text-sm p-2 bg-white border border-gray-200 rounded hover:bg-gray-100 hover:border-nvidia-green transition-all break-words whitespace-normal"
                  title={question}
                >
                  💡 {question}
                </button>
              ))}
            </div>
          )}
        </div>

        {/* System Status Section */}
        <div className="border-b border-gray-200">
          <button
            onClick={() => toggleSection('systemStatus')}
            className="w-full px-4 py-3 flex items-center justify-between hover:bg-gray-100 transition-colors"
          >
            <span className="font-semibold text-gray-800">📊 System Status</span>
            {expandedSections.systemStatus ? <ChevronDown className="w-4 h-4" /> : <ChevronRight className="w-4 h-4" />}
          </button>
          {expandedSections.systemStatus && (
            <div className="px-4 pb-3">
              <div className="bg-gradient-to-br from-nvidia-green to-green-600 text-white p-4 rounded-lg text-center shadow-md">
                <div className="text-3xl font-bold">{stats.total_entries}</div>
                <div className="text-sm mt-1">Lifelog Entries</div>
              </div>
            </div>
          )}
        </div>

        {/* Active Agents Section */}
        <div className="border-b border-gray-200">
          <button
            onClick={() => toggleSection('activeAgents')}
            className="w-full px-4 py-3 flex items-center justify-between hover:bg-gray-100 transition-colors"
          >
            <span className="font-semibold text-gray-800">🤖 Active Agents</span>
            {expandedSections.activeAgents ? <ChevronDown className="w-4 h-4" /> : <ChevronRight className="w-4 h-4" />}
          </button>
          {expandedSections.activeAgents && (
            <div className="px-4 pb-3 space-y-2">
              {agents.map((agent, idx) => (
                <div key={idx} className="flex items-center gap-2 p-2 bg-white rounded border border-gray-200">
                  <span>{agent.icon}</span>
                  <span className="text-sm text-gray-700">{agent.name}</span>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Architecture Section */}
        <div className="border-b border-gray-200">
          <button
            onClick={() => toggleSection('architecture')}
            className="w-full px-4 py-3 flex items-center justify-between hover:bg-gray-100 transition-colors"
          >
            <span className="font-semibold text-gray-800">🏗️ Architecture</span>
            {expandedSections.architecture ? <ChevronDown className="w-4 h-4" /> : <ChevronRight className="w-4 h-4" />}
          </button>
          {expandedSections.architecture && (
            <div className="px-4 pb-3 text-sm text-gray-700 space-y-2">
              <div className="bg-white p-3 rounded border border-gray-200">
                <p className="font-semibold mb-2">Multi-Agent Workflow:</p>
                <ol className="list-decimal list-inside text-xs space-y-1 ml-2">
                  <li>🛡️ Input Safety Check</li>
                  <li>🔄 ReAct Loop (1-3 cycles)</li>
                  <li>🎨 Synthesize Insights</li>
                  <li>✅ Output Validation</li>
                </ol>
              </div>
              <div className="bg-white p-3 rounded border border-gray-200">
                <p className="font-semibold mb-2">Tech Stack:</p>
                <ul className="list-disc list-inside text-xs space-y-1 ml-2">
                  <li>NVIDIA Nemotron Models</li>
                  <li>LangGraph Orchestration</li>
                  <li>ChromaDB Vector Store</li>
                  <li>Agentic RAG Pattern</li>
                </ul>
              </div>
            </div>
          )}
        </div>
      </div>
    </aside>
  );
};