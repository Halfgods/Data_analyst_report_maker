import React, { useState } from 'react';
import { FileUpload } from '@/components/FileUpload';
import { Dashboard } from '@/pages/Dashboard';

// Backend API configuration
const API_BASE_URL = 'http://127.0.0.1:8000';

// Transform backend data to frontend format
const transformBackendData = (backendResponse: any, fileName: string) => {
  const csvMetadata = backendResponse.csv_metadata.files[0];
  const analysisResults = backendResponse.analysis_results;
  
  // Transform statistics
  const statistics: any = {};
  Object.entries(analysisResults.descriptive_statistics || {}).forEach(([key, stats]: [string, any]) => {
    statistics[key] = {
      ...stats,
      type: 'numeric' as const
    };
  });

  // Transform charts - convert backend chart URLs to chart objects
  const charts: any[] = [];
  if (analysisResults.chart_urls) {
    Object.entries(analysisResults.chart_urls).forEach(([chartType, urls]: [string, any]) => {
      urls.forEach((url: string, index: number) => {
        const chartName = url.split('/').pop()?.replace('.html', '') || `${chartType}_${index}`;
        charts.push({
          id: chartName,
          title: chartName.split('_').map((word: string) => word.charAt(0).toUpperCase() + word.slice(1)).join(' '),
          type: chartType.slice(0, -1) as const, // Remove 's' from plural (histograms -> histogram)
          description: `Interactive ${chartType.slice(0, -1)} chart`,
          url: `${API_BASE_URL}${url}` // Full URL for iframe
        });
      });
    });
  }

  // Split AI commentary into insights array and clean markdown
  const insights = backendResponse.ai_commentary 
    ? backendResponse.ai_commentary
        .split('\n\n')
        .filter((insight: string) => insight.trim().length > 0)
        .map((insight: string) => {
          // Clean markdown formatting and remove any numbering
          return insight
            .replace(/\*\*(.*?)\*\*/g, '$1') // Remove bold
            .replace(/\*(.*?)\*/g, '$1') // Remove italic
            .replace(/^\d+\.\s*/, '') // Remove numbered prefixes
            .replace(/^[A-Z]\.\s*/, '') // Remove letter prefixes
            .replace(/^Insight\s*\d*:?\s*/i, '') // Remove "Insight X:" prefixes
            .trim();
        })
        .slice(0, 4) // Ensure exactly 4 insights
    : [];

  return {
    sessionId: backendResponse.session_id,
    fileName,
    rowCount: csvMetadata.rows,
    columnCount: csvMetadata.columns.length,
    columnTypes: csvMetadata.inferred_types,
    fileSize: `${csvMetadata.file_size_mb?.toFixed(2) || (csvMetadata.file_size_bytes / 1024 / 1024).toFixed(2)} MB`,
    statistics,
    charts,
    insights: insights.slice(0, 4), // Limit to first 4 insights
    rawBackendData: backendResponse // Keep original data for other uses
  };
};
// API functions for backend communication
const uploadFiles = async (files: File[]) => {
  const formData = new FormData();
  files.forEach(file => formData.append('files', file));
  
  const response = await fetch(`${API_BASE_URL}/upload-csv/`, {
    method: 'POST',
    body: formData
  });
  
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'File upload failed');
  }
  
  return response.json();
};

const processData = async (sessionId: string) => {
  const response = await fetch(`${API_BASE_URL}/process-data/${sessionId}`, {
    method: 'POST'
  });
  
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Data processing failed');
  }
  
  return response.json();
};

type AppState = 'upload' | 'processing' | 'dashboard';

const Index = () => {
  const [appState, setAppState] = useState<AppState>('upload');
  const [dashboardData, setDashboardData] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleFilesSelected = async (files: File[]) => {
    setIsLoading(true);
    setAppState('processing');

    try {
      // Step 1: Upload files to backend
      const uploadResult = await uploadFiles(files);
      const sessionId = uploadResult.session_id;

      // Step 2: Process data and get analysis results
      const analysisData = await processData(sessionId);

      // Step 3: Transform backend data to frontend format
      const transformedData = transformBackendData(analysisData, files[0].name);

      setDashboardData(transformedData);
      setAppState('dashboard');
    } catch (error) {
      console.error('Error processing files:', error);
      // You could add error state handling here if needed
      setAppState('upload');
    } finally {
      setIsLoading(false);
    }
  };

  const handleBackToUpload = () => {
    setAppState('upload');
    setDashboardData(null);
  };

  if (appState === 'processing') {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <div className="text-center space-y-4">
          <div className="w-16 h-16 border-4 border-primary border-t-transparent animate-spin rounded-full mx-auto" />
          <h2 className="text-2xl font-bold">Analyzing Your Data</h2>
          <p className="text-muted-foreground">This may take a few moments...</p>
        </div>
      </div>
    );
  }

  if (appState === 'dashboard' && dashboardData) {
    return (
      <Dashboard 
        data={dashboardData} 
        onBackToUpload={handleBackToUpload} 
      />
    );
  }

  return (
    <div className="min-h-screen bg-background py-12">
      <div className="container mx-auto px-4">
        <FileUpload 
          onFilesSelected={handleFilesSelected}
          isLoading={isLoading}
        />
      </div>
    </div>
  );
};

export default Index;
