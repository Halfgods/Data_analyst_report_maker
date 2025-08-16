import React from 'react';
import { Logo } from './Logo';

export const LogoDemo: React.FC = () => {
  return (
    <div className="p-8 space-y-8">
      <h1 className="text-3xl font-bold text-center mb-8">Logo & Animation Demo</h1>
      
      {/* Logo Sizes */}
      <div className="space-y-4">
        <h2 className="text-xl font-semibold">Logo Sizes</h2>
        <div className="flex items-center space-x-8">
          <div className="text-center">
            <Logo size="sm" />
            <p className="text-sm text-muted-foreground mt-2">Small</p>
          </div>
          <div className="text-center">
            <Logo size="md" />
            <p className="text-sm text-muted-foreground mt-2">Medium</p>
          </div>
          <div className="text-center">
            <Logo size="lg" />
            <p className="text-sm text-muted-foreground mt-2">Large</p>
          </div>
        </div>
      </div>

      {/* Animation Showcase */}
      <div className="space-y-4">
        <h2 className="text-xl font-semibold">Animations</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="p-6 border rounded-lg bg-card">
            <h3 className="font-medium mb-4">Floating Logo</h3>
            <div className="flex justify-center">
              <Logo size="lg" />
            </div>
            <p className="text-sm text-muted-foreground mt-2 text-center">
              Gentle floating animation with glow effect
            </p>
          </div>
          
          <div className="p-6 border rounded-lg bg-card">
            <h3 className="font-medium mb-4">Chart Growth</h3>
            <div className="flex justify-center">
              <Logo size="lg" />
            </div>
            <p className="text-sm text-muted-foreground mt-2 text-center">
              Bars grow sequentially with trend line drawing
            </p>
          </div>
        </div>
      </div>

      {/* Color Variations */}
      <div className="space-y-4">
        <h2 className="text-xl font-semibold">Color Themes</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="p-4 border rounded-lg bg-blue-50 dark:bg-blue-950">
            <Logo size="md" className="text-blue-600" />
            <p className="text-sm text-muted-foreground mt-2 text-center">Blue Theme</p>
          </div>
          <div className="p-4 border rounded-lg bg-green-50 dark:bg-green-950">
            <Logo size="md" className="text-green-600" />
            <p className="text-sm text-muted-foreground mt-2 text-center">Green Theme</p>
          </div>
          <div className="p-4 border rounded-lg bg-purple-50 dark:bg-purple-950">
            <Logo size="md" className="text-purple-600" />
            <p className="text-sm text-muted-foreground mt-2 text-center">Purple Theme</p>
          </div>
        </div>
      </div>
    </div>
  );
};
