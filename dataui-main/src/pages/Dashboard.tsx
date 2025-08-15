import React, { useState } from 'react';
import { DataOverview } from '@/components/DataOverview';
import { StatisticsTable } from '@/components/StatisticsTable';
import { ChartDisplay } from '@/components/ChartDisplay';
import { AIInsights } from '@/components/AIInsights';
import { ActionButtons } from '@/components/ActionButtons';
import { PDFPreview } from '@/components/PDFPreview';
import { ThemeToggle } from '@/components/ThemeToggle';
import { Button } from '@/components/ui/button';
import { ArrowLeft } from 'lucide-react';

// Backend API configuration
const API_BASE_URL = 'http://127.0.0.1:8000';

// Mock data types for demonstration
interface DashboardData {
  fileName: string;
  rowCount: number;
  columnCount: number;
  columnTypes: Record<string, string>;
  fileSize: string;
  statistics: any;
  charts: any[];
  insights: string[];
  sessionId?: string;
  rawBackendData?: any;
}

interface DashboardProps {
  data: DashboardData;
  onBackToUpload: () => void;
}

export const Dashboard: React.FC<DashboardProps> = ({ data, onBackToUpload }) => {
  const [isGeneratingPDF, setIsGeneratingPDF] = useState(false);
  const [isGeneratingComprehensiveReport, setIsGeneratingComprehensiveReport] = useState(false);
  const [pdfInfo, setPdfInfo] = useState<any>(null);
  const [pdfUrl, setPdfUrl] = useState<string | null>(null);
  const [comprehensiveReportInfo, setComprehensiveReportInfo] = useState<any>(null);
  const [aiResponse, setAiResponse] = useState<string>('');
  const [isAskingAI, setIsAskingAI] = useState(false);

  const handleDownloadPDF = async () => {
    if (!data.sessionId) {
      console.error('No session ID available for PDF generation');
      return;
    }

    setIsGeneratingPDF(true);
    try {
      const response = await fetch(`${API_BASE_URL}/generate-report/${data.sessionId}`, {
        method: 'POST'
      });
      
      if (!response.ok) {
        throw new Error('PDF generation failed');
      }
      
      const result = await response.json();
      setPdfInfo(result.pdf_info);
      
      // Set PDF URL for preview
      if (result.pdf_info && result.pdf_info.download_url) {
        setPdfUrl(`${API_BASE_URL}${result.pdf_info.download_url}`);
      }
      
      // Automatically trigger download
      if (result.pdf_info && result.pdf_info.download_url) {
        const downloadLink = document.createElement('a');
        downloadLink.href = `${API_BASE_URL}${result.pdf_info.download_url}`;
        downloadLink.download = result.pdf_info.filename;
        document.body.appendChild(downloadLink);
        downloadLink.click();
        document.body.removeChild(downloadLink);
      }
    } catch (error) {
      console.error('Error generating PDF:', error);
    } finally {
      setIsGeneratingPDF(false);
    }
  };

  const handleAskQuestion = async (question: string) => {
    if (!data.sessionId) {
      console.error('No session ID available for AI questions');
      return;
    }

    setIsAskingAI(true);
    setAiResponse('');

    try {
      const response = await fetch(`${API_BASE_URL}/query-data/${data.sessionId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ question })
      });
      
      if (!response.ok) {
        throw new Error('AI question failed');
      }
      
      const result = await response.json();
      console.log('AI Response:', result);
      
      // Extract the response text
      if (result.answer) {
        setAiResponse(result.answer);
      } else if (result.commentary) {
        setAiResponse(result.commentary);
      } else {
        setAiResponse('AI response received but no content found.');
      }
    } catch (error) {
      console.error('Error asking AI question:', error);
      setAiResponse('Error: Failed to get AI response. Please try again.');
    } finally {
      setIsAskingAI(false);
    }
  };

  const handleGenerateComprehensiveReport = async () => {
    if (!data.sessionId) {
      console.error('No session ID available for comprehensive report generation');
      return;
    }

    setIsGeneratingComprehensiveReport(true);
    try {
      const response = await fetch(`${API_BASE_URL}/generate-comprehensive-report/${data.sessionId}`, {
        method: 'POST'
      });
      
      if (!response.ok) {
        throw new Error('Comprehensive report generation failed');
      }
      
      const result = await response.json();
      setComprehensiveReportInfo(result);
      
      // Automatically trigger download
      if (result.download_url) {
        const downloadLink = document.createElement('a');
        downloadLink.href = `${API_BASE_URL}${result.download_url}`;
        downloadLink.download = result.report_filename;
        document.body.appendChild(downloadLink);
        downloadLink.click();
        document.body.removeChild(downloadLink);
      }
    } catch (error) {
      console.error('Error generating comprehensive report:', error);
    } finally {
      setIsGeneratingComprehensiveReport(false);
    }
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <div className="bg-surface-elevated border-b border-border sticky top-0 z-10 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center gap-4">
              <Button 
                variant="ghost" 
                onClick={onBackToUpload}
                className="flex items-center gap-2 focus-enhanced"
              >
                <ArrowLeft className="w-4 h-4" />
                Back to Upload
              </Button>
              <div>
                <h1 className="text-xl font-bold">Analysis Results</h1>
                <p className="text-sm text-muted-foreground">{data.fileName}</p>
              </div>
            </div>
            <ThemeToggle />
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="space-y-8">
          {/* Data Overview */}
          <section>
            <DataOverview
              fileName={data.fileName}
              rowCount={data.rowCount}
              columnCount={data.columnCount}
              columnTypes={data.columnTypes}
              fileSize={data.fileSize}
            />
          </section>

          {/* Statistics */}
          <section>
            <h2 className="text-2xl font-bold mb-6">Statistical Summary</h2>
            <StatisticsTable data={data.statistics} />
          </section>

          {/* Charts */}
          <section>
            <ChartDisplay charts={data.charts} />
          </section>

          {/* AI Insights */}
          <section>
            <AIInsights 
              insights={data.insights}
              onAskQuestion={handleAskQuestion}
              isLoading={isAskingAI}
              aiResponse={aiResponse}
            />
          </section>

          {/* PDF Preview */}
          <section>
            <h2 className="text-2xl font-bold mb-6">Report Preview</h2>
            <PDFPreview
              fileName={data.fileName}
              isGenerating={isGeneratingPDF}
              onDownload={handleDownloadPDF}
              pdfUrl={pdfUrl || undefined}
              pdfInfo={pdfInfo}
            />
          </section>

          {/* Action Buttons */}
          <section>
            <ActionButtons
              onDownloadPDF={handleDownloadPDF}
              onGenerateComprehensiveReport={handleGenerateComprehensiveReport}
              onStartOver={onBackToUpload}
              isGeneratingPDF={isGeneratingPDF}
              isGeneratingComprehensiveReport={isGeneratingComprehensiveReport}
              fileName={data.fileName}
            />
          </section>
        </div>
      </div>
    </div>
  );
};