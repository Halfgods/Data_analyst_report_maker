import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Home, Upload, BarChart3, Settings } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { useNavigation } from '@/contexts/NavigationContext';

export const NavigationMenu: React.FC = () => {
  const location = useLocation();
  const { currentSession, clearSession } = useNavigation();

  const navItems = [
    { path: '/', label: 'Home', icon: <Home className="w-4 h-4" /> },
    { path: '/upload', label: 'Upload', icon: <Upload className="w-4 h-4" /> },
    ...(currentSession ? [
      { path: '/dashboard', label: 'Dashboard', icon: <BarChart3 className="w-4 h-4" /> }
    ] : []),
  ];

  const handleClearSession = () => {
    clearSession();
  };

  return (
    <nav className="flex items-center space-x-2">
      {navItems.map((item) => (
        <Link key={item.path} to={item.path}>
          <Button
            variant={location.pathname === item.path ? "default" : "ghost"}
            size="sm"
            className="flex items-center space-x-2"
          >
            {item.icon}
            <span className="hidden sm:inline">{item.label}</span>
          </Button>
        </Link>
      ))}
      
      {currentSession && (
        <Button
          variant="outline"
          size="sm"
          onClick={handleClearSession}
          className="text-destructive hover:text-destructive"
        >
          Clear Session
        </Button>
      )}
    </nav>
  );
};
