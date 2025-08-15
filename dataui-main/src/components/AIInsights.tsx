import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from '@/components/ui/collapsible';
import { Brain, ChevronDown, ChevronUp, Send, Sparkles } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

interface AIInsightsProps {
  insights: string[];
  onAskQuestion?: (question: string) => void;
  isLoading?: boolean;
  aiResponse?: string;
}

export const AIInsights: React.FC<AIInsightsProps> = ({ 
  insights, 
  onAskQuestion, 
  isLoading = false,
  aiResponse = ''
}) => {
  const [isOpen, setIsOpen] = useState(true);
  const [question, setQuestion] = useState('');

  const handleAskQuestion = () => {
    if (question.trim() && onAskQuestion) {
      onAskQuestion(question);
      setQuestion('');
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleAskQuestion();
    }
  };

  return (
    <div className="space-y-6">
      {/* AI Insights */}
      <Card className="card-elevated">
        <Collapsible open={isOpen} onOpenChange={setIsOpen}>
          <CollapsibleTrigger asChild>
            <CardHeader className="cursor-pointer hover:bg-surface/50 rounded-t-lg transition-colors">
              <CardTitle className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <Brain className="w-5 h-5 text-primary" />
                  AI Insights
                  <Sparkles className="w-4 h-4 text-accent" />
                </div>
                {isOpen ? (
                  <ChevronUp className="w-5 h-5 text-muted-foreground" />
                ) : (
                  <ChevronDown className="w-5 h-5 text-muted-foreground" />
                )}
              </CardTitle>
            </CardHeader>
          </CollapsibleTrigger>
          <CollapsibleContent>
            <CardContent className="space-y-4">
              {insights.length > 0 ? (
                insights.map((insight, index) => (
                  <div 
                    key={index} 
                    className="p-4 bg-gradient-surface rounded-lg border border-border/50"
                  >
                    <ReactMarkdown 
                      remarkPlugins={[remarkGfm]}
                      components={{
                        h1: ({children}) => <h1 className="text-lg font-bold mb-2">{children}</h1>,
                        h2: ({children}) => <h2 className="text-base font-semibold mb-2">{children}</h2>,
                        h3: ({children}) => <h3 className="text-sm font-semibold mb-1">{children}</h3>,
                        p: ({children}) => <p className="text-sm leading-relaxed mb-2">{children}</p>,
                        strong: ({children}) => <strong className="font-semibold">{children}</strong>,
                        em: ({children}) => <em className="italic">{children}</em>,
                        code: ({children}) => <code className="bg-muted px-1 py-0.5 rounded text-xs">{children}</code>,
                        pre: ({children}) => <pre className="bg-muted p-2 rounded text-xs overflow-x-auto">{children}</pre>,
                      }}
                    >
                      {insight}
                    </ReactMarkdown>
                  </div>
                ))
              ) : (
                <div className="text-center py-8">
                  <Brain className="w-12 h-12 mx-auto mb-3 text-muted-foreground" />
                  <p className="text-muted-foreground">AI insights will appear here after analysis</p>
                </div>
              )}
            </CardContent>
          </CollapsibleContent>
        </Collapsible>
      </Card>

      {/* Ask AI */}
      <Card className="card-elevated">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Send className="w-5 h-5 text-secondary" />
            Ask AI About Your Data
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex gap-2">
            <Input
              placeholder="Ask a question about your data..."
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              onKeyPress={handleKeyPress}
              disabled={isLoading}
              className="flex-1"
            />
            <Button 
              onClick={handleAskQuestion}
              disabled={!question.trim() || isLoading}
              className="bg-gradient-secondary hover:bg-secondary-hover"
            >
              {isLoading ? (
                <div className="w-4 h-4 border-2 border-current border-t-transparent animate-spin rounded-full" />
              ) : (
                <Send className="w-4 h-4" />
              )}
            </Button>
          </div>
          
          <div className="mt-4 text-xs text-muted-foreground">
            <p>Try asking:</p>
            <ul className="list-disc list-inside mt-1 space-y-1">
              <li>"What are the main patterns in this data?"</li>
              <li>"Which columns have the most missing values?"</li>
              <li>"What correlations do you see?"</li>
            </ul>
          </div>
          
          {/* AI Response Display */}
          {aiResponse && (
            <div className="mt-6 p-4 bg-gradient-surface rounded-lg border border-border/50">
              <h4 className="font-semibold text-sm mb-2 text-primary">AI Response:</h4>
              <ReactMarkdown 
                remarkPlugins={[remarkGfm]}
                components={{
                  h1: ({children}) => <h1 className="text-lg font-bold mb-2">{children}</h1>,
                  h2: ({children}) => <h2 className="text-base font-semibold mb-2">{children}</h2>,
                  h3: ({children}) => <h3 className="text-sm font-semibold mb-1">{children}</h3>,
                  p: ({children}) => <p className="text-sm leading-relaxed mb-2">{children}</p>,
                  strong: ({children}) => <strong className="font-semibold">{children}</strong>,
                  em: ({children}) => <em className="italic">{children}</em>,
                  code: ({children}) => <code className="bg-muted px-1 py-0.5 rounded text-xs">{children}</code>,
                  pre: ({children}) => <pre className="bg-muted p-2 rounded text-xs overflow-x-auto">{children}</pre>,
                }}
              >
                {aiResponse}
              </ReactMarkdown>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
};