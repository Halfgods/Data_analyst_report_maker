import React from 'react';
import { Logo } from './Logo';
import { NavigationMenu } from './NavigationMenu';

interface HeaderProps {
  className?: string;
}

export const Header: React.FC<HeaderProps> = ({ className = '' }) => {
  return (
    <header className={`w-full bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 border-b border-border/40 ${className}`}>
      <div className="container mx-auto px-4 py-3">
        <div className="flex items-center justify-between">
          {/* Logo on the left */}
          <div className="flex items-center">
            <Logo size="md" />
          </div>
          
          {/* Right side - navigation menu */}
          <div className="flex items-center space-x-4">
            <NavigationMenu />
          </div>
        </div>
      </div>
    </header>
  );
};
