import { useState, useEffect } from 'react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { LineChart, Line, BarChart, Bar, PieChart, Pie, Cell, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { TrendingUp, TrendingDown, DollarSign, Users, Activity, BarChart3, Upload, AlertCircle, FileText, Download } from 'lucide-react';

interface ProcessedData {
  session_id: string;
  csv_metadata: {
    files: Array<{
      filename: string;
      rows: number;
      columns: string[];
      inferred_types: Record<string, string>;
      missing_values?: Record<string, number>;
      sample_data?: Record<string, any[]>;
    }>;
  };
  analysis_results: {
    descriptive_statistics?: Record<string, any>;
    correlation_matrix?: Record<string, any>;
    dynamic_charts?: {
      individual_columns: Array<{
        type: string;
        title: string;
        data: Array<{ name: string; value: number }>;
      }>;
    };
    data_quality?: {
      total_rows: number;
      total_columns: number;
      missing_values_total: number;
      duplicate_rows: number;
    };
  };
  ai_commentary: string;
}

const DashboardSection = () => {
  const [files, setFiles] = useState<FileList | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [processedData, setProcessedData] = useState<ProcessedData | null>(null);
  const [currentSessionId, setCurrentSessionId] = useState<string | null>(null);
  const [error, setError] = useState('');
  const [isGeneratingPdf, setIsGeneratingPdf] = useState(false);
  const [pdfInfo, setPdfInfo] = useState<any>(null);

  const API_BASE_URL = ''; // Matches index.html exactly

  // File upload logic from index.html
  const uploadFiles = async () => {
    if (!files || files.length === 0) {
      setError('Please select at least one CSV file.');
      return;
    }

    setIsProcessing(true);
    setError('');

    try {
      const formData = new FormData();
      for (let i = 0; i < files.length; i++) {
        formData.append('files', files[i]);
      }

      // Step 1: Upload CSVs (exact logic from index.html)
      const uploadResponse = await fetch(`${API_BASE_URL}/upload-csv/`, {
        method: 'POST',
        body: formData
      });
      const uploadData = await uploadResponse.json();

      if (!uploadResponse.ok) {
        throw new Error(uploadData.detail || 'File upload failed.');
      }

      const sessionId = uploadData.session_id;
      setCurrentSessionId(sessionId);

      // Step 2: Process data (exact logic from index.html)
      const processResponse = await fetch(`${API_BASE_URL}/process-data/${sessionId}`, {
        method: 'POST'
      });
      const processData = await processResponse.json();

      if (!processResponse.ok) {
        throw new Error(processData.detail || 'Data processing failed.');
      }

      setProcessedData(processData);
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Unknown error occurred';
      setError(errorMessage);
      console.error('Error:', error);
    } finally {
      setIsProcessing(false);
    }
  };

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

  // Generate dynamic data from backend response
  const generateDynamicData = () => {
    if (!processedData?.analysis_results || !processedData?.csv_metadata) {
      // Fallback data when no backend data available
      return {
        lineData: [
          { month: 'Jan', col1: 4000, col2: 2400 },
          { month: 'Feb', col1: 3000, col2: 1398 },
          { month: 'Mar', col1: 5000, col2: 9800 },
          { month: 'Apr', col1: 4500, col2: 3908 },
          { month: 'May', col1: 6000, col2: 4800 },
          { month: 'Jun', col1: 5500, col2: 3800 },
        ],
        lineDataKeys: ['col1', 'col2'],
        barData: [
          { category: 'Desktop', value: 45, color: 'hsl(var(--chart-1))' },
          { category: 'Mobile', value: 35, color: 'hsl(var(--chart-2))' },
          { category: 'Tablet', value: 20, color: 'hsl(var(--chart-3))' },
        ],
        pieData: [
          { name: 'Organic', value: 40, color: 'hsl(var(--chart-1))' },
          { name: 'Paid', value: 30, color: 'hsl(var(--chart-2))' },
          { name: 'Social', value: 20, color: 'hsl(var(--chart-3))' },
          { name: 'Email', value: 10, color: 'hsl(var(--chart-4))' },
        ],
        metrics: [
          { title: 'Total Rows', value: 'No Data', change: '', trend: 'up' as const, icon: DollarSign },
          { title: 'Columns', value: 'No Data', change: '', trend: 'up' as const, icon: Users },
          { title: 'Missing Values', value: 'No Data', change: '', trend: 'down' as const, icon: Activity },
          { title: 'Duplicates', value: 'No Data', change: '', trend: 'up' as const, icon: BarChart3 },
        ]
      };
    }

    const { analysis_results, csv_metadata } = processedData;
    const stats = analysis_results.descriptive_statistics || {};
    const dataQuality = analysis_results.data_quality || {};
    const dynamicCharts = analysis_results.dynamic_charts || {};
    const fileInfo = csv_metadata.files?.[0] || {};

    // Generate line data for first two numeric columns
    const numericColumns = Object.keys(stats).filter(col => 
      fileInfo.inferred_types?.[col] === 'integer' || fileInfo.inferred_types?.[col] === 'float'
    ).slice(0, 2);
    
    const lineData = [];
    const lineDataKeys = numericColumns.length >= 2 ? numericColumns : ['col1', 'col2'];
    
    if (numericColumns.length >= 2) {
      const col1Stats = stats[numericColumns[0]] || {};
      const col2Stats = stats[numericColumns[1]] || {};
      
      for (let i = 0; i < 6; i++) {
        lineData.push({
          month: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'][i],
          [numericColumns[0]]: Math.round((col1Stats.mean || 0) * (0.8 + Math.random() * 0.4)),
          [numericColumns[1]]: Math.round((col2Stats.mean || 0) * (0.8 + Math.random() * 0.4)),
        });
      }
    }

    // Generate bar data from first categorical chart
    let barData = [];
    if (dynamicCharts.individual_columns) {
      const barCharts = dynamicCharts.individual_columns.filter(chart => chart.type === 'bar');
      if (barCharts.length > 0 && barCharts[0].data) {
        barData = barCharts[0].data.slice(0, 3).map((item, index) => ({
          category: item.name || `Category ${index + 1}`,
          value: item.value || 0,
          color: `hsl(var(--chart-${index + 1}))`
        }));
      }
    }
    
    if (barData.length === 0) {
      barData = [
        { category: 'Category 1', value: 45, color: 'hsl(var(--chart-1))' },
        { category: 'Category 2', value: 35, color: 'hsl(var(--chart-2))' },
        { category: 'Category 3', value: 20, color: 'hsl(var(--chart-3))' },
      ];
    }

    // Generate pie data from first pie chart
    let pieData = [];
    if (dynamicCharts.individual_columns) {
      const pieCharts = dynamicCharts.individual_columns.filter(chart => chart.type === 'pie');
      if (pieCharts.length > 0 && pieCharts[0].data) {
        pieData = pieCharts[0].data.slice(0, 4).map((item, index) => ({
          name: item.name || `Item ${index + 1}`,
          value: item.value || 0,
          color: `hsl(var(--chart-${index + 1}))`
        }));
      }
    }
    
    if (pieData.length === 0) {
      pieData = [
        { name: 'Group 1', value: 40, color: 'hsl(var(--chart-1))' },
        { name: 'Group 2', value: 30, color: 'hsl(var(--chart-2))' },
        { name: 'Group 3', value: 20, color: 'hsl(var(--chart-3))' },
        { name: 'Group 4', value: 10, color: 'hsl(var(--chart-4))' },
      ];
    }

    // Generate real metrics from backend data
    const totalRows = fileInfo.rows || dataQuality.total_rows || 0;
    const totalColumns = fileInfo.columns?.length || dataQuality.total_columns || 0;
    const missingValues = dataQuality.missing_values_total || 0;
    const duplicateRows = dataQuality.duplicate_rows || 0;

    const metrics = [
      {
        title: 'Total Rows',
        value: totalRows.toLocaleString(),
        change: totalRows > 1000 ? '+High Volume' : '+Normal',
        trend: 'up' as const,
        icon: DollarSign,
      },
      {
        title: 'Columns',
        value: totalColumns.toString(),
        change: totalColumns > 10 ? '+Rich Data' : '+Standard',
        trend: 'up' as const,
        icon: Users,
      },
      {
        title: 'Missing Values',
        value: missingValues.toLocaleString(),
        change: missingValues > 0 ? 'Needs Attention' : 'Clean Data',
        trend: missingValues > 0 ? 'down' : 'up' as const,
        icon: Activity,
      },
      {
        title: 'Duplicates',
        value: duplicateRows.toLocaleString(),
        change: duplicateRows > 0 ? 'Found Issues' : 'Clean',
        trend: duplicateRows > 0 ? 'down' : 'up' as const,
        icon: BarChart3,
      },
    ];

    return { lineData, lineDataKeys, barData, pieData, metrics };
  };

  const { lineData, lineDataKeys, barData, pieData, metrics } = generateDynamicData();

  return (
    <section id="dashboard" className="py-20 bg-gradient-to-b from-background to-muted/20">
      <div className="container mx-auto px-6">
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold mb-6">
            Analytics Dashboard
          </h2>
          <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
            Interactive data visualizations with real-time updates and comprehensive insights
          </p>
        </div>

        {/* File Upload Section - matches index.html exactly */}
        {!processedData && (
          <Card className="max-w-2xl mx-auto mb-12 p-6">
            <div className="text-center mb-6">
              <h3 className="text-xl font-semibold mb-2">Upload CSVs for Analysis</h3>
              <p className="text-muted-foreground">Select one or multiple CSV files to start the analysis pipeline</p>
            </div>
            
            <div className="space-y-4">
              <div className="space-y-2">
                <Input
                  type="file"
                  multiple
                  accept=".csv"
                  onChange={(e) => setFiles(e.target.files)}
                  className="cursor-pointer"
                />
                {files && files.length > 0 && (
                  <p className="text-sm text-muted-foreground">
                    {files.length} file{files.length !== 1 ? 's' : ''} selected
                  </p>
                )}
              </div>
              
              <Button 
                onClick={uploadFiles}
                disabled={isProcessing || !files || files.length === 0}
                className="w-full"
                size="lg"
              >
                {isProcessing ? (
                  <>
                    <div className="animate-spin mr-2 h-4 w-4 border-2 border-white border-t-transparent rounded-full" />
                    Processing...
                  </>
                ) : (
                  <>
                    <Upload className="mr-2 h-4 w-4" />
                    Upload and Process
                  </>
                )}
              </Button>
              
              {error && (
                <div className="flex items-center gap-2 p-3 bg-destructive/10 border border-destructive/20 rounded-md">
                  <AlertCircle className="h-4 w-4 text-destructive" />
                  <p className="text-sm text-destructive">{error}</p>
                </div>
              )}
            </div>
          </Card>
        )}
        
        {processedData && (
          <div className="max-w-2xl mx-auto mb-8 text-center">
            <p className="text-lg text-muted-foreground">
              Session: <span className="font-mono text-sm">{currentSessionId}</span>
            </p>
            <p className="text-sm text-muted-foreground mt-2">
              Data processed successfully. Showing analysis for {processedData.csv_metadata.files?.[0]?.filename}
            </p>
          </div>
        )}

        {/* Key Metrics */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
          {metrics.map((metric, index) => {
            const Icon = metric.icon;
            return (
              <Card key={metric.title} className="analytics-card animate-slide-up" style={{ animationDelay: `${index * 0.1}s` }}>
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-muted-foreground">{metric.title}</p>
                    <p className="text-2xl font-bold">{metric.value}</p>
                    <div className={`flex items-center text-sm ${
                      metric.trend === 'up' ? 'text-analytics-success' : 'text-destructive'
                    }`}>
                      {metric.trend === 'up' ? (
                        <TrendingUp className="h-4 w-4 mr-1" />
                      ) : (
                        <TrendingDown className="h-4 w-4 mr-1" />
                      )}
                      {metric.change}
                    </div>
                  </div>
                  <div className="w-12 h-12 bg-primary/10 rounded-full flex items-center justify-center">
                    <Icon className="h-6 w-6 text-primary" />
                  </div>
                </div>
              </Card>
            );
          })}
        </div>

        {/* Charts Grid - Real backend generated images */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {processedData?.analysis_results?.chart_urls ? (
            // Display real backend-generated charts
            Object.entries(processedData.analysis_results.chart_urls).map(([chartType, urls], index) => 
              (urls as string[]).map((chartUrl, chartIndex) => {
                const chartName = chartUrl.split('/').pop()?.replace('.png', '') || 'Chart';
                return (
                  <Card key={chartUrl} className="analytics-card animate-chart-appear" style={{ animationDelay: `${(index + chartIndex) * 0.2}s` }}>
                    <div className="mb-6">
                      <h3 className="text-xl font-semibold mb-2">
                        {chartName.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')}
                      </h3>
                      <p className="text-muted-foreground">Generated from your data analysis</p>
                    </div>
                    <div className="h-80 flex items-center justify-center bg-muted/20 rounded-lg">
                      <img 
                        src={`${API_BASE_URL}${chartUrl}`}
                        alt={chartName}
                        className="max-w-full max-h-full object-contain rounded"
                        onError={(e) => {
                          e.currentTarget.style.display = 'none';
                          const parent = e.currentTarget.parentElement;
                          if (parent) {
                            parent.innerHTML = '<div class="text-muted-foreground text-center"><p>Chart could not be loaded</p></div>';
                          }
                        }}
                      />
                    </div>
                  </Card>
                );
              })
            ).flat()
          ) : (
            // Fallback when no processed data - show message instead of fake charts
            <div className="col-span-full">
              <Card className="analytics-card text-center py-20">
                <div className="text-muted-foreground">
                  <BarChart3 className="h-16 w-16 mx-auto mb-4 opacity-50" />
                  <h3 className="text-xl font-semibold mb-2">No Charts Available</h3>
                  <p>Upload and process CSV data to generate real analytical charts</p>
                </div>
              </Card>
            </div>
          )}

          {/* Bar Chart */}
          <Card className="analytics-card animate-chart-appear" style={{ animationDelay: '0.2s' }}>
            <div className="mb-6">
              <h3 className="text-xl font-semibold mb-2">Device Categories</h3>
              <p className="text-muted-foreground">Traffic distribution by device type</p>
            </div>
            <div className="h-80">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={barData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="hsl(var(--border))" />
                  <XAxis 
                    dataKey="category" 
                    stroke="hsl(var(--muted-foreground))"
                    tick={{ fill: 'hsl(var(--muted-foreground))' }}
                  />
                  <YAxis 
                    stroke="hsl(var(--muted-foreground))"
                    tick={{ fill: 'hsl(var(--muted-foreground))' }}
                  />
                  <Tooltip 
                    contentStyle={{
                      backgroundColor: 'hsl(var(--card))',
                      border: '1px solid hsl(var(--border))',
                      borderRadius: '8px',
                    }}
                  />
                  <Bar 
                    dataKey="value" 
                    fill="hsl(var(--chart-1))"
                    radius={[4, 4, 0, 0]}
                  />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </Card>

          {/* Pie Chart */}
          <Card className="analytics-card animate-chart-appear" style={{ animationDelay: '0.4s' }}>
            <div className="mb-6">
              <h3 className="text-xl font-semibold mb-2">Traffic Sources</h3>
              <p className="text-muted-foreground">User acquisition channels</p>
            </div>
            <div className="h-80">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={pieData}
                    cx="50%"
                    cy="50%"
                    outerRadius={80}
                    dataKey="value"
                    label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                  >
                    {pieData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip 
                    contentStyle={{
                      backgroundColor: 'hsl(var(--card))',
                      border: '1px solid hsl(var(--border))',
                      borderRadius: '8px',
                    }}
                  />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </Card>

          {/* Additional Chart Area */}
          <Card className="analytics-card animate-chart-appear" style={{ animationDelay: '0.6s' }}>
            <div className="mb-6">
              <h3 className="text-xl font-semibold mb-2">Performance Metrics</h3>
              <p className="text-muted-foreground">Key performance indicators overview</p>
            </div>
            <div className="space-y-6">
              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span>Click-through Rate</span>
                  <span className="text-primary">3.24%</span>
                </div>
                <div className="w-full bg-muted h-2 rounded-full">
                  <div className="bg-primary h-2 rounded-full" style={{ width: '65%' }}></div>
                </div>
              </div>
              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span>Bounce Rate</span>
                  <span className="text-secondary">1.8%</span>
                </div>
                <div className="w-full bg-muted h-2 rounded-full">
                  <div className="bg-secondary h-2 rounded-full" style={{ width: '35%' }}></div>
                </div>
              </div>
              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span>Session Duration</span>
                  <span className="text-chart-3">4.2min</span>
                </div>
                <div className="w-full bg-muted h-2 rounded-full">
                  <div className="bg-chart-3 h-2 rounded-full" style={{ width: '80%' }}></div>
                </div>
              </div>
            </div>
          </Card>
        </div>
      </div>
    </section>
  );
};

export default DashboardSection;