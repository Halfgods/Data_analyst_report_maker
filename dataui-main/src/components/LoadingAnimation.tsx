import React from 'react';
import { Logo } from './Logo';

interface LoadingAnimationProps {
  message?: string;
  subMessage?: string;
}

export const LoadingAnimation: React.FC<LoadingAnimationProps> = ({ 
  message = "Analyzing Your Data", 
  subMessage = "This may take a few moments..." 
}) => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-background">
      <div className="text-center space-y-6 max-w-md mx-auto px-4">
        {/* Logo with Animation */}
        <div className="flex justify-center">
          <div className="relative">
            <Logo size="lg" className="animate-pulse" />
            {/* Rotating Ring around logo */}
            <div className="absolute inset-0 rounded-full border-2 border-primary border-t-transparent animate-spin" />
          </div>
        </div>

        {/* Main Message */}
        <div className="space-y-2">
          <h2 className="text-2xl font-bold text-foreground animate-pulse">
            {message}
          </h2>
          <p className="text-muted-foreground text-sm">
            {subMessage}
          </p>
        </div>

        {/* Progress Indicators */}
        <div className="flex justify-center space-x-2">
          {[0, 1, 2, 3].map((i) => (
            <div
              key={i}
              className="w-3 h-3 bg-gradient-to-r from-primary to-secondary rounded-full animate-bounce shadow-lg"
              style={{
                animationDelay: `${i * 0.15}s`,
                animationDuration: '1.2s'
              }}
            />
          ))}
        </div>

        {/* Analysis Steps */}
        <div className="space-y-3 text-left bg-muted/20 rounded-lg p-4">
          <div className="flex items-center space-x-3">
            <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
            <span className="text-sm text-muted-foreground">Uploading CSV file</span>
          </div>
          <div className="flex items-center space-x-3">
            <div className="w-2 h-2 bg-blue-500 rounded-full animate-pulse" />
            <span className="text-sm text-muted-foreground">Processing data structure</span>
          </div>
          <div className="flex items-center space-x-3">
            <div className="w-2 h-2 bg-purple-500 rounded-full animate-pulse" />
            <span className="text-sm text-muted-foreground">Generating AI insights</span>
          </div>
          <div className="flex items-center space-x-3">
            <div className="w-2 h-2 bg-orange-500 rounded-full animate-pulse" />
            <span className="text-sm text-muted-foreground">Creating visualizations</span>
          </div>
        </div>

        {/* Fun Fact */}
        <div className="text-xs text-muted-foreground bg-muted/10 rounded p-2">
          💡 Did you know? AI analysis can reveal patterns invisible to the human eye!
        </div>
      </div>
    </div>
  );
};
