import { useEffect, useState } from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Header } from './components/Layout/Header';
import { Sidebar } from './components/Layout/Sidebar';
import { TabLayout } from './components/Layout/TabLayout';
import { SimpleStreamingChat } from './components/Chat/SimpleStreamingChat';
import { SummaryCards } from './components/DataInsights/SummaryCards';
import { TimelineChart } from './components/DataInsights/TimelineChart';
import { CategoryChart } from './components/DataInsights/CategoryChart';
import { CorrelationHeatmap } from './components/DataInsights/CorrelationHeatmap';
import { RecentEntries } from './components/DataInsights/RecentEntries';
import { Architecture } from './components/SystemInfo/Architecture';
import { AgentDescriptions } from './components/SystemInfo/AgentDescriptions';
import { TechStack } from './components/SystemInfo/TechStack';
import { useChatStore } from './store/chatStore';
import { dataApi } from './services/api';
import type { 
  DataInsights, 
  CorrelationData, 
  TimelineDataPoint, 
  LifelogEntry 
} from './types/index';

// Create a client for React Query
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000, // 5 minutes
      gcTime: 10 * 60 * 1000, // 10 minutes
    },
  },
});

function App() {
  const { demoQuestion, setDemoQuestion, stats, loadStats, sidebarOpen } = useChatStore();
  const [dataInsights, setDataInsights] = useState<DataInsights | null>(null);
  const [correlationData, setCorrelationData] = useState<CorrelationData | null>(null);
  const [timelineData, setTimelineData] = useState<TimelineDataPoint[]>([]);
  const [recentEntries, setRecentEntries] = useState<LifelogEntry[]>([]);
  const [loading, setLoading] = useState(true);

  // Load initial data
  useEffect(() => {
    loadInitialData();
  }, []);

  const loadInitialData = async () => {
    try {
      await loadStats();
      
      // Load data insights
      const [insights, correlations, timeline, entries] = await Promise.all([
        dataApi.getInsights(),
        dataApi.getCorrelations(),
        dataApi.getTimeline(),
        dataApi.getEntries(15) // Get 15 most recent entries
      ]);
      
      setDataInsights(insights);
      setCorrelationData(correlations);
      setTimelineData(timeline.data);
      setRecentEntries(entries);
    } catch (error) {
      console.error('Error loading initial data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDemoQuestionClick = (question: string) => {
    setDemoQuestion(question);
  };
  
  const handleDemoQuestionHandled = () => {
    setDemoQuestion(null);
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="spinner mx-auto mb-4"></div>
          <p className="text-gray-600">Loading Agentic Lifelog...</p>
        </div>
      </div>
    );
  }

  return (
    <QueryClientProvider client={queryClient}>
      <div className="min-h-screen bg-white">
        <Header />
        
        <Sidebar 
          onDemoQuestionClick={handleDemoQuestionClick}
          stats={stats || { total_entries: 0 }}
        />
        
        <main className={`fixed top-16 bottom-0 right-0 bg-gray-50 transition-all duration-300 ${
          sidebarOpen ? 'left-72' : 'left-16'
        }`}>
          <TabLayout>
              {/* Chat Interface Tab */}
              <SimpleStreamingChat 
                demoQuestion={demoQuestion}
                onDemoQuestionHandled={handleDemoQuestionHandled}
              />
              
              {/* Data Insights Tab */}
              <div className="p-6 space-y-6 bg-white">
                <h2 className="text-2xl font-bold mb-6">📊 Your Lifelog Data Insights</h2>
              
              {dataInsights && (
                <>
                  <SummaryCards categories={dataInsights.category_summaries} />
                  
                  <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    <TimelineChart data={timelineData} />
                    <CategoryChart data={dataInsights.category_summaries} />
                  </div>
                </>
              )}
              
              {correlationData && (
                <CorrelationHeatmap data={correlationData} />
              )}
              
              <RecentEntries entries={recentEntries} />
            </div>
            
              {/* System Info Tab */}
              <div className="overflow-y-auto bg-white">
                <Architecture />
                <AgentDescriptions />
                <TechStack />
              </div>
            </TabLayout>
          </main>
      </div>
    </QueryClientProvider>
  );
}

export default App;