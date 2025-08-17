import React, { useState, useRef, useEffect } from 'react';
import { Send, MessageSquare, User, Bot, Loader } from 'lucide-react';

const ChatInterface = ({ 
  profile, 
  chatHistory, 
  onSendMessage, 
  session, 
  connected,
  loading = false,
  processingMessage = false
}) => {
  const [message, setMessage] = useState('');
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [chatHistory]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!message.trim() || !connected || processingMessage) return;

    onSendMessage(message.trim());
    setMessage('');
  };

  const formatTime = (timestamp) => {
    return new Date(timestamp).toLocaleTimeString();
  };

  const exampleQueries = [
    "Which is the highest performing keyword?",
    "Which is the highest performing keyword this week?",
    "Which is the highest performing keyword this month?",
    "Which is the highest performing keyword by ROAS?"
  ];

  return (
    <div className="h-full flex flex-col">
      {/* Chat Header */}
      <div className="bg-white border-b border-gray-200 p-4">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-xl font-semibold text-gray-900">
              💬 Chat Interface
            </h2>
            <p className="text-sm text-gray-600">
              {profile.profile_name} • {profile.data_sources?.length || 0} data sources
            </p>
          </div>
          <div className="flex items-center space-x-2">
            <div className={`w-2 h-2 rounded-full ${
              connected ? 'bg-green-500' : 'bg-red-500'
            }`} />
            <span className="text-sm text-gray-500">
              {connected ? 'Connected' : 'Disconnected'}
            </span>
          </div>
        </div>
      </div>

      {/* Chat Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {loading ? (
          <div className="flex items-center justify-center h-64">
            <div className="text-center">
              <Loader className="w-8 h-8 animate-spin text-blue-500 mx-auto mb-4" />
              <p className="text-gray-600">Restoring chat session...</p>
            </div>
          </div>
        ) : chatHistory.length === 0 ? (
          <div className="text-center py-8">
            <MessageSquare className="w-12 h-12 text-gray-300 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              Start a conversation
            </h3>
            <p className="text-gray-600 mb-6">
              Ask questions about your data to get AI-powered insights
            </p>
            
            {/* Example Queries */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3 max-w-2xl mx-auto">
              {exampleQueries.map((query, index) => (
                <button
                  key={index}
                  onClick={() => setMessage(query)}
                  disabled={processingMessage}
                  className={`p-3 text-left rounded-lg border transition-colors ${
                    processingMessage 
                      ? 'bg-gray-100 text-gray-400 cursor-not-allowed' 
                      : 'bg-gray-50 hover:bg-gray-100 border-gray-200 text-gray-700'
                  }`}
                >
                  <span className="text-sm">{query}</span>
                </button>
              ))}
            </div>
          </div>
        ) : (
          chatHistory.map((msg, index) => (
            <div
              key={index}
              className={`flex ${msg.type === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div className={`max-w-3xl flex ${msg.type === 'user' ? 'flex-row-reverse' : 'flex-row'}`}>
                <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
                  msg.type === 'user' 
                    ? 'bg-primary-600 text-white ml-3' 
                    : 'bg-gray-200 text-gray-600 mr-3'
                }`}>
                  {msg.type === 'user' ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
                </div>
                <div className={`flex-1 ${msg.type === 'user' ? 'text-right' : 'text-left'}`}>
                  <div className={`inline-block p-4 rounded-lg ${
                    msg.type === 'user'
                      ? 'bg-primary-600 text-white'
                      : 'bg-white border border-gray-200 text-gray-900'
                  }`}>
                    <p className="whitespace-pre-wrap">{msg.content}</p>
                    <p className={`text-xs mt-2 ${
                      msg.type === 'user' ? 'text-primary-100' : 'text-gray-500'
                    }`}>
                      {formatTime(msg.timestamp)}
                    </p>
                  </div>
                </div>
              </div>
            </div>
          ))
        )}

        {/* Processing Indicator */}
        {processingMessage && (
          <div className="flex justify-start">
            <div className="flex items-center space-x-2 bg-white border border-gray-200 rounded-lg p-3">
              <Bot className="w-4 h-4 text-gray-600" />
              <div className="flex items-center space-x-2">
                <Loader className="w-4 h-4 animate-spin text-blue-500" />
                <span className="text-sm text-gray-600">Processing your message...</span>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Message Input */}
      <div className="bg-white border-t border-gray-200 p-4">
        <form onSubmit={handleSubmit} className="flex space-x-3">
          <input
            type="text"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder={processingMessage ? "Processing..." : "Ask a question about your data..."}
            disabled={!connected || processingMessage}
            className="flex-1 input-field"
          />
          <button
            type="submit"
            disabled={!message.trim() || !connected || processingMessage}
            className="btn-primary flex items-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {processingMessage ? (
              <>
                <Loader className="w-4 h-4 animate-spin" />
                <span>Processing...</span>
              </>
            ) : (
              <>
                <Send className="w-4 h-4" />
                <span>Send</span>
              </>
            )}
          </button>
        </form>
        
        {!connected && (
          <p className="text-sm text-red-600 mt-2">
            Not connected to backend. Please check your connection.
          </p>
        )}
      </div>
    </div>
  );
};

export default ChatInterface;
