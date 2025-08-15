import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { BarChart, LineChart, PieChart } from 'lucide-react';

interface ChartData {
  id: string;
  title: string;
  type: 'histogram' | 'bar' | 'scatter' | 'line' | 'pie';
  htmlContent?: string;
  url?: string;
  description?: string;
}

interface ChartDisplayProps {
  charts: ChartData[];
}

export const ChartDisplay: React.FC<ChartDisplayProps> = ({ charts }) => {
  const getChartIcon = (type: string) => {
    switch (type) {
      case 'bar':
      case 'histogram':
        return BarChart;
      case 'line':
      case 'scatter':
        return LineChart;
      case 'pie':
        return PieChart;
      default:
        return BarChart;
    }
  };

  const getChartColor = (type: string) => {
    switch (type) {
      case 'bar':
      case 'histogram':
        return 'text-primary';
      case 'line':
      case 'scatter':
        return 'text-secondary';
      case 'pie':
        return 'text-accent';
      default:
        return 'text-primary';
    }
  };

  return (
    <div className="space-y-6">
      <div className="text-center">
        <h2 className="text-2xl font-bold mb-2">Interactive Charts</h2>
        <p className="text-muted-foreground">Visual insights from your data</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {charts.map((chart) => {
          const IconComponent = getChartIcon(chart.type);
          const iconColor = getChartColor(chart.type);
          
          return (
            <Card key={chart.id} className="card-elevated card-interactive">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <IconComponent className={`w-5 h-5 ${iconColor}`} />
                  {chart.title}
                </CardTitle>
                {chart.description && (
                  <p className="text-sm text-muted-foreground">{chart.description}</p>
                )}
              </CardHeader>
              <CardContent>
                <div className="relative w-full h-80 bg-surface rounded-lg overflow-hidden">
                  <iframe
                    src={chart.url || ''}
                    srcDoc={chart.htmlContent}
                    className="w-full h-full border-0"
                    title={chart.title}
                    sandbox="allow-scripts"
                  />
                </div>
              </CardContent>
            </Card>
          );
        })}
      </div>

      {charts.length === 0 && (
        <Card className="card-elevated">
          <CardContent className="text-center py-12">
            <BarChart className="w-16 h-16 mx-auto mb-4 text-muted-foreground" />
            <h3 className="text-lg font-semibold mb-2">No Charts Available</h3>
            <p className="text-muted-foreground">
              Charts will be generated based on your data analysis
            </p>
          </CardContent>
        </Card>
      )}
    </div>
  );
};