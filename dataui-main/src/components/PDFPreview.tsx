import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Badge } from '@/components/ui/badge';
import { Eye, Download, FileText, Calendar, User, BarChart3, TrendingUp } from 'lucide-react';

interface PDFPreviewProps {
  fileName: string;
  isGenerating?: boolean;
  onDownload: () => void;
  pdfUrl?: string;
  pdfInfo?: any;
}

export const PDFPreview: React.FC<PDFPreviewProps> = ({ 
  fileName, 
  isGenerating = false, 
  onDownload,
  pdfUrl,
  pdfInfo
}) => {
  const [activeTab, setActiveTab] = useState('overview');

  const generateDate = new Date().toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });

  const handleViewPDF = () => {
    if (pdfUrl) {
      window.open(pdfUrl, '_blank');
    }
  };

  return (
    <Card className="card-elevated">
      <CardHeader className="border-b border-border">
        <div className="flex items-center justify-between">
          <CardTitle className="flex items-center gap-2">
            <FileText className="w-5 h-5 text-primary" />
            PDF Report Preview
          </CardTitle>
          <div className="flex items-center gap-2">
            <span className="status-indicator status-info">
              <Calendar className="w-3 h-3" />
              {generateDate}
            </span>
            {pdfUrl && (
              <Button 
                onClick={handleViewPDF}
                variant="outline"
                size="sm"
              >
                <Eye className="w-4 h-4 mr-2" />
                View PDF
              </Button>
            )}
            <Button 
              onClick={onDownload}
              disabled={isGenerating}
              size="sm"
              className="bg-gradient-accent hover:bg-accent-hover"
            >
              {isGenerating ? (
                <>
                  <div className="w-3 h-3 border-2 border-current border-t-transparent animate-spin rounded-full mr-2" />
                  Generating...
                </>
              ) : (
                <>
                  <Download className="w-4 h-4 mr-2" />
                  Download PDF
                </>
              )}
            </Button>
          </div>
        </div>
      </CardHeader>

      <CardContent className="p-0">
        <Tabs value={activeTab} onValueChange={setActiveTab}>
          <TabsList className="grid w-full grid-cols-3 rounded-none border-b">
            <TabsTrigger value="overview" className="flex items-center gap-2">
              <Eye className="w-4 h-4" />
              Overview
            </TabsTrigger>
            <TabsTrigger value="stats" className="flex items-center gap-2">
              <BarChart3 className="w-4 h-4" />
              Statistics
            </TabsTrigger>
            <TabsTrigger value="insights" className="flex items-center gap-2">
              <TrendingUp className="w-4 h-4" />
              Insights
            </TabsTrigger>
          </TabsList>

          <div className="p-6">
            <TabsContent value="overview" className="mt-0 space-y-4">
              <div className="bg-gradient-surface p-6 rounded-lg border border-border/50">
                <div className="text-center space-y-2 mb-6">
                  <h1 className="text-2xl font-bold gradient-text">Data Analysis Report</h1>
                  <p className="text-muted-foreground">Comprehensive analysis of {fileName}</p>
                  <div className="flex justify-center gap-4 text-sm text-muted-foreground">
                    <span className="flex items-center gap-1">
                      <User className="w-3 h-3" />
                      CSV Analyzer
                    </span>
                    <span className="flex items-center gap-1">
                      <Calendar className="w-3 h-3" />
                      {generateDate}
                    </span>
                  </div>
                </div>

                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <div className="text-center p-4 bg-card rounded-lg border border-border">
                    <div className="text-2xl font-bold text-primary">{pdfInfo?.statistics?.total_rows || '0'}</div>
                    <div className="text-sm text-muted-foreground">Total Rows</div>
                  </div>
                  <div className="text-center p-4 bg-card rounded-lg border border-border">
                    <div className="text-2xl font-bold text-secondary">{pdfInfo?.statistics?.total_columns || '0'}</div>
                    <div className="text-sm text-muted-foreground">Columns</div>
                  </div>
                  <div className="text-center p-4 bg-card rounded-lg border border-border">
                    <div className="text-2xl font-bold text-accent">{pdfInfo?.statistics?.data_types_count || '0'}</div>
                    <div className="text-sm text-muted-foreground">Data Types</div>
                  </div>
                  <div className="text-center p-4 bg-card rounded-lg border border-border">
                    <div className="text-2xl font-bold text-chart-4">{pdfInfo?.file_info?.size || 'Unknown'}</div>
                    <div className="text-sm text-muted-foreground">File Size</div>
                  </div>
                </div>
              </div>

              <div className="space-y-3">
                <h3 className="font-semibold">Report Contents</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                  <div className="flex items-center gap-3 p-3 bg-surface rounded-lg">
                    <div className="w-2 h-2 bg-primary rounded-full"></div>
                    <span className="text-sm">Executive Summary</span>
                  </div>
                  <div className="flex items-center gap-3 p-3 bg-surface rounded-lg">
                    <div className="w-2 h-2 bg-secondary rounded-full"></div>
                    <span className="text-sm">Data Quality Assessment</span>
                  </div>
                  <div className="flex items-center gap-3 p-3 bg-surface rounded-lg">
                    <div className="w-2 h-2 bg-accent rounded-full"></div>
                    <span className="text-sm">Statistical Analysis</span>
                  </div>
                  <div className="flex items-center gap-3 p-3 bg-surface rounded-lg">
                    <div className="w-2 h-2 bg-chart-4 rounded-full"></div>
                    <span className="text-sm">AI-Generated Insights</span>
                  </div>
                </div>
              </div>
            </TabsContent>

            <TabsContent value="stats" className="mt-0 space-y-4">
              <div className="space-y-4">
                <h3 className="font-semibold">Statistical Summary Preview</h3>
                
                <div className="bg-surface rounded-lg p-4 border border-border">
                  <h4 className="font-medium mb-3">Numeric Columns Analysis</h4>
                  <div className="space-y-2 text-sm">
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">Age (Mean):</span>
                      <Badge variant="secondary">42.5 years</Badge>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">Income (Median):</span>
                      <Badge variant="secondary">$52,000</Badge>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">Purchase Amount (Avg):</span>
                      <Badge variant="secondary">$125.50</Badge>
                    </div>
                  </div>
                </div>

                <div className="bg-surface rounded-lg p-4 border border-border">
                  <h4 className="font-medium mb-3">Data Quality Metrics</h4>
                  <div className="space-y-2 text-sm">
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">Completeness:</span>
                      <Badge className="bg-success-light text-success">98.5%</Badge>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">Unique Values:</span>
                      <Badge className="bg-primary-light text-primary">87.2%</Badge>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">Outliers Detected:</span>
                      <Badge className="bg-warning-light text-warning">2.3%</Badge>
                    </div>
                  </div>
                </div>
              </div>
            </TabsContent>

            <TabsContent value="insights" className="mt-0 space-y-4">
              <div className="space-y-4">
                <h3 className="font-semibold">Key Insights Preview</h3>
                
                <div className="space-y-3">
                  <div className="bg-gradient-surface p-4 rounded-lg border border-border/50">
                    <div className="flex items-start gap-3">
                      <div className="w-2 h-2 bg-primary rounded-full mt-2 flex-shrink-0"></div>
                      <div>
                        <h4 className="font-medium text-sm mb-1">Strong Income-Spending Correlation</h4>
                        <p className="text-xs text-muted-foreground">
                          Analysis reveals a 0.78 correlation between customer income and purchase amounts.
                        </p>
                      </div>
                    </div>
                  </div>

                  <div className="bg-gradient-surface p-4 rounded-lg border border-border/50">
                    <div className="flex items-start gap-3">
                      <div className="w-2 h-2 bg-secondary rounded-full mt-2 flex-shrink-0"></div>
                      <div>
                        <h4 className="font-medium text-sm mb-1">Target Demographics</h4>
                        <p className="text-xs text-muted-foreground">
                          Primary customer base centers around 42-45 years old, indicating middle-aged focus.
                        </p>
                      </div>
                    </div>
                  </div>

                  <div className="bg-gradient-surface p-4 rounded-lg border border-border/50">
                    <div className="flex items-start gap-3">
                      <div className="w-2 h-2 bg-accent rounded-full mt-2 flex-shrink-0"></div>
                      <div>
                        <h4 className="font-medium text-sm mb-1">Regional Performance</h4>
                        <p className="text-xs text-muted-foreground">
                          West region shows 23% higher spending, suggesting targeted marketing opportunities.
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </TabsContent>
          </div>
        </Tabs>
      </CardContent>
    </Card>
  );
};