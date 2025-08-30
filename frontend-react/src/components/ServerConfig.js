import React, { useState } from 'react';
import { Settings, Save, RotateCcw } from 'lucide-react';

const ServerConfig = ({ backendUrl, onBackendUrlChange, onTestConnection }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [tempUrl, setTempUrl] = useState(backendUrl);
  const [isTesting, setIsTesting] = useState(false);
  const [testResult, setTestResult] = useState(null);

  const handleSave = () => {
    onBackendUrlChange(tempUrl);
    setIsOpen(false);
    setTestResult(null);
  };

  const handleReset = () => {
    setTempUrl(backendUrl);
    setTestResult(null);
  };

  const handleTest = async () => {
    setIsTesting(true);
    setTestResult(null);
    
    try {
      await onTestConnection(tempUrl);
      setTestResult({ success: true, message: 'Connection successful!' });
    } catch (error) {
      setTestResult({ success: false, message: `Connection failed: ${error.message}` });
    } finally {
      setIsTesting(false);
    }
  };

  return (
    <div className="server-config">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-2 px-3 py-2 text-sm bg-gray-100 hover:bg-gray-200 rounded-md transition-colors"
        title="Server Configuration"
      >
        <Settings size={16} />
        Server Config
      </button>

      {isOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-96 max-w-[90vw]">
            <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
              <Settings size={20} />
              Server Configuration
            </h3>
            
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Backend Server URL
                </label>
                <input
                  type="url"
                  value={tempUrl}
                  onChange={(e) => setTempUrl(e.target.value)}
                  placeholder="http://localhost:5001"
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                <p className="text-xs text-gray-500 mt-1">
                  Override the default backend URL. Leave empty to use environment default.
                </p>
              </div>

              {testResult && (
                <div className={`p-3 rounded-md text-sm ${
                  testResult.success 
                    ? 'bg-green-100 text-green-800 border border-green-200' 
                    : 'bg-red-100 text-red-800 border border-red-200'
                }`}>
                  {testResult.message}
                </div>
              )}

              <div className="flex gap-2">
                <button
                  onClick={handleTest}
                  disabled={isTesting}
                  className="flex-1 flex items-center justify-center gap-2 px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {isTesting ? 'Testing...' : 'Test Connection'}
                </button>
                
                <button
                  onClick={handleReset}
                  className="px-4 py-2 bg-gray-500 text-white rounded-md hover:bg-gray-600 flex items-center gap-2"
                  title="Reset to current value"
                >
                  <RotateCcw size={16} />
                </button>
              </div>

              <div className="flex gap-2 pt-4 border-t">
                <button
                  onClick={handleSave}
                  className="flex-1 flex items-center justify-center gap-2 px-4 py-2 bg-green-500 text-white rounded-md hover:bg-green-600"
                >
                  <Save size={16} />
                  Save & Apply
                </button>
                
                <button
                  onClick={() => setIsOpen(false)}
                  className="flex-1 px-4 py-2 bg-gray-300 text-gray-700 rounded-md hover:bg-gray-400"
                >
                  Cancel
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ServerConfig;
