import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { ChevronRight, Home, Upload, BarChart3, FileText } from 'lucide-react';
import { useNavigation } from '@/contexts/NavigationContext';

interface BreadcrumbItem {
  label: string;
  path: string;
  icon: React.ReactNode;
  isActive?: boolean;
}

export const BreadcrumbNav: React.FC = () => {
  const location = useLocation();
  const { currentFile, isProcessing } = useNavigation();

  const getBreadcrumbs = (): BreadcrumbItem[] => {
    const pathname = location.pathname;
    
    if (pathname === '/') {
      return [
        { label: 'Home', path: '/', icon: <Home className="w-4 h-4" />, isActive: true }
      ];
    }
    
    if (pathname === '/upload') {
      return [
        { label: 'Home', path: '/', icon: <Home className="w-4 h-4" /> },
        { label: 'Upload CSV', path: '/upload', icon: <Upload className="w-4 h-4" />, isActive: true }
      ];
    }
    
    if (pathname === '/processing') {
      return [
        { label: 'Home', path: '/', icon: <Home className="w-4 h-4" /> },
        { label: 'Upload CSV', path: '/upload', icon: <Upload className="w-4 h-4" /> },
        { label: 'Processing', path: '/processing', icon: <BarChart3 className="w-4 h-4" />, isActive: true }
      ];
    }
    
    if (pathname === '/dashboard') {
      return [
        { label: 'Home', path: '/', icon: <Home className="w-4 h-4" /> },
        { label: 'Upload CSV', path: '/upload', icon: <Upload className="w-4 h-4" /> },
        { label: 'Processing', path: '/processing', icon: <BarChart3 className="w-4 h-4" /> },
        { 
          label: currentFile ? `Analysis: ${currentFile}` : 'Dashboard', 
          path: '/dashboard', 
          icon: <FileText className="w-4 h-4" />, 
          isActive: true 
        }
      ];
    }
    
    return [
      { label: 'Home', path: '/', icon: <Home className="w-4 h-4" /> }
    ];
  };

  const breadcrumbs = getBreadcrumbs();

  if (breadcrumbs.length <= 1) {
    return null;
  }

  return (
    <nav className="bg-muted/30 border-b border-border/40 px-4 py-2">
      <div className="container mx-auto">
        <ol className="flex items-center space-x-2 text-sm">
          {breadcrumbs.map((item, index) => (
            <li key={item.path} className="flex items-center">
              {index > 0 && (
                <ChevronRight className="w-4 h-4 text-muted-foreground mx-2" />
              )}
              
              {item.isActive ? (
                <span className="flex items-center space-x-1 text-foreground font-medium">
                  {item.icon}
                  <span>{item.label}</span>
                </span>
              ) : (
                <Link
                  to={item.path}
                  className="flex items-center space-x-1 text-muted-foreground hover:text-foreground transition-colors"
                >
                  {item.icon}
                  <span>{item.label}</span>
                </Link>
              )}
            </li>
          ))}
        </ol>
      </div>
    </nav>
  );
};
