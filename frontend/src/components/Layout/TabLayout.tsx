import React, { useState } from 'react';

interface Tab {
  id: string;
  label: string;
  icon: string;
}

interface TabLayoutProps {
  children: React.ReactNode[];
}

export const TabLayout: React.FC<TabLayoutProps> = ({ children }) => {
  const [activeTab, setActiveTab] = useState(0);
  
  const tabs: Tab[] = [
    { id: 'chat', label: 'Chat Interface', icon: '💬' },
    { id: 'data', label: 'Data Insights', icon: '📊' },
    { id: 'system', label: 'System Info', icon: '🔧' }
  ];

  return (
    <div className="h-full flex flex-col">
      {/* Tab headers */}
      <div className="bg-white border-b-2 border-gray-200">
        <div className="flex">
          {tabs.map((tab, index) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(index)}
              className={`
                px-6 py-3 font-medium transition-all relative
                ${activeTab === index
                  ? 'text-nvidia-green bg-gray-50'
                  : 'text-gray-600 hover:text-gray-800 hover:bg-gray-50'
                }
              `}
            >
              <div className="flex items-center gap-2">
                <span className="text-lg">{tab.icon}</span>
                <span>{tab.label}</span>
              </div>
              {activeTab === index && (
                <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-nvidia-green"></div>
              )}
            </button>
          ))}
        </div>
      </div>

      {/* Tab content */}
      <div className="flex-1 bg-white overflow-auto">
        {children[activeTab]}
      </div>
    </div>
  );
};
