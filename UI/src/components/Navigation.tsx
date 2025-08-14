import { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { BarChart3, MessageSquare, FileText, TrendingUp } from 'lucide-react';

const Navigation = () => {
  const [isScrolled, setIsScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 50);
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const navItems = [
    { label: 'Dashboard', href: '#dashboard', icon: BarChart3 },
    { label: 'Insights', href: '#insights', icon: TrendingUp },
    { label: 'Chat', href: '#chat', icon: MessageSquare },
    { label: 'Reports', href: '#reports', icon: FileText },
  ];

  const scrollToSection = (href: string) => {
    const element = document.querySelector(href);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  return (
    <nav className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
      isScrolled ? 'bg-background/95 backdrop-blur-md border-b border-border' : 'bg-transparent'
    }`}>
      <div className="container mx-auto px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <BarChart3 className="h-8 w-8 text-primary" />
            <span className="text-2xl font-bold bg-gradient-primary bg-clip-text text-transparent">
              DataLens
            </span>
          </div>
          
          <div className="hidden md:flex items-center space-x-1">
            {navItems.map((item) => {
              const Icon = item.icon;
              return (
                <Button
                  key={item.label}
                  variant="ghost"
                  onClick={() => scrollToSection(item.href)}
                  className="smooth-hover hover:text-primary hover:bg-primary/10"
                >
                  <Icon className="h-4 w-4 mr-2" />
                  {item.label}
                </Button>
              );
            })}
          </div>

          <Button variant="outline" className="hidden md:block border-primary text-primary hover:bg-primary hover:text-primary-foreground smooth-hover">
            Get Started
          </Button>
        </div>
      </div>
    </nav>
  );
};

export default Navigation;