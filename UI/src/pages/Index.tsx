import Navigation from '@/components/Navigation';
import HeroSection from '@/components/HeroSection';
import DashboardSection from '@/components/DashboardSection';
import InsightsSection from '@/components/InsightsSection';
import ChatSection from '@/components/ChatSection';
import ReportsSection from '@/components/ReportsSection';

const Index = () => {
  return (
    <div className="min-h-screen bg-background">
      <Navigation />
      <HeroSection />
      <DashboardSection />
      <InsightsSection />
      <ChatSection />
      <ReportsSection />
    </div>
  );
};

export default Index;
