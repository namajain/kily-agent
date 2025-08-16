import React from 'react';
import { Brain, Wifi, WifiOff } from 'lucide-react';

const Header = ({ connected }) => {
  return (
    <header className="bg-white shadow-sm border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center">
            <Brain className="w-8 h-8 text-primary-600 mr-3" />
            <h1 className="text-xl font-bold text-gray-900">
              Enhanced QnA Agent
            </h1>
            <span className="ml-3 text-sm text-gray-500">
              MVP Version
            </span>
          </div>
          
          <div className="flex items-center space-x-4">
            <div className="flex items-center">
              {connected ? (
                <>
                  <Wifi className="w-4 h-4 text-green-500 mr-2" />
                  <span className="text-sm text-green-600">Connected</span>
                </>
              ) : (
                <>
                  <WifiOff className="w-4 h-4 text-red-500 mr-2" />
                  <span className="text-sm text-red-600">Disconnected</span>
                </>
              )}
            </div>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
