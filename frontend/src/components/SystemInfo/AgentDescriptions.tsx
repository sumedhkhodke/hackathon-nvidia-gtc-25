import React, { useEffect, useState } from 'react';
import type { AgentInfo } from '../../types/index';
import { systemApi } from '../../services/api';

export const AgentDescriptions: React.FC = () => {
  const [agents, setAgents] = useState<AgentInfo[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadAgents();
  }, []);

  const loadAgents = async () => {
    try {
      const data = await systemApi.getAgents();
      setAgents(data);
    } catch (error) {
      console.error('Error loading agents:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="spinner"></div>
      </div>
    );
  }

  const coreReasoningAgents = agents.filter(a => 
    ['Reasoning Agent', 'ReAct Agent', 'Query Analyzer'].includes(a.name)
  );
  const backgroundAgents = agents.filter(a => 
    ['Analysis Agent', 'Coach Agent'].includes(a.name)
  );
  const safetyAgents = agents.filter(a => 
    ['Safety Guard'].includes(a.name)
  );

  return (
    <div className="max-w-6xl mx-auto p-6">
      <h2 className="text-2xl font-bold mb-6">🤖 Agent Descriptions</h2>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Core Reasoning Agents */}
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold mb-4">Core Reasoning Agents</h3>
          <div className="space-y-4">
            {coreReasoningAgents.map((agent) => (
              <div key={agent.name} className="border-l-4 border-nvidia-green pl-4">
                <div className="flex items-start gap-2">
                  <span className="text-2xl">{agent.icon}</span>
                  <div className="flex-1">
                    <h4 className="font-semibold text-nvidia-green">{agent.name}</h4>
                    <p className="text-sm text-gray-600 mb-1">Model: {agent.model}</p>
                    <p className="text-sm text-gray-700">{agent.description}</p>
                    <span className={`inline-block mt-1 text-xs px-2 py-1 rounded ${
                      agent.status === 'active' 
                        ? 'bg-green-100 text-green-800' 
                        : 'bg-gray-100 text-gray-600'
                    }`}>
                      {agent.status}
                    </span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Background Analysis */}
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold mb-4">Background Analysis</h3>
          <div className="space-y-4">
            {backgroundAgents.map((agent) => (
              <div key={agent.name} className="border-l-4 border-orange-500 pl-4">
                <div className="flex items-start gap-2">
                  <span className="text-2xl">{agent.icon}</span>
                  <div className="flex-1">
                    <h4 className="font-semibold text-orange-600">{agent.name}</h4>
                    <p className="text-sm text-gray-600 mb-1">Model: {agent.model}</p>
                    <p className="text-sm text-gray-700">{agent.description}</p>
                    <span className={`inline-block mt-1 text-xs px-2 py-1 rounded ${
                      agent.status === 'active' 
                        ? 'bg-green-100 text-green-800' 
                        : 'bg-gray-100 text-gray-600'
                    }`}>
                      {agent.status}
                    </span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Safety & Support */}
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold mb-4">Safety & Support</h3>
          <div className="space-y-4">
            {safetyAgents.map((agent) => (
              <div key={agent.name} className="border-l-4 border-blue-500 pl-4">
                <div className="flex items-start gap-2">
                  <span className="text-2xl">{agent.icon}</span>
                  <div className="flex-1">
                    <h4 className="font-semibold text-blue-600">{agent.name}</h4>
                    <p className="text-sm text-gray-600 mb-1">Model: {agent.model}</p>
                    <p className="text-sm text-gray-700">{agent.description}</p>
                    <span className={`inline-block mt-1 text-xs px-2 py-1 rounded ${
                      agent.status === 'active' 
                        ? 'bg-green-100 text-green-800' 
                        : 'bg-gray-100 text-gray-600'
                    }`}>
                      {agent.status}
                    </span>
                  </div>
                </div>
              </div>
            ))}

            {/* Additional components */}
            <div className="border-l-4 border-purple-500 pl-4">
              <div className="flex items-start gap-2">
                <span className="text-2xl">💡</span>
                <div className="flex-1">
                  <h4 className="font-semibold text-purple-600">Insights Tool</h4>
                  <p className="text-sm text-gray-700">
                    Bridges background & real-time, fetches pre-computed KPIs, 
                    enriches ReAct context, enables data-driven responses
                  </p>
                </div>
              </div>
            </div>

            <div className="border-l-4 border-gray-500 pl-4">
              <div className="flex items-start gap-2">
                <span className="text-2xl">📊</span>
                <div className="flex-1">
                  <h4 className="font-semibold text-gray-700">Data Stores</h4>
                  <ul className="text-sm text-gray-600 list-disc list-inside">
                    <li>ChromaDB: Vector embeddings</li>
                    <li>KPI Store: Computed metrics</li>
                    <li>Insights Cache: Coach outputs</li>
                    <li>SQLite: Metadata</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
