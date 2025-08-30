import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import io from 'socket.io-client';
import axios from 'axios';
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import ProfileList from './components/ProfileList';
import ChatInterface from './components/ChatInterface';
import ChatHistory from './components/ChatHistory';
import ServerConfig from './components/ServerConfig';
import { Brain, Database, MessageSquare, Users } from 'lucide-react';

const DEFAULT_BACKEND_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:5001';

function App() {
  const [backendUrl, setBackendUrl] = useState(DEFAULT_BACKEND_URL);
  const [socket, setSocket] = useState(null);
  const [connected, setConnected] = useState(false);
  const [userProfiles, setUserProfiles] = useState([]);
  const [selectedProfile, setSelectedProfile] = useState(null);
  const [chatSession, setChatSession] = useState(null);
  const [chatHistory, setChatHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [showChatHistory, setShowChatHistory] = useState(false);
  const [currentUserId, setCurrentUserId] = useState('user1');
  const [processingMessage, setProcessingMessage] = useState(false);

    // Initialize Socket.IO connection
  useEffect(() => {
    if (socket) {
      socket.disconnect();
    }
    
    console.log('🔌 Attempting Socket.IO connection to:', backendUrl);
    
    // Extract path from backendUrl for Socket.IO
    const url = new URL(backendUrl);
    const basePath = url.pathname === '/' ? '' : url.pathname;
    const socketPath = `${basePath}/socket.io/`;
    
    console.log('🔧 Socket.IO path:', socketPath);
    console.log('🔧 Socket.IO host:', `${url.protocol}//${url.host}`);
    
    const newSocket = io(`${url.protocol}//${url.host}`, {
      timeout: 10000,
      reconnection: true,
      reconnectionAttempts: 5,
      reconnectionDelay: 1000,
      transports: ['polling', 'websocket'], // Try polling first
      forceNew: true,
      upgrade: true,
      path: socketPath // Use extracted path including /kily-agent
    });
    
    console.log('🔧 Socket.IO instance created:', newSocket);
    
    newSocket.on('connect', () => {
      console.log('✅ Connected to backend:', backendUrl);
      setConnected(true);
    });

    newSocket.on('disconnect', (reason) => {
      console.log('❌ Disconnected from backend:', backendUrl, 'Reason:', reason);
      setConnected(false);
    });

    newSocket.on('connect_error', (error) => {
      console.error('🔴 Socket.IO connection error:', error);
      setConnected(false);
    });

    newSocket.on('chat_started', (data) => {
      console.log('Chat session started:', data);
      setChatSession(data);
    });

    newSocket.on('message_response', (data) => {
      console.log('Received message response:', data);
      setChatHistory(prev => [...prev, {
        type: 'assistant',
        content: data.response,
        timestamp: data.timestamp
      }]);
      setProcessingMessage(false);
    });

    newSocket.on('session_restored', (data) => {
      console.log('Session restored:', data);
      setChatSession({
        session_id: data.session_id,
        profile_id: data.profile_id,
        profile_name: data.profile_name
      });
      
      // Set the profile for display
      setSelectedProfile({
        profile_id: data.profile_id,
        profile_name: data.profile_name
      });
      
      // Set the chat history
      setChatHistory(data.chat_history || []);
      setLoading(false);
    });

    newSocket.on('error', (data) => {
      console.error('Socket error:', data);
      setError(data.message);
      setLoading(false);
      setProcessingMessage(false);
    });

    newSocket.on('voice_transcription', (data) => {
      console.log('Received voice transcription:', data);
      setChatHistory(prev => [
        ...prev,
        {
          type: 'user',
          content: data.transcribed_text,
          timestamp: data.timestamp,
          input_method: 'voice'
        }
      ]);
      // Keep processing message true until AI response is received
    });

    newSocket.on('voice_response', (data) => {
      console.log('Received voice response:', data);
      setChatHistory(prev => [
        ...prev,
        {
          type: 'assistant',
          content: data.response,
          timestamp: data.timestamp,
          voice_response: data.voice_response
        }
      ]);
      setProcessingMessage(false);
    });

    setSocket(newSocket);

    return () => {
      newSocket.close();
    };
  }, [backendUrl]);

  // Handle backend URL change
  const handleBackendUrlChange = (newUrl) => {
    setBackendUrl(newUrl || DEFAULT_BACKEND_URL);
    setConnected(false);
    setError(null);
  };

  // Test connection to backend (both HTTP and Socket.IO)
  const testConnection = async (url) => {
    const results = {
      http: null,
      socket: null
    };

    // Test HTTP connection
    try {
      const response = await axios.get(`${url}/health`, { 
        timeout: 5000,
        headers: {
          'Content-Type': 'application/json'
        }
      });
      
      if (response.status === 200) {
        results.http = { success: true, data: response.data };
      } else {
        results.http = { success: false, error: 'Health check failed' };
      }
    } catch (error) {
      results.http = { 
        success: false, 
        error: `Cannot connect to ${url}: ${error.message}` 
      };
    }

    // Test Socket.IO connection
    try {
      await new Promise((resolve, reject) => {
        console.log('🧪 Testing Socket.IO connection to:', url);
        
        // Extract path from url for Socket.IO test
        const testUrl = new URL(url);
        const testBasePath = testUrl.pathname === '/' ? '' : testUrl.pathname;
        const testSocketPath = `${testBasePath}/socket.io/`;
        
        console.log('🧪 Testing Socket.IO host:', `${testUrl.protocol}//${testUrl.host}`);
        console.log('🧪 Testing Socket.IO path:', testSocketPath);
        
        const testSocket = io(`${testUrl.protocol}//${testUrl.host}`, {
          timeout: 8000,
          reconnection: false, // Don't reconnect for test
          transports: ['polling', 'websocket'],
          forceNew: true,
          upgrade: true,
          path: testSocketPath
        });

        const timeoutId = setTimeout(() => {
          testSocket.disconnect();
          reject(new Error('Socket.IO connection timeout'));
        }, 8000);

        testSocket.on('connect', () => {
          console.log('✅ Socket.IO test connection successful');
          clearTimeout(timeoutId);
          testSocket.disconnect();
          results.socket = { success: true, message: 'Socket.IO connection successful' };
          resolve();
        });

        testSocket.on('connect_error', (error) => {
          console.error('❌ Socket.IO test connection failed:', error);
          clearTimeout(timeoutId);
          testSocket.disconnect();
          results.socket = { success: false, error: `Socket.IO connection failed: ${error.message}` };
          reject(error);
        });

        testSocket.on('disconnect', (reason) => {
          console.log('🔌 Socket.IO test disconnected:', reason);
        });
      });
    } catch (error) {
      if (!results.socket) {
        results.socket = { success: false, error: error.message };
      }
    }

    // Return results or throw error based on what succeeded
    if (results.http.success && results.socket.success) {
      return {
        message: 'Both HTTP and Socket.IO connections successful! ✅',
        details: results
      };
    } else if (results.http.success) {
      return {
        message: 'HTTP ✅ successful, but Socket.IO ❌ failed',
        details: results
      };
    } else {
      throw new Error(`Connection test failed - HTTP: ${results.http.error}, Socket.IO: ${results.socket?.error || 'Not tested'}`);
    }
  };

  // Load user profiles
  const loadProfiles = async (userId = 'user1') => {
    console.log('🔍 Load Profiles button clicked');
    console.log('📋 User ID:', userId);
    console.log('🌐 Backend URL:', backendUrl);
    console.log('🔗 Full API URL:', `${backendUrl}/api/users/${userId}/profiles`);
    
    setCurrentUserId(userId);
    setLoading(true);
    setError(null);
    
    try {
      console.log('📡 Making API request...');
      const response = await axios.get(`${backendUrl}/api/users/${userId}/profiles`);
      console.log('✅ API Response received:', response);
      console.log('📊 Profiles data:', response.data);
      setUserProfiles(response.data.profiles);
      console.log('💾 Profiles state updated:', response.data.profiles);
    } catch (err) {
      console.error('❌ Failed to load profiles:', err);
      console.error('❌ Error details:', {
        message: err.message,
        status: err.response?.status,
        statusText: err.response?.statusText,
        data: err.response?.data
      });
      setError('Failed to load profiles');
    } finally {
      setLoading(false);
      console.log('🏁 Load profiles operation completed');
    }
  };

  // Show chat history
  const handleShowChatHistory = (userId) => {
    setShowChatHistory(true);
    setSelectedProfile(null);
  };

  // Continue chat from history
  const handleContinueChat = (sessionId) => {
    setShowChatHistory(false);
    setLoading(true);
    setError(null);
    
    // Try to restore session from backend
    if (socket) {
      socket.emit('restore_session', {
        session_id: sessionId
      });
    } else {
      setError('Socket connection not available');
      setLoading(false);
    }
  };

  // Start chat session
  const startChat = (profile) => {
    setSelectedProfile(profile);
    setChatHistory([]);
    
    // Try to start chat with backend
    if (socket) {
      socket.emit('start_chat', {
        user_id: 'user1',
        profile_id: profile.profile_id
      });
    } else {
      setError('Socket connection not available - chat features disabled');
    }
  };

  // Send message
  const sendMessage = (message) => {
    if (!socket) {
      setError('Socket connection not available');
      return;
    }

    if (!chatSession) {
      setError('No active chat session');
      return;
    }

    // Set processing state
    setProcessingMessage(true);

    // Add user message to chat history
    setChatHistory(prev => [...prev, {
      type: 'user',
      content: message,
      timestamp: new Date().toISOString()
    }]);

    // Send message to backend
    socket.emit('send_message', {
      session_id: chatSession.session_id,
      message: message
    });
  };

  // Handle voice message
  const handleVoiceMessage = (voiceData) => {
    if (!socket) {
      setError('Socket connection not available');
      return;
    }

    if (!chatSession) {
      setError('No active chat session');
      return;
    }

    // Set processing state
    setProcessingMessage(true);

    // Send voice message to backend
    socket.emit('voice_message', {
      session_id: chatSession.session_id,
      audio_data: voiceData.audio_data,
      voice_id: voiceData.voice_id
    });
  };

  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <Header connected={connected} />
        
        {/* Server Configuration */}
        <div className="absolute top-4 right-4 z-10 flex items-center gap-2">
          <div className="text-xs text-gray-500 bg-white px-2 py-1 rounded border">
            {connected ? '🟢' : '🔴'} {backendUrl}
          </div>
          <ServerConfig
            backendUrl={backendUrl}
            onBackendUrlChange={handleBackendUrlChange}
            onTestConnection={testConnection}
          />
        </div>
        
        <div className="flex">
          {/* Sidebar */}
          <Sidebar 
            userProfiles={userProfiles}
            selectedProfile={selectedProfile}
            onLoadProfiles={loadProfiles}
            onSelectProfile={startChat}
            onShowChatHistory={handleShowChatHistory}
            loading={loading}
            error={error}
          />
          
          {/* Main Content */}
          <main className="flex-1 p-6">
            {showChatHistory ? (
              <ChatHistory
                userId={currentUserId}
                onSelectSession={handleContinueChat}
              />
            ) : selectedProfile ? (
              <ChatInterface
                profile={selectedProfile}
                chatHistory={chatHistory}
                onSendMessage={sendMessage}
                onVoiceMessage={handleVoiceMessage}
                session={chatSession}
                connected={connected}
                loading={loading}
                processingMessage={processingMessage}
                socket={socket}
              />
            ) : (
              <div className="text-center py-12">
                <div className="max-w-md mx-auto">
                  <Brain className="w-16 h-16 text-primary-500 mx-auto mb-4" />
                  <h2 className="text-2xl font-bold text-gray-900 mb-2">
                    Welcome to Enhanced QnA Agent
                  </h2>
                  <p className="text-gray-600">
                    Select a profile from the sidebar to start analyzing your data with AI-powered insights.
                  </p>
                </div>
              </div>
            )}
          </main>
        </div>
      </div>
    </Router>
  );
}

export default App;
