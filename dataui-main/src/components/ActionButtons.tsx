import React from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Download, FileText, RotateCcw, Share2, FileBarChart } from 'lucide-react';

interface ActionButtonsProps {
  onDownloadPDF: () => void;
  onGenerateComprehensiveReport?: () => void;
  onStartOver: () => void;
  onShare?: () => void;
  isGeneratingPDF?: boolean;
  isGeneratingComprehensiveReport?: boolean;
  fileName: string;
}

export const ActionButtons: React.FC<ActionButtonsProps> = ({
  onDownloadPDF,
  onGenerateComprehensiveReport,
  onStartOver,
  onShare,
  isGeneratingPDF = false,
  isGeneratingComprehensiveReport = false,
  fileName
}) => {
  return (
    <Card className="card-elevated">
      <CardContent className="p-6">
        <div className="flex flex-col sm:flex-row gap-4">
          {/* Primary Actions */}
          <div className="flex-1 space-y-3 sm:space-y-0 sm:space-x-3 sm:flex">
            <Button 
              onClick={onDownloadPDF}
              disabled={isGeneratingPDF || isGeneratingComprehensiveReport}
              className="flex-1 bg-gradient-primary hover:bg-primary-hover"
              size="lg"
            >
              {isGeneratingPDF ? (
                <>
                  <div className="w-4 h-4 border-2 border-current border-t-transparent animate-spin rounded-full mr-2" />
                  Generating PDF...
                </>
              ) : (
                <>
                  <Download className="w-4 h-4 mr-2" />
                  Download PDF Report
                </>
              )}
            </Button>

            {onGenerateComprehensiveReport && (
              <Button 
                onClick={onGenerateComprehensiveReport}
                disabled={isGeneratingPDF || isGeneratingComprehensiveReport}
                className="flex-1 bg-gradient-secondary hover:bg-secondary-hover"
                size="lg"
              >
                {isGeneratingComprehensiveReport ? (
                  <>
                    <div className="w-4 h-4 border-2 border-current border-t-transparent animate-spin rounded-full mr-2" />
                    Generating Report...
                  </>
                ) : (
                  <>
                    <FileBarChart className="w-4 h-4 mr-2" />
                    Comprehensive Report
                  </>
                )}
              </Button>
            )}

            <Button 
              variant="outline" 
              onClick={onStartOver}
              className="flex-1"
              size="lg"
            >
              <RotateCcw className="w-4 h-4 mr-2" />
              Analyze New File
            </Button>
          </div>

          {/* Secondary Actions */}
          <div className="flex gap-3">
            {onShare && (
              <Button 
                variant="outline" 
                onClick={onShare}
                size="lg"
              >
                <Share2 className="w-4 h-4 mr-2" />
                Share
              </Button>
            )}
          </div>
        </div>

        {/* File Info */}
        <div className="mt-4 pt-4 border-t border-border">
          <div className="flex items-center justify-between text-sm">
            <div className="flex items-center gap-2 text-muted-foreground">
              <FileText className="w-4 h-4" />
              <span>Current file: {fileName}</span>
            </div>
            <div className="text-xs text-muted-foreground">
              Analysis completed
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};