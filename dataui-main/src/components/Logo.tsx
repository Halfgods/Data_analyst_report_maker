import React from 'react';

interface LogoProps {
  className?: string;
  size?: 'sm' | 'md' | 'lg';
}

export const Logo: React.FC<LogoProps> = ({ className = '', size = 'md' }) => {
  const sizeClasses = {
    sm: 'w-8 h-8',
    md: 'w-10 h-10',
    lg: 'w-12 h-12'
  };

  return (
    <div className={`flex items-center space-x-2 ${className}`}>
      {/* Logo Icon */}
      <div className={`${sizeClasses[size]} relative animate-logo-float`}>
        <svg
          viewBox="0 0 48 48"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
          className="w-full h-full animate-logo-glow"
        >
          {/* Magnifying Glass */}
          <circle
            cx="24"
            cy="24"
            r="20"
            stroke="currentColor"
            strokeWidth="3"
            fill="none"
            className="text-foreground"
          />
          {/* Magnifying Glass Handle */}
          <path
            d="M32 32L42 42"
            stroke="currentColor"
            strokeWidth="3"
            strokeLinecap="round"
            className="text-foreground"
          />
          
          {/* Bar Chart Inside Magnifying Glass */}
          <g className="text-primary">
            {/* Bar 1 */}
            <rect x="16" y="28" width="2" height="8" fill="currentColor" className="animate-chart-grow" style={{animationDelay: '0.1s'}} />
            {/* Bar 2 */}
            <rect x="19" y="26" width="2" height="10" fill="currentColor" className="animate-chart-grow" style={{animationDelay: '0.2s'}} />
            {/* Bar 3 */}
            <rect x="22" y="24" width="2" height="12" fill="currentColor" className="animate-chart-grow" style={{animationDelay: '0.3s'}} />
            {/* Bar 4 */}
            <rect x="25" y="20" width="2" height="16" fill="currentColor" className="animate-chart-grow" style={{animationDelay: '0.4s'}} />
            
            {/* Upward Trend Line */}
            <path
              d="M16 36 Q19 34 22 32 Q25 28 28 24"
              stroke="currentColor"
              strokeWidth="2"
              fill="none"
              strokeLinecap="round"
              className="text-blue-400 animate-trend-line"
              style={{animationDelay: '0.6s'}}
            />
            {/* Arrow */}
            <path
              d="M26 26L28 24L30 26"
              stroke="currentColor"
              strokeWidth="2"
              fill="none"
              strokeLinecap="round"
              strokeLinejoin="round"
              className="text-blue-400 animate-trend-line"
              style={{animationDelay: '0.8s'}}
            />
          </g>
        </svg>
      </div>
      
      {/* Logo Text */}
      <div className="hidden sm:block">
        <span className="font-bold text-lg text-foreground">DataViz</span>
        <span className="text-sm text-muted-foreground ml-1">Pro</span>
      </div>
    </div>
  );
};
