import React from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { useNavigation } from '@/contexts/NavigationContext';

interface RouteGuardProps {
  children: React.ReactNode;
  requireSession?: boolean;
  requireFile?: boolean;
  redirectTo?: string;
}

export const RouteGuard: React.FC<RouteGuardProps> = ({ 
  children, 
  requireSession = false, 
  requireFile = false, 
  redirectTo = '/' 
}) => {
  const { currentSession, currentFile } = useNavigation();
  const location = useLocation();

  // Check if session is required but not present
  if (requireSession && !currentSession) {
    return <Navigate to={redirectTo} state={{ from: location }} replace />;
  }

  // Check if file is required but not present
  if (requireFile && !currentFile) {
    return <Navigate to={redirectTo} state={{ from: location }} replace />;
  }

  return <>{children}</>;
};
