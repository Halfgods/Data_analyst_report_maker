import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Header } from '@/components/Header';
import { BreadcrumbNav } from '@/components/BreadcrumbNav';
import { FileUpload } from '@/components/FileUpload';
import { useNavigation } from '@/contexts/NavigationContext';

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
          type: chartType.slice(0, -1) as const,
          description: `Interactive ${chartType.slice(0, -1)} chart`,
          url: `${API_BASE_URL}${url}`
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
          return insight
            .replace(/\*\*(.*?)\*\*/g, '$1')
            .replace(/\*(.*?)\*/g, '$1')
            .replace(/^\d+\.\s*/, '')
            .replace(/^[A-Z]\.\s*/, '')
            .replace(/^Insight\s*\d*:?\s*/i, '')
            .trim();
        })
        .slice(0, 4)
    : [];

  return {
    sessionId: backendResponse.session_id || 'fallback-session-id',
    fileName,
    rowCount: csvMetadata.rows,
    columnCount: csvMetadata.columns.length,
    columnTypes: csvMetadata.inferred_types,
    fileSize: `${csvMetadata.file_size_mb?.toFixed(2) || (csvMetadata.file_size_bytes / 1024 / 1024).toFixed(2)} MB`,
    statistics,
    charts,
    insights: insights.slice(0, 4),
    rawBackendData: backendResponse
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

const Upload: React.FC = () => {
  const navigate = useNavigate();
  const { setCurrentSession, setCurrentFile, setIsProcessing } = useNavigation();
  const [isLoading, setIsLoading] = useState(false);

  const handleFilesSelected = async (files: File[]) => {
    setIsLoading(true);
    setIsProcessing(true);

    try {
      // Step 1: Upload files to backend
      const uploadResult = await uploadFiles(files);
      const sessionId = uploadResult.session_id;

      // Step 2: Process data and get analysis results
      const analysisData = await processData(sessionId);

      // Step 3: Transform backend data to frontend format
      const transformedData = transformBackendData(analysisData, files[0].name);
      
      console.log('Upload - Backend analysis data:', analysisData);
      console.log('Upload - Transformed data:', transformedData);
      console.log('Upload - Session ID:', sessionId);

      // Set navigation context
      setCurrentSession(sessionId);
      setCurrentFile(files[0].name);

      // Navigate to processing page first
      navigate('/processing', { replace: true });
      
      // Simulate processing time and then navigate to dashboard
      setTimeout(() => {
        navigate('/dashboard', { 
          state: { dashboardData: transformedData },
          replace: true 
        });
      }, 3000); // Show processing for 3 seconds
    } catch (error) {
      console.error('Error processing files:', error);
      // Reset processing state
      setIsProcessing(false);
      // You could add error state handling here if needed
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-background">
      <Header />
      <BreadcrumbNav />
      
      <div className="container mx-auto px-4 py-12">
        <div className="max-w-4xl mx-auto">
          <div className="text-center mb-12">
            <h1 className="text-4xl font-bold text-foreground mb-4">
              Upload Your CSV File
            </h1>
            <p className="text-xl text-muted-foreground">
              Get instant AI-powered analysis, insights, and visualizations
            </p>
          </div>

          <div className="bg-card border rounded-lg p-8 shadow-lg">
            <FileUpload 
              onFilesSelected={handleFilesSelected}
              isLoading={isLoading}
            />
          </div>

          {/* File Requirements */}
          <div className="mt-12 grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="text-center p-6 bg-muted/20 rounded-lg">
              <div className="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl font-bold text-primary">📊</span>
              </div>
              <h3 className="font-semibold mb-2">CSV Format</h3>
              <p className="text-sm text-muted-foreground">
                Upload files in CSV format with headers in the first row
              </p>
            </div>

            <div className="text-center p-6 bg-muted/20 rounded-lg">
              <div className="w-16 h-16 bg-secondary/10 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl font-bold text-secondary">📏</span>
              </div>
              <h3 className="font-semibold mb-2">Size Limit</h3>
              <p className="text-sm text-muted-foreground">
                Maximum file size: 100MB for optimal performance
              </p>
            </div>

            <div className="text-center p-6 bg-muted/20 rounded-lg">
              <div className="w-16 h-16 bg-accent/10 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl font-bold text-accent">🔒</span>
              </div>
              <h3 className="font-semibold mb-2">Privacy First</h3>
              <p className="text-sm text-muted-foreground">
                Your data is processed locally and never shared
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Upload;
