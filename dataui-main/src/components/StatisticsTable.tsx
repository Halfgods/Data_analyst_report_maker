import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { BarChart3 } from 'lucide-react';

interface StatisticsData {
  [column: string]: {
    count: number;
    mean?: number;
    std?: number;
    min?: number | string;
    max?: number | string;
    '25%'?: number;
    '50%'?: number;
    '75%'?: number;
    unique?: number;
    type: 'numeric' | 'categorical';
  };
}

interface StatisticsTableProps {
  data: StatisticsData;
}

export const StatisticsTable: React.FC<StatisticsTableProps> = ({ data }) => {
  const formatValue = (value: number | string | undefined): string => {
    if (value === undefined || value === null) return '-';
    if (typeof value === 'number') {
      return value.toFixed(2);
    }
    return String(value);
  };

  const numericColumns = Object.entries(data).filter(([_, stats]) => stats.type === 'numeric');
  const categoricalColumns = Object.entries(data).filter(([_, stats]) => stats.type === 'categorical');

  return (
    <div className="space-y-6">
      {/* Numeric Statistics */}
      {numericColumns.length > 0 && (
        <Card className="card-elevated">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <BarChart3 className="w-5 h-5 text-primary" />
              Numeric Column Statistics
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="overflow-x-auto">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead className="font-semibold">Column</TableHead>
                    <TableHead className="text-center">Count</TableHead>
                    <TableHead className="text-center">Mean</TableHead>
                    <TableHead className="text-center">Std Dev</TableHead>
                    <TableHead className="text-center">Min</TableHead>
                    <TableHead className="text-center">25%</TableHead>
                    <TableHead className="text-center">50%</TableHead>
                    <TableHead className="text-center">75%</TableHead>
                    <TableHead className="text-center">Max</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {numericColumns.map(([column, stats]) => (
                    <TableRow key={column} className="hover:bg-surface/50">
                      <TableCell className="font-medium">{column}</TableCell>
                      <TableCell className="text-center">{stats.count.toLocaleString()}</TableCell>
                      <TableCell className="text-center">{formatValue(stats.mean)}</TableCell>
                      <TableCell className="text-center">{formatValue(stats.std)}</TableCell>
                      <TableCell className="text-center">{formatValue(stats.min)}</TableCell>
                      <TableCell className="text-center">{formatValue(stats['25%'])}</TableCell>
                      <TableCell className="text-center">{formatValue(stats['50%'])}</TableCell>
                      <TableCell className="text-center">{formatValue(stats['75%'])}</TableCell>
                      <TableCell className="text-center">{formatValue(stats.max)}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Categorical Statistics */}
      {categoricalColumns.length > 0 && (
        <Card className="card-elevated">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <BarChart3 className="w-5 h-5 text-secondary" />
              Categorical Column Statistics
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="overflow-x-auto">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead className="font-semibold">Column</TableHead>
                    <TableHead className="text-center">Count</TableHead>
                    <TableHead className="text-center">Unique Values</TableHead>
                    <TableHead className="text-center">Most Frequent</TableHead>
                    <TableHead className="text-center">Least Frequent</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {categoricalColumns.map(([column, stats]) => (
                    <TableRow key={column} className="hover:bg-surface/50">
                      <TableCell className="font-medium">{column}</TableCell>
                      <TableCell className="text-center">{stats.count.toLocaleString()}</TableCell>
                      <TableCell className="text-center">{stats.unique || '-'}</TableCell>
                      <TableCell className="text-center">{formatValue(stats.max)}</TableCell>
                      <TableCell className="text-center">{formatValue(stats.min)}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
};