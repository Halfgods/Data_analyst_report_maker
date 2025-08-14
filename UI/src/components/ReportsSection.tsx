import { useState } from 'react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Download, FileText, Calendar, BarChart3, TrendingUp, Users, DollarSign, Eye, AlertCircle } from 'lucide-react';

interface ReportsSectionProps {
  currentSessionId?: string | null;
  processedData?: any;
}

const ReportsSection = ({ currentSessionId, processedData }: ReportsSectionProps) => {
  const [isGeneratingPdf, setIsGeneratingPdf] = useState(false);
  const [pdfInfo, setPdfInfo] = useState<any>(null);
  const [error, setError] = useState('');

  const API_BASE_URL = ''; // Matches index.html exactly

  // PDF report generation function
  const generatePdfReport = async () => {
    if (!currentSessionId) {
      setError('No active session. Please upload a CSV file first.');
      return;
    }

    setIsGeneratingPdf(true);
    setError('');

    try {
      // Call PDF generation endpoint
      const response = await fetch(`${API_BASE_URL}/generate-report/${currentSessionId}`, {
        method: 'POST'
      });
      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || 'PDF generation failed.');
      }

      setPdfInfo(data.pdf_info);
      
      // Auto-download the PDF
      if (data.pdf_info?.download_url) {
        const downloadLink = document.createElement('a');
        downloadLink.href = `${API_BASE_URL}${data.pdf_info.download_url}`;
        downloadLink.download = data.pdf_info.filename;
        document.body.appendChild(downloadLink);
        downloadLink.click();
        document.body.removeChild(downloadLink);
      }

    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Unknown error occurred';
      setError(errorMessage);
      console.error('PDF Generation Error:', error);
    } finally {
      setIsGeneratingPdf(false);
    }
  };
  const reportData = {
    title: "Q3 2024 Analytics Report",
    generatedDate: "December 8, 2024",
    period: "July 1 - September 30, 2024",
    pages: 24,
    size: "2.4 MB"
  };

  const reportSections = [
    { title: "Executive Summary", page: 1, icon: BarChart3 },
    { title: "Revenue Analysis", page: 3, icon: DollarSign },
    { title: "User Behavior Insights", page: 8, icon: Users },
    { title: "Growth Trends", page: 15, icon: TrendingUp },
    { title: "Recommendations", page: 20, icon: FileText }
  ];

  const keyHighlights = [
    {
      metric: "Total Revenue",
      value: "$142,350",
      change: "+18.5%",
      description: "Compared to previous quarter"
    },
    {
      metric: "Active Users",
      value: "12,847",
      change: "+23.2%",
      description: "Monthly active users growth"
    },
    {
      metric: "Conversion Rate",
      value: "4.8%",
      change: "+1.2%",
      description: "Overall conversion improvement"
    },
    {
      metric: "Customer LTV",
      value: "$1,248",
      change: "+9.7%",
      description: "Average customer lifetime value"
    }
  ];

  return (
    <section id="reports" className="py-20 bg-gradient-to-b from-muted/20 to-background">
      <div className="container mx-auto px-6">
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold mb-6">
            Professional Reports
          </h2>
          <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
            Comprehensive analytics reports ready for executive presentation and strategic decision-making
          </p>
        </div>

        <div className="max-w-6xl mx-auto">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {/* PDF Preview */}
            <Card className="analytics-card">
              <div className="mb-6">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-xl font-semibold">Report Preview</h3>
                  <Badge variant="outline" className="border-primary text-primary">
                    Latest
                  </Badge>
                </div>
                
                <div className="space-y-2 text-sm text-muted-foreground">
                  <div className="flex justify-between">
                    <span>Report Period:</span>
                    <span>{reportData.period}</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Generated:</span>
                    <span>{reportData.generatedDate}</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Pages:</span>
                    <span>{reportData.pages}</span>
                  </div>
                  <div className="flex justify-between">
                    <span>File Size:</span>
                    <span>{reportData.size}</span>
                  </div>
                </div>
              </div>

              {/* PDF Preview Mockup */}
              <div className="bg-muted/50 rounded-lg p-6 mb-6 min-h-[400px] border border-border relative overflow-hidden">
                <div className="absolute inset-0 bg-gradient-to-br from-background to-muted/30"></div>
                <div className="relative z-10">
                  {/* Header */}
                  <div className="text-center mb-8">
                    <div className="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-4">
                      <BarChart3 className="h-8 w-8 text-primary" />
                    </div>
                    <h4 className="text-2xl font-bold mb-2">{reportData.title}</h4>
                    <p className="text-muted-foreground">Comprehensive Analytics Overview</p>
                  </div>

                  {/* Sample Content */}
                  <div className="space-y-4">
                    <div className="h-3 bg-foreground/20 rounded w-3/4"></div>
                    <div className="h-3 bg-foreground/15 rounded w-full"></div>
                    <div className="h-3 bg-foreground/15 rounded w-5/6"></div>
                    
                    <div className="my-6 p-4 bg-primary/5 rounded border border-primary/20">
                      <div className="h-2 bg-primary/30 rounded w-1/2 mb-2"></div>
                      <div className="h-2 bg-primary/20 rounded w-3/4"></div>
                    </div>
                    
                    <div className="grid grid-cols-2 gap-4">
                      <div className="h-20 bg-secondary/10 rounded border border-secondary/20"></div>
                      <div className="h-20 bg-chart-3/10 rounded border border-chart-3/20"></div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Action Buttons */}
              <div className="flex flex-col sm:flex-row gap-3">
                <Button className="flex-1 bg-primary hover:bg-primary/90 text-primary-foreground smooth-hover">
                  <Download className="h-4 w-4 mr-2" />
                  Download PDF
                </Button>
                <Button variant="outline" className="flex-1 border-secondary text-secondary hover:bg-secondary hover:text-secondary-foreground smooth-hover">
                  <Eye className="h-4 w-4 mr-2" />
                  Full Preview
                </Button>
              </div>
            </Card>

            {/* Report Content & Highlights */}
            <div className="space-y-6">
              {/* Key Highlights */}
              <Card className="analytics-card">
                <h3 className="text-xl font-semibold mb-6">Key Highlights</h3>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  {keyHighlights.map((highlight, index) => (
                    <div 
                      key={highlight.metric} 
                      className="p-4 bg-gradient-to-br from-background to-muted/30 rounded-lg border border-border smooth-hover hover:border-primary/20 animate-slide-up"
                      style={{ animationDelay: `${index * 0.1}s` }}
                    >
                      <p className="text-sm text-muted-foreground mb-1">{highlight.metric}</p>
                      <p className="text-2xl font-bold mb-1">{highlight.value}</p>
                      <div className="flex items-center gap-2">
                        <span className="text-sm text-analytics-success">{highlight.change}</span>
                        <span className="text-xs text-muted-foreground">{highlight.description}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </Card>

              {/* Table of Contents */}
              <Card className="analytics-card">
                <h3 className="text-xl font-semibold mb-6">Report Sections</h3>
                <div className="space-y-3">
                  {reportSections.map((section, index) => {
                    const Icon = section.icon;
                    return (
                      <div 
                        key={section.title}
                        className="flex items-center justify-between p-3 rounded-lg bg-gradient-to-r from-background to-muted/20 border border-border smooth-hover hover:border-primary/20 animate-slide-up"
                        style={{ animationDelay: `${index * 0.05}s` }}
                      >
                        <div className="flex items-center gap-3">
                          <div className="w-8 h-8 bg-primary/10 rounded-full flex items-center justify-center">
                            <Icon className="h-4 w-4 text-primary" />
                          </div>
                          <span className="font-medium">{section.title}</span>
                        </div>
                        <span className="text-sm text-muted-foreground">Page {section.page}</span>
                      </div>
                    );
                  })}
                </div>
              </Card>

              {/* Report Options */}
              <Card className="analytics-card">
                <h3 className="text-xl font-semibold mb-6">Report Options</h3>
                <div className="space-y-4">
                  <div className="flex items-center justify-between p-3 bg-gradient-to-r from-background to-muted/20 rounded-lg border border-border">
                    <div className="flex items-center gap-3">
                      <Calendar className="h-5 w-5 text-primary" />
                      <span>Custom Date Range</span>
                    </div>
                    <Button variant="outline" size="sm" className="border-primary text-primary hover:bg-primary hover:text-primary-foreground">
                      Configure
                    </Button>
                  </div>
                  
                  <div className="flex items-center justify-between p-3 bg-gradient-to-r from-background to-muted/20 rounded-lg border border-border">
                    <div className="flex items-center gap-3">
                      <FileText className="h-5 w-5 text-secondary" />
                      <span>Executive Summary Only</span>
                    </div>
                    <Button variant="outline" size="sm" className="border-secondary text-secondary hover:bg-secondary hover:text-secondary-foreground">
                      Generate
                    </Button>
                  </div>
                  
                  <div className="flex items-center justify-between p-3 bg-gradient-to-r from-background to-muted/20 rounded-lg border border-border">
                    <div className="flex items-center gap-3">
                      <TrendingUp className="h-5 w-5 text-chart-3" />
                      <span>Scheduled Reports</span>
                    </div>
                    <Button variant="outline" size="sm" className="border-chart-3 text-chart-3 hover:bg-chart-3 hover:text-background">
                      Setup
                    </Button>
                  </div>
                </div>
              </Card>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default ReportsSection;