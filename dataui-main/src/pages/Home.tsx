import React from 'react';
import { Link } from 'react-router-dom';
import { Header } from '@/components/Header';
import { Logo } from '@/components/Logo';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Upload, BarChart3, FileText, Zap, Shield, TrendingUp } from 'lucide-react';

const Home: React.FC = () => {
  return (
    <div className="min-h-screen bg-background">
      <Header />
      
      {/* Hero Section */}
      <section className="py-20 px-4">
        <div className="container mx-auto text-center">
          <div className="flex justify-center mb-8">
            <Logo size="lg" />
          </div>
          
          <h1 className="text-4xl md:text-6xl font-bold text-foreground mb-6">
            Transform Your Data with
            <span className="text-primary block">AI-Powered Insights</span>
          </h1>
          
          <p className="text-xl text-muted-foreground mb-8 max-w-3xl mx-auto">
            Upload your CSV files and get instant analysis, AI commentary, and beautiful visualizations. 
            Discover patterns you never knew existed.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link to="/upload">
              <Button size="lg" className="text-lg px-8 py-6">
                <Upload className="w-5 h-5 mr-2" />
                Start Analyzing
              </Button>
            </Link>
            
            <Button variant="outline" size="lg" className="text-lg px-8 py-6">
              <FileText className="w-5 h-5 mr-2" />
              View Demo
            </Button>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 px-4 bg-muted/20">
        <div className="container mx-auto">
          <h2 className="text-3xl font-bold text-center mb-16">Why Choose DataViz Pro?</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <Card className="text-center">
              <CardHeader>
                <div className="flex justify-center mb-4">
                  <div className="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center">
                    <Zap className="w-8 h-8 text-primary" />
                  </div>
                </div>
                <CardTitle>Lightning Fast</CardTitle>
                <CardDescription>
                  Get insights in seconds, not hours. Our optimized algorithms process data at incredible speeds.
                </CardDescription>
              </CardHeader>
            </Card>

            <Card className="text-center">
              <CardHeader>
                <div className="flex justify-center mb-4">
                  <div className="w-16 h-16 bg-secondary/10 rounded-full flex items-center justify-center">
                    <TrendingUp className="w-8 h-8 text-secondary" />
                  </div>
                </div>
                <CardTitle>AI-Powered</CardTitle>
                <CardDescription>
                  Advanced AI algorithms uncover hidden patterns and provide intelligent commentary on your data.
                </CardDescription>
              </CardHeader>
            </Card>

            <Card className="text-center">
              <CardHeader>
                <div className="flex justify-center mb-4">
                  <div className="w-16 h-16 bg-accent/10 rounded-full flex items-center justify-center">
                    <Shield className="w-8 h-8 text-accent" />
                  </div>
                </div>
                <CardTitle>Secure & Private</CardTitle>
                <CardDescription>
                  Your data never leaves your system. All processing happens locally for maximum security.
                </CardDescription>
              </CardHeader>
            </Card>
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="py-20 px-4">
        <div className="container mx-auto">
          <h2 className="text-3xl font-bold text-center mb-16">How It Works</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div className="text-center">
              <div className="w-16 h-16 bg-primary text-primary-foreground rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-4">
                1
              </div>
              <h3 className="text-xl font-semibold mb-2">Upload CSV</h3>
              <p className="text-muted-foreground">
                Simply drag and drop your CSV file or click to browse
              </p>
            </div>

            <div className="text-center">
              <div className="w-16 h-16 bg-secondary text-secondary-foreground rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-4">
                2
              </div>
              <h3 className="text-xl font-semibold mb-2">AI Analysis</h3>
              <p className="text-muted-foreground">
                Our AI processes your data and identifies key patterns
              </p>
            </div>

            <div className="text-center">
              <div className="w-16 h-16 bg-accent text-accent-foreground rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-4">
                3
              </div>
              <h3 className="text-xl font-semibold mb-2">Visualize</h3>
              <p className="text-muted-foreground">
                Beautiful charts and graphs bring your data to life
              </p>
            </div>

            <div className="text-center">
              <div className="w-16 h-16 bg-primary text-primary-foreground rounded-full flex items-center justify-center text-2xl font-bold mx-auto mb-4">
                4
              </div>
              <h3 className="text-xl font-semibold mb-2">Export</h3>
              <p className="text-muted-foreground">
                Download reports and share insights with your team
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4 bg-primary text-primary-foreground">
        <div className="container mx-auto text-center">
          <h2 className="text-3xl font-bold mb-6">Ready to Discover Your Data?</h2>
          <p className="text-xl mb-8 opacity-90">
            Join thousands of users who are already making better decisions with data-driven insights.
          </p>
          <Link to="/upload">
            <Button size="lg" variant="secondary" className="text-lg px-8 py-6">
              <Upload className="w-5 h-5 mr-2" />
              Get Started Now
            </Button>
          </Link>
        </div>
      </section>
    </div>
  );
};

export default Home;
