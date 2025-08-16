import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Header } from '@/components/Header';
import { BreadcrumbNav } from '@/components/BreadcrumbNav';
import { LoadingAnimation } from '@/components/LoadingAnimation';
import { useNavigation } from '@/contexts/NavigationContext';

const Processing: React.FC = () => {
  const navigate = useNavigate();
  const { isProcessing, currentSession, currentFile } = useNavigation();

  useEffect(() => {
    // If not processing, redirect to home
    if (!isProcessing) {
      navigate('/', { replace: true });
      return;
    }

    // If no session, redirect to upload
    if (!currentSession) {
      navigate('/upload', { replace: true });
      return;
    }
  }, [isProcessing, currentSession, navigate]);

  // If not processing, don't render anything (will redirect)
  if (!isProcessing || !currentSession) {
    return null;
  }

  return (
    <div className="min-h-screen bg-background">
      <Header />
      <BreadcrumbNav />
      
      <LoadingAnimation 
        message="Analyzing Your Data"
        subMessage={`Processing ${currentFile || 'your CSV file'} with AI-powered algorithms...`}
      />
    </div>
  );
};

export default Processing;
