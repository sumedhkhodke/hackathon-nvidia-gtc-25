import React from 'react';

export const TechStack: React.FC = () => {
  return (
    <div className="max-w-6xl mx-auto p-6 space-y-8">
      {/* Key Features */}
      <section>
        <h2 className="text-2xl font-bold mb-4">✨ Key Features Demonstrated</h2>
        <div className="bg-white rounded-lg shadow p-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {[
              { icon: '✅', text: 'Agentic Behavior - Autonomous reasoning and decision-making' },
              { icon: '✅', text: 'ReAct Pattern - Reason → Act → Observe cycles for complex problem-solving' },
              { icon: '✅', text: 'Multi-Agent Orchestration - Specialized agents working in coordination via LangGraph' },
              { icon: '✅', text: 'Background Processing - Async Analysis & Coach agents for KPI-driven insights' },
              { icon: '✅', text: 'Safety Guardrails - Dual safety checks on input and output' },
              { icon: '✅', text: 'Agentic RAG - Intelligent retrieval-augmented generation' },
              { icon: '✅', text: 'Tool Integration - Vector DB querying and data analysis' },
              { icon: '✅', text: 'State Management - LangGraph for stateful workflows' },
              { icon: '✅', text: 'Privacy-by-Design - Local-first data architecture' },
              { icon: '✅', text: 'NVIDIA Embeddings - NeMo Retriever embeddings for better retrieval' },
            ].map((feature, index) => (
              <div key={index} className="flex items-start gap-2">
                <span className="text-lg">{feature.icon}</span>
                <span className="text-gray-700">{feature.text}</span>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Technology Stack */}
      <section>
        <h2 className="text-2xl font-bold mb-4">🛠️ Technology Stack</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="font-semibold text-lg mb-3 text-nvidia-green">AI Models:</h3>
            <ul className="space-y-2 text-gray-700">
              <li className="flex items-center gap-2">
                <span className="text-green-500">✅</span>
                Nemotron Super 49B v1.5
              </li>
              <li className="flex items-center gap-2">
                <span className="text-green-500">✅</span>
                Nemotron Safety 8B v3 (NEW)
              </li>
              <li className="flex items-center gap-2">
                <span className="text-green-500">✅</span>
                Nemotron Nano 9B v2
              </li>
              <li className="flex items-center gap-2">
                <span className="text-green-500">✅</span>
                NVIDIA NIM APIs
              </li>
              <li className="flex items-center gap-2">
                <span className="text-green-500">✅</span>
                NeMo Retriever Embeddings
              </li>
            </ul>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="font-semibold text-lg mb-3 text-nvidia-green">Orchestration:</h3>
            <ul className="space-y-2 text-gray-700">
              <li>• LangGraph</li>
              <li>• Python OpenAI Client</li>
              <li>• FastAPI + WebSockets</li>
              <li>• React + TypeScript</li>
              <li>• Zustand State Management</li>
            </ul>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="font-semibold text-lg mb-3 text-nvidia-green">Data & Storage:</h3>
            <ul className="space-y-2 text-gray-700">
              <li>• ChromaDB with NVIDIA Embeddings</li>
              <li>• Pandas</li>
              <li>• Vector Embeddings (1024d)</li>
              <li>• Asymmetric Embeddings</li>
              <li>• Local-first Architecture</li>
            </ul>
          </div>
        </div>
      </section>

      {/* Alignment with Judging Criteria */}
      <section>
        <h2 className="text-2xl font-bold mb-4">🏆 Alignment with Judging Criteria</h2>
        <div className="bg-white rounded-lg shadow overflow-hidden">
          <table className="w-full">
            <thead className="bg-nvidia-green text-white">
              <tr>
                <th className="px-6 py-3 text-left">Criteria</th>
                <th className="px-6 py-3 text-left">How We Address It</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {[
                {
                  criteria: 'Creativity',
                  solution: 'Novel application of multi-agent AI to personal lifelog analysis with ReAct pattern'
                },
                {
                  criteria: 'Functionality',
                  solution: 'Live demo with real data processing, multi-step reasoning, and safety guardrails'
                },
                {
                  criteria: 'Scope of Completion',
                  solution: 'Complete end-to-end workflow: data ingestion → RAG retrieval → multi-agent reasoning → safe output'
                },
                {
                  criteria: 'Presentation',
                  solution: 'Interactive UI showing agent reasoning process, safety checks, and system architecture'
                },
                {
                  criteria: 'Use of NVIDIA Tools',
                  solution: 'NVIDIA Nemotron models (Super 49B, Safety 8B v3) via NIM APIs + NeMo Retriever embeddings'
                },
                {
                  criteria: 'Use of Nemotron Models',
                  solution: 'Sophisticated multi-agent orchestration demonstrating agentic reasoning and safety capabilities'
                },
              ].map((item, index) => (
                <tr key={index} className="hover:bg-gray-50">
                  <td className="px-6 py-4 font-medium text-gray-900">{item.criteria}</td>
                  <td className="px-6 py-4 text-gray-700">{item.solution}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      {/* Footer */}
      <div className="text-center text-gray-600 text-sm mt-8 pb-4">
        <p className="font-bold">🏆 Built for NVIDIA GTC Hackathon 2025 - Nemotron Prize Track</p>
        <p className="mt-1">
          Demonstrating agentic AI with ReAct pattern, multi-agent orchestration, safety guardrails, and tool integration
        </p>
        <p className="mt-1 italic">
          Powered by NVIDIA Nemotron Super 49B v1.5 & Nemotron Safety Guard 8B v3
        </p>
      </div>
    </div>
  );
};
