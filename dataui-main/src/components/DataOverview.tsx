import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { FileText, Database, Columns, Rows } from 'lucide-react';

interface DataOverviewProps {
  fileName: string;
  rowCount: number;
  columnCount: number;
  columnTypes: Record<string, string>;
  fileSize: string;
}

export const DataOverview: React.FC<DataOverviewProps> = ({
  fileName,
  rowCount,
  columnCount,
  columnTypes,
  fileSize
}) => {
  const typeColors: Record<string, string> = {
    string: 'bg-chart-1/10 text-chart-1',
    number: 'bg-chart-2/10 text-chart-2',
    date: 'bg-chart-3/10 text-chart-3',
    boolean: 'bg-chart-4/10 text-chart-4',
  };

  return (
    <Card className="card-elevated">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <FileText className="w-5 h-5 text-primary" />
          Data Overview
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-6">
        {/* File Info */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="text-center p-4 bg-surface rounded-lg">
            <Database className="w-8 h-8 mx-auto mb-2 text-primary" />
            <p className="text-2xl font-bold text-foreground">{rowCount.toLocaleString()}</p>
            <p className="text-sm text-muted-foreground">Rows</p>
          </div>
          
          <div className="text-center p-4 bg-surface rounded-lg">
            <Columns className="w-8 h-8 mx-auto mb-2 text-secondary" />
            <p className="text-2xl font-bold text-foreground">{columnCount}</p>
            <p className="text-sm text-muted-foreground">Columns</p>
          </div>
          
          <div className="text-center p-4 bg-surface rounded-lg">
            <FileText className="w-8 h-8 mx-auto mb-2 text-accent" />
            <p className="text-2xl font-bold text-foreground">{fileSize}</p>
            <p className="text-sm text-muted-foreground">File Size</p>
          </div>
          
          <div className="text-center p-4 bg-surface rounded-lg">
            <Rows className="w-8 h-8 mx-auto mb-2 text-chart-4" />
            <p className="text-2xl font-bold text-foreground">{Object.keys(columnTypes).length}</p>
            <p className="text-sm text-muted-foreground">Data Types</p>
          </div>
        </div>

        {/* File Name */}
        <div>
          <h4 className="font-medium mb-2">File Name</h4>
          <p className="text-sm text-muted-foreground bg-surface p-3 rounded-lg font-mono">
            {fileName}
          </p>
        </div>

        {/* Column Types */}
        <div>
          <h4 className="font-medium mb-3">Column Data Types</h4>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {Object.entries(columnTypes).map(([column, type]) => (
              <div key={column} className="flex items-center justify-between p-3 bg-surface rounded-lg">
                <span className="font-medium text-sm truncate">{column}</span>
                <Badge 
                  variant="secondary" 
                  className={`ml-2 ${typeColors[type] || 'bg-muted text-muted-foreground'}`}
                >
                  {type}
                </Badge>
              </div>
            ))}
          </div>
        </div>
      </CardContent>
    </Card>
  );
};