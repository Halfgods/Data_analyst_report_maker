import { useState, useEffect } from 'react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { MessageSquare, Send, Bot, User, TrendingUp, BarChart3, FileText } from 'lucide-react';

interface ChatSectionProps {
  currentSessionId?: string | null;
}

const ChatSection = ({ currentSessionId }: ChatSectionProps = {}) => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'bot',
      content: currentSessionId ? 
        "Hello! I'm ready to analyze your uploaded data. Ask me anything about your CSV data and I'll provide insights based on the analysis." :
        "Hello! I'm your AI analytics assistant. Please upload a CSV file first so I can help you understand your data, explain trends, and provide insights.",
      timestamp: new Date()
    }
  ]);
  
  const [inputValue, setInputValue] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const API_BASE_URL = ''; // Matches index.html exactly

  const quickQuestions = [
    { text: "Explain the revenue trend", icon: TrendingUp },
    { text: "Compare device performance", icon: BarChart3 },
    { text: "Generate summary report", icon: FileText }
  ];

  const handleSendMessage = async () => {
    if (!inputValue.trim()) return;
    
    // Check if we have a session ID for data queries
    if (!currentSessionId) {
      const errorMessage = {
        id: Date.now() + 1,
        type: 'bot' as const,
        content: "Please upload a CSV file first so I can analyze your data and answer questions about it.",
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
      return;
    }

    const userMessage = {
      id: Date.now(),
      type: 'user' as const,
      content: inputValue,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    const question = inputValue;
    setInputValue('');
    setIsTyping(true);

    try {
      // Real API call to backend (exact logic from index.html)
      const response = await fetch(`${API_BASE_URL}/query-data/${currentSessionId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ question: question })
      });
      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || 'Failed to get AI answer.');
      }

      const botResponse = {
        id: Date.now() + 1,
        type: 'bot' as const,
        content: data.answer || data.error || 'No answer received.',
        timestamp: new Date()
      };
      
      setMessages(prev => [...prev, botResponse]);
    } catch (error) {
      const errorMessage = {
        id: Date.now() + 1,
        type: 'bot' as const,
        content: `Error: ${error instanceof Error ? error.message : 'Unknown error occurred'}`,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsTyping(false);
    }
  };

  const handleQuickQuestion = (question: string) => {
    setInputValue(question);
  };

  const formatTime = (date: Date) => {
    return new Intl.DateTimeFormat('en-US', {
      hour: '2-digit',
      minute: '2-digit'
    }).format(date);
  };

  return (
    <section id="chat" className="py-20 bg-gradient-to-b from-background to-muted/20">
      <div className="container mx-auto px-6">
        <div className="text-center mb-16">
          <h2 className="text-4xl md:text-5xl font-bold mb-6">
            AI Analytics Assistant
          </h2>
          <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
            Ask questions about your data in natural language and get instant, actionable insights
          </p>
        </div>

        <div className="max-w-4xl mx-auto">
          <Card className="analytics-card">
            {/* Chat Header */}
            <div className="border-b border-border p-6">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 bg-primary/10 rounded-full flex items-center justify-center">
                  <Bot className="h-6 w-6 text-primary" />
                </div>
                <div>
                  <h3 className="font-semibold">DataLens AI Assistant</h3>
                  <p className="text-sm text-muted-foreground">Always ready to help with your analytics</p>
                </div>
                <div className="ml-auto">
                  <div className="flex items-center gap-2">
                    <div className="w-2 h-2 bg-analytics-success rounded-full"></div>
                    <span className="text-sm text-muted-foreground">Online</span>
                  </div>
                </div>
              </div>
            </div>

            {/* Messages Area */}
            <div className="h-96 overflow-y-auto p-6 space-y-4">
              {messages.map((message) => (
                <div key={message.id} className={`flex gap-3 ${message.type === 'user' ? 'justify-end' : ''}`}>
                  {message.type === 'bot' && (
                    <div className="w-8 h-8 bg-primary/10 rounded-full flex items-center justify-center flex-shrink-0">
                      <Bot className="h-4 w-4 text-primary" />
                    </div>
                  )}
                  
                  <div className={`max-w-[80%] ${message.type === 'user' ? 'order-first' : ''}`}>
                    <div className={`p-4 rounded-lg ${
                      message.type === 'user' 
                        ? 'bg-primary text-primary-foreground ml-auto' 
                        : 'bg-muted'
                    }`}>
                      <p className="whitespace-pre-line leading-relaxed">{message.content}</p>
                    </div>
                    <p className="text-xs text-muted-foreground mt-1 px-1">
                      {formatTime(message.timestamp)}
                    </p>
                  </div>

                  {message.type === 'user' && (
                    <div className="w-8 h-8 bg-secondary/10 rounded-full flex items-center justify-center flex-shrink-0">
                      <User className="h-4 w-4 text-secondary" />
                    </div>
                  )}
                </div>
              ))}

              {isTyping && (
                <div className="flex gap-3">
                  <div className="w-8 h-8 bg-primary/10 rounded-full flex items-center justify-center flex-shrink-0">
                    <Bot className="h-4 w-4 text-primary" />
                  </div>
                  <div className="max-w-[80%]">
                    <div className="p-4 rounded-lg bg-muted">
                      <div className="flex gap-1">
                        <div className="w-2 h-2 bg-muted-foreground rounded-full animate-pulse"></div>
                        <div className="w-2 h-2 bg-muted-foreground rounded-full animate-pulse" style={{ animationDelay: '0.2s' }}></div>
                        <div className="w-2 h-2 bg-muted-foreground rounded-full animate-pulse" style={{ animationDelay: '0.4s' }}></div>
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </div>

            {/* Quick Questions */}
            <div className="px-6 py-4 border-t border-border">
              <p className="text-sm text-muted-foreground mb-3">Quick questions:</p>
              <div className="flex flex-wrap gap-2">
                {quickQuestions.map((question, index) => {
                  const Icon = question.icon;
                  return (
                    <Button
                      key={index}
                      variant="outline"
                      size="sm"
                      onClick={() => handleQuickQuestion(question.text)}
                      className="text-xs smooth-hover hover:bg-primary/10 hover:border-primary/20"
                    >
                      <Icon className="h-3 w-3 mr-1" />
                      {question.text}
                    </Button>
                  );
                })}
              </div>
            </div>

            {/* Input Area */}
            <div className="p-6 border-t border-border">
              <div className="flex gap-3">
                <Input
                  placeholder="Ask me anything about your analytics data..."
                  value={inputValue}
                  onChange={(e) => setInputValue(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                  className="flex-1 border-border focus:border-primary smooth-hover"
                />
                <Button 
                  onClick={handleSendMessage}
                  disabled={!inputValue.trim() || isTyping}
                  className="bg-primary hover:bg-primary/90 text-primary-foreground smooth-hover"
                >
                  <Send className="h-4 w-4" />
                </Button>
              </div>
              <p className="text-xs text-muted-foreground mt-2">
                AI responses are generated based on your current analytics data and industry best practices.
              </p>
            </div>
          </Card>
        </div>
      </div>
    </section>
  );
};

export default ChatSection;