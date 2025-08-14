import { Button } from '@/components/ui/button';
import { ArrowRight, TrendingUp, BarChart3, PieChart } from 'lucide-react';

const HeroSection = () => {
  return (
    <section className="min-h-screen flex items-center justify-center relative overflow-hidden bg-gradient-to-br from-background to-background/80">
      {/* Background decorative elements */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute top-1/4 left-1/4 w-64 h-64 bg-primary/5 rounded-full blur-3xl animate-pulse-glow"></div>
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-secondary/5 rounded-full blur-3xl animate-pulse-glow" style={{ animationDelay: '1s' }}></div>
      </div>

      <div className="container mx-auto px-6 py-20 relative z-10">
        <div className="text-center max-w-4xl mx-auto">
          {/* Main heading */}
          <h1 className="text-5xl md:text-7xl font-bold mb-8 animate-fade-in">
            <span className="block">Transform Data Into</span>
            <span className="bg-gradient-primary bg-clip-text text-transparent">
              Actionable Insights
            </span>
          </h1>
          
          {/* Subheading */}
          <p className="text-xl md:text-2xl text-muted-foreground mb-12 max-w-3xl mx-auto animate-slide-up">
            Professional analytics platform designed for data analysts. 
            Interactive visualizations, AI-powered insights, and comprehensive reporting 
            in one seamless interface.
          </p>

          {/* CTA Buttons */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-16 animate-slide-up" style={{ animationDelay: '0.2s' }}>
            <Button size="lg" className="bg-primary hover:bg-primary/90 text-primary-foreground px-8 py-4 text-lg smooth-hover glow-primary">
              Explore Dashboard
              <ArrowRight className="ml-2 h-5 w-5" />
            </Button>
            <Button variant="outline" size="lg" className="border-secondary text-secondary hover:bg-secondary hover:text-secondary-foreground px-8 py-4 text-lg smooth-hover">
              View Demo
            </Button>
          </div>

          {/* Feature highlights */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-3xl mx-auto animate-slide-up" style={{ animationDelay: '0.4s' }}>
            <div className="flex flex-col items-center space-y-3">
              <div className="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center">
                <BarChart3 className="h-8 w-8 text-primary" />
              </div>
              <h3 className="text-lg font-semibold">Interactive Charts</h3>
              <p className="text-muted-foreground text-center">Real-time data visualization with multiple chart types</p>
            </div>
            
            <div className="flex flex-col items-center space-y-3">
              <div className="w-16 h-16 bg-secondary/10 rounded-full flex items-center justify-center">
                <TrendingUp className="h-8 w-8 text-secondary" />
              </div>
              <h3 className="text-lg font-semibold">AI Insights</h3>
              <p className="text-muted-foreground text-center">Automated analysis and pattern recognition</p>
            </div>
            
            <div className="flex flex-col items-center space-y-3">
              <div className="w-16 h-16 bg-chart-3/10 rounded-full flex items-center justify-center">
                <PieChart className="h-8 w-8 text-chart-3" />
              </div>
              <h3 className="text-lg font-semibold">Professional Reports</h3>
              <p className="text-muted-foreground text-center">Export-ready analytics reports and documentation</p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default HeroSection;