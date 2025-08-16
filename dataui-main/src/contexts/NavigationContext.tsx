import React, { createContext, useContext, useState, ReactNode } from 'react';

interface NavigationContextType {
  currentSession: string | null;
  setCurrentSession: (sessionId: string | null) => void;
  currentFile: string | null;
  setCurrentFile: (fileName: string | null) => void;
  isProcessing: boolean;
  setIsProcessing: (processing: boolean) => void;
  clearSession: () => void;
}

const NavigationContext = createContext<NavigationContextType | undefined>(undefined);

export const useNavigation = () => {
  const context = useContext(NavigationContext);
  if (context === undefined) {
    throw new Error('useNavigation must be used within a NavigationProvider');
  }
  return context;
};

interface NavigationProviderProps {
  children: ReactNode;
}

export const NavigationProvider: React.FC<NavigationProviderProps> = ({ children }) => {
  const [currentSession, setCurrentSession] = useState<string | null>(null);
  const [currentFile, setCurrentFile] = useState<string | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);

  const clearSession = () => {
    setCurrentSession(null);
    setCurrentFile(null);
    setIsProcessing(false);
  };

  const value: NavigationContextType = {
    currentSession,
    setCurrentSession,
    currentFile,
    setCurrentFile,
    isProcessing,
    setIsProcessing,
    clearSession,
  };

  return (
    <NavigationContext.Provider value={value}>
      {children}
    </NavigationContext.Provider>
  );
};
