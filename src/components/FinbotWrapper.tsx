import React, { useEffect, useState } from 'react';
import { Button } from '@/components/ui/button';
import { Bot } from 'lucide-react';

const FinbotWrapper: React.FC = () => {
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Check if finbot app is running
    fetch('http://localhost:5173')
      .then(() => {
        window.location.href = 'http://localhost:5173';
      })
      .catch(() => {
        setError('The Finance AI Assistant is not running. Please start it first.');
        setIsLoading(false);
      });
  }, []);

  if (error) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center p-4">
        <Bot className="h-12 w-12 text-gray-400 mb-4" />
        <h2 className="text-xl font-semibold mb-2">Finance AI Assistant</h2>
        <p className="text-gray-600 mb-4 text-center">{error}</p>
        <p className="text-sm text-gray-500 mb-4 text-center max-w-md">
          To start the assistant, run the following command in a new terminal:
          <code className="block bg-gray-100 p-2 rounded mt-2 font-mono text-sm">
            cd finbot-linguist-ai && npm run dev
          </code>
        </p>
        <Button
          onClick={() => window.location.reload()}
          className="bg-gradient-to-r from-blue-600 to-green-600 hover:from-blue-700 hover:to-green-700"
        >
          Retry Connection
        </Button>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="text-center">
        <div className="animate-spin h-8 w-8 border-4 border-blue-500 border-t-transparent rounded-full mx-auto mb-4"></div>
        <p className="text-gray-600">Connecting to Finance AI Assistant...</p>
      </div>
    </div>
  );
};

export default FinbotWrapper;
