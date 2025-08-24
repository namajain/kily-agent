import React, { useState, useRef, useEffect } from 'react';
import { Send, MessageSquare, User, Bot, Loader, Volume2 } from 'lucide-react';
import VoiceInput from './VoiceInput';
import VoiceOutput from './VoiceOutput';
import MarkdownRenderer from './MarkdownRenderer';

const ChatInterface = ({ 
  profile, 
  chatHistory, 
  onSendMessage, 
  onVoiceMessage,
  session, 
  connected,
  loading = false,
  processingMessage = false,
  socket
}) => {
  const [message, setMessage] = useState('');
  const [availableVoices, setAvailableVoices] = useState([]);
  const [selectedVoice, setSelectedVoice] = useState(null);
  const [voiceEnabled, setVoiceEnabled] = useState(true);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [chatHistory]);

  useEffect(() => {
    // Get available voices when component mounts
    if (socket && connected) {
      socket.emit('get_available_voices');
      socket.on('available_voices', (data) => {
        setAvailableVoices(data.voices || []);
        if (data.voices && data.voices.length > 0) {
          setSelectedVoice(data.voices[0].voice_id);
        }
      });
    }
  }, [socket, connected]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!message.trim() || !connected || processingMessage) return;

    onSendMessage(message.trim());
    setMessage('');
  };

  const handleVoiceMessage = (audioData) => {
    if (!connected || processingMessage) return;
    
    onVoiceMessage({
      session_id: session?.session_id,
      audio_data: audioData,
      voice_id: selectedVoice
    });
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
          <div className="flex items-center space-x-4">
            {/* Voice Settings */}
            {voiceEnabled && availableVoices.length > 0 && (
              <div className="flex items-center space-x-2">
                <Volume2 className="w-4 h-4 text-gray-500" />
                <select
                  value={selectedVoice || ''}
                  onChange={(e) => setSelectedVoice(e.target.value)}
                  className="text-sm border border-gray-300 rounded px-2 py-1"
                  disabled={processingMessage}
                >
                  {availableVoices.map((voice) => (
                    <option key={voice.voice_id} value={voice.voice_id}>
                      {voice.name}
                    </option>
                  ))}
                </select>
              </div>
            )}
            
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
                     {msg.type === 'assistant' ? (
                       <MarkdownRenderer content={msg.content} />
                     ) : (
                       <p className="whitespace-pre-wrap">{msg.content}</p>
                     )}
                     
                     {/* Voice Output for Assistant Messages */}
                     {msg.type === 'assistant' && voiceEnabled && msg.voice_response && (
                       <div className="mt-2">
                         <VoiceOutput
                           audioData={msg.voice_response.audio_data}
                           text="Listen to response"
                         />
                       </div>
                     )}
                     
                                         {/* Voice Input Indicator for User Messages */}
                    {msg.type === 'user' && msg.input_method === 'voice' && (
                      <div className="mt-2 pt-2 border-t border-primary-500 border-opacity-30">
                        <span className="text-xs opacity-75 flex items-center gap-1">
                          🎤 <span className="italic">Transcribed from voice</span>
                        </span>
                      </div>
                    )}
                     
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
                 <form onSubmit={handleSubmit} className="flex items-center space-x-3">
           <div className="flex-1">
             <input
               type="text"
               value={message}
               onChange={(e) => setMessage(e.target.value)}
               placeholder="Type your message..."
               disabled={!connected || processingMessage}
               className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:bg-gray-100 disabled:cursor-not-allowed"
             />
           </div>
           
           {/* Voice Input Button */}
           {voiceEnabled && (
             <VoiceInput
               onVoiceMessage={handleVoiceMessage}
               disabled={!connected || processingMessage}
               processing={processingMessage}
             />
           )}
           
           <button
             type="submit"
             disabled={!message.trim() || !connected || processingMessage}
             className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
           >
             <Send className="w-4 h-4" />
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
