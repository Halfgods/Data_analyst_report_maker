import React, { useCallback, useState } from 'react';
import { Upload, FileText, AlertCircle } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { ThemeToggle } from '@/components/ThemeToggle';

interface FileUploadProps {
  onFilesSelected: (files: File[]) => void;
  isLoading?: boolean;
}

export const FileUpload: React.FC<FileUploadProps> = ({ onFilesSelected, isLoading }) => {
  const [dragActive, setDragActive] = useState(false);
  const [files, setFiles] = useState<File[]>([]);
  const [error, setError] = useState<string>('');

  const handleDrag = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  }, []);

  const validateFile = (file: File): boolean => {
    if (file.type !== 'text/csv' && !file.name.endsWith('.csv')) {
      setError('Please select CSV files only');
      return false;
    }
    if (file.size > 100 * 1024 * 1024) { // 100MB limit
      setError('File size must be less than 100MB');
      return false;
    }
    setError('');
    return true;
  };

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    const droppedFiles = Array.from(e.dataTransfer.files);
    const validFiles = droppedFiles.filter(validateFile);
    
    if (validFiles.length > 0) {
      setFiles(validFiles);
    }
  }, []);

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFiles = Array.from(e.target.files || []);
    const validFiles = selectedFiles.filter(validateFile);
    
    if (validFiles.length > 0) {
      setFiles(validFiles);
    }
  };

  const handleAnalyze = () => {
    if (files.length > 0) {
      onFilesSelected(files);
    }
  };

  const removeFile = (index: number) => {
    setFiles(files.filter((_, i) => i !== index));
  };

  return (
    <div className="w-full max-w-2xl mx-auto space-y-6">
      {/* Header with Theme Toggle */}
      <div className="text-center space-y-2 relative">
        <div className="absolute top-0 right-0">
          <ThemeToggle />
        </div>
        <h1 className="text-3xl font-bold text-foreground">CSV Data Analyzer</h1>
        <p className="text-muted-foreground">Upload your CSV files to get instant insights and analysis</p>
      </div>

      <Card className="card-elevated">
        <CardContent className="p-8">
          <div
            className={`upload-zone rounded-lg p-12 text-center transition-all ${
              dragActive ? 'drag-active' : ''
            }`}
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
          >
            <Upload className="w-16 h-16 mx-auto mb-4 text-muted-foreground" />
            <h3 className="text-lg font-semibold mb-2">Drop your CSV files here</h3>
            <p className="text-muted-foreground mb-4">or click to browse files</p>
            
            <input
              type="file"
              multiple
              accept=".csv"
              onChange={handleFileInput}
              className="hidden"
              id="file-input"
              disabled={isLoading}
            />
            
            <Button 
              variant="outline" 
              onClick={() => document.getElementById('file-input')?.click()}
              disabled={isLoading}
              className="mb-4"
            >
              Select Files
            </Button>
            
            <p className="text-xs text-muted-foreground">
              Supports multiple CSV files up to 100MB each
            </p>
          </div>

          {error && (
            <div className="mt-4 p-3 bg-destructive/10 border border-destructive/20 rounded-lg flex items-center gap-2">
              <AlertCircle className="w-4 h-4 text-destructive" />
              <span className="text-sm text-destructive">{error}</span>
            </div>
          )}

          {files.length > 0 && (
            <div className="mt-6 space-y-3">
              <h4 className="font-medium">Selected Files:</h4>
              {files.map((file, index) => (
                <div key={index} className="flex items-center justify-between p-3 bg-surface rounded-lg">
                  <div className="flex items-center gap-3">
                    <FileText className="w-5 h-5 text-primary" />
                    <div>
                      <p className="font-medium text-sm">{file.name}</p>
                      <p className="text-xs text-muted-foreground">
                        {(file.size / 1024 / 1024).toFixed(2)} MB
                      </p>
                    </div>
                  </div>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => removeFile(index)}
                    disabled={isLoading}
                  >
                    Remove
                  </Button>
                </div>
              ))}
              
              <Button 
                onClick={handleAnalyze} 
                disabled={isLoading || files.length === 0}
                className="w-full bg-gradient-primary hover:bg-primary-hover"
                size="lg"
              >
                {isLoading ? 'Analyzing...' : 'Analyze Data'}
              </Button>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
};