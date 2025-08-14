import { Card } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { TrendingUp, AlertTriangle, CheckCircle, Info, Target, Zap, Award } from 'lucide-react';

const InsightsSection = () => {
  const insights = [
    {
      type: 'success',
      icon: CheckCircle,
      title: 'Revenue Growth Acceleration',
      description: 'Monthly revenue increased by 15.3% compared to the previous quarter, primarily driven by mobile user conversion optimization.',
      impact: 'High',
      confidence: 95,
      recommendations: [
        'Continue mobile-first optimization strategy',
        'Expand marketing budget for mobile channels',
        'Implement similar optimization for tablet users'
      ],
      metrics: {
        revenue_impact: '+$12,500',
        time_period: 'Last 30 days'
      }
    },
    {
      type: 'warning',
      icon: AlertTriangle,
      title: 'Desktop Conversion Decline',
      description: 'Desktop traffic shows a concerning 8.7% decrease in conversion rates, suggesting potential UX issues or increased competition.',
      impact: 'Medium',
      confidence: 87,
      recommendations: [
        'Conduct desktop UX audit',
        'A/B test checkout process improvements',
        'Analyze competitor desktop experiences'
      ],
      metrics: {
        revenue_impact: '-$3,200',
        time_period: 'Last 14 days'
      }
    },
    {
      type: 'info',
      icon: Target,
      title: 'Seasonal Pattern Recognition',
      description: 'AI analysis reveals a consistent 23% uptick in user engagement during weekday evening hours (6-9 PM), indicating optimal campaign timing.',
      impact: 'Medium',
      confidence: 92,
      recommendations: [
        'Schedule major campaigns for 6-9 PM slots',
        'Increase server capacity during peak hours',
        'Create evening-specific content strategies'
      ],
      metrics: {
        engagement_lift: '+23%',
        time_period: 'Last 60 days'
      }
    },
    {
      type: 'opportunity',
      icon: Zap,
      title: 'Untapped Market Segment',
      description: 'Data shows significant potential in the 35-44 age demographic with 67% higher lifetime value but currently represents only 12% of our user base.',
      impact: 'High',
      confidence: 89,
      recommendations: [
        'Develop targeted campaigns for 35-44 demographic',
        'Research preferred channels for this age group',
        'Create age-appropriate content and messaging'
      ],
      metrics: {
        potential_revenue: '+$28,000',
        market_share: '12% current, 35% potential'
      }
    }
  ];

  const getInsightColor = (type: string) => {
    switch (type) {
      case 'success': return 'text-analytics-success border-analytics-success/20 bg-analytics-success/5';
      case 'warning': return 'text-destructive border-destructive/20 bg-destructive/5';
      case 'info': return 'text-primary border-primary/20 bg-primary/5';
      case 'opportunity': return 'text-secondary border-secondary/20 bg-secondary/5';
      default: return 'text-muted-foreground border-border bg-muted/5';
    }
  };

  const getImpactBadge = (impact: string) => {
    const colors = {
      'High': 'bg-analytics-success text-analytics-success-foreground',
      'Medium': 'bg-analytics-warning text-background',
      'Low': 'bg-muted text-muted-foreground'
    };
    return colors[impact as keyof typeof colors] || colors.Low;
  };

  return (
    <section id="insights" className="py-20 bg-gradient-to-b from-muted/20 to-background">
      <div className="container mx-auto px-6">
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold mb-6">
            AI-Powered Insights
          </h2>
          <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
            Automated analysis and actionable recommendations based on your data patterns and industry benchmarks
          </p>
        </div>

        {/* Summary Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
          <Card className="analytics-card text-center animate-slide-up">
            <div className="w-16 h-16 bg-analytics-success/10 rounded-full flex items-center justify-center mx-auto mb-4">
              <Award className="h-8 w-8 text-analytics-success" />
            </div>
            <h3 className="text-2xl font-bold mb-2">87%</h3>
            <p className="text-muted-foreground">Average Insight Accuracy</p>
          </Card>
          
          <Card className="analytics-card text-center animate-slide-up" style={{ animationDelay: '0.1s' }}>
            <div className="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-4">
              <TrendingUp className="h-8 w-8 text-primary" />
            </div>
            <h3 className="text-2xl font-bold mb-2">24</h3>
            <p className="text-muted-foreground">Active Recommendations</p>
          </Card>
          
          <Card className="analytics-card text-center animate-slide-up" style={{ animationDelay: '0.2s' }}>
            <div className="w-16 h-16 bg-secondary/10 rounded-full flex items-center justify-center mx-auto mb-4">
              <Info className="h-8 w-8 text-secondary" />
            </div>
            <h3 className="text-2xl font-bold mb-2">$47K</h3>
            <p className="text-muted-foreground">Potential Monthly Impact</p>
          </Card>
        </div>

        {/* Insights List */}
        <div className="space-y-8">
          {insights.map((insight, index) => {
            const Icon = insight.icon;
            return (
              <Card 
                key={insight.title} 
                className={`analytics-card ${getInsightColor(insight.type)} animate-slide-up`}
                style={{ animationDelay: `${index * 0.1}s` }}
              >
                <div className="flex flex-col lg:flex-row lg:items-start gap-6">
                  {/* Icon and Header */}
                  <div className="flex items-start gap-4 lg:min-w-0 lg:flex-1">
                    <div className={`w-12 h-12 rounded-full flex items-center justify-center flex-shrink-0 ${
                      insight.type === 'success' ? 'bg-analytics-success/10' :
                      insight.type === 'warning' ? 'bg-destructive/10' :
                      insight.type === 'info' ? 'bg-primary/10' :
                      'bg-secondary/10'
                    }`}>
                      <Icon className="h-6 w-6" />
                    </div>
                    
                    <div className="flex-1 min-w-0">
                      <div className="flex flex-col sm:flex-row sm:items-center gap-3 mb-3">
                        <h3 className="text-xl font-semibold">{insight.title}</h3>
                        <div className="flex gap-2">
                          <Badge className={getImpactBadge(insight.impact)}>
                            {insight.impact} Impact
                          </Badge>
                          <Badge variant="outline" className="border-current">
                            {insight.confidence}% Confidence
                          </Badge>
                        </div>
                      </div>
                      
                      <p className="text-muted-foreground mb-4 leading-relaxed">
                        {insight.description}
                      </p>
                      
                      {/* Metrics */}
                      <div className="grid grid-cols-2 gap-4 mb-4 p-4 bg-background/50 rounded-lg">
                        {Object.entries(insight.metrics).map(([key, value]) => (
                          <div key={key}>
                            <p className="text-sm text-muted-foreground capitalize">
                              {key.replace('_', ' ')}
                            </p>
                            <p className="font-semibold">{value}</p>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                  
                  {/* Recommendations */}
                  <div className="lg:min-w-80">
                    <h4 className="font-semibold mb-3">Recommended Actions</h4>
                    <ul className="space-y-2">
                      {insight.recommendations.map((recommendation, idx) => (
                        <li key={idx} className="flex items-start gap-2 text-sm">
                          <CheckCircle className="h-4 w-4 text-analytics-success mt-0.5 flex-shrink-0" />
                          <span className="leading-relaxed">{recommendation}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
              </Card>
            );
          })}
        </div>

        {/* Action Center */}
        <Card className="analytics-card mt-12 text-center animate-slide-up">
          <div className="max-w-2xl mx-auto">
            <h3 className="text-2xl font-bold mb-4">Need More Detailed Analysis?</h3>
            <p className="text-muted-foreground mb-6">
              Our AI can provide deeper insights and custom recommendations based on your specific business goals and industry benchmarks.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <button className="px-6 py-3 bg-primary text-primary-foreground rounded-lg smooth-hover hover:bg-primary/90">
                Generate Custom Report
              </button>
              <button className="px-6 py-3 border border-secondary text-secondary rounded-lg smooth-hover hover:bg-secondary hover:text-secondary-foreground">
                Schedule Analysis
              </button>
            </div>
          </div>
        </Card>
      </div>
    </section>
  );
};

export default InsightsSection;