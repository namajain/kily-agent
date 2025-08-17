import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import io from 'socket.io-client';
import axios from 'axios';
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import ProfileList from './components/ProfileList';
import ChatInterface from './components/ChatInterface';
import ChatHistory from './components/ChatHistory';
import { Brain, Database, MessageSquare, Users } from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:5001';

function App() {
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
    const newSocket = io(BACKEND_URL);
    
    newSocket.on('connect', () => {
      console.log('Connected to backend');
      setConnected(true);
    });

    newSocket.on('disconnect', () => {
      console.log('Disconnected from backend');
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

    setSocket(newSocket);

    return () => {
      newSocket.close();
    };
  }, []);

  // Load user profiles
  const loadProfiles = async (userId = 'user1') => {
    console.log('🔍 Load Profiles button clicked');
    console.log('📋 User ID:', userId);
    console.log('🌐 Backend URL:', BACKEND_URL);
    console.log('🔗 Full API URL:', `${BACKEND_URL}/api/users/${userId}/profiles`);
    
    setCurrentUserId(userId);
    setLoading(true);
    setError(null);
    
    try {
      console.log('📡 Making API request...');
      const response = await axios.get(`${BACKEND_URL}/api/users/${userId}/profiles`);
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
    if (!socket || !connected) {
      setError('Not connected to backend');
      return;
    }

    setShowChatHistory(false);
    setLoading(true);
    setError(null);
    
    // Restore session from backend
    socket.emit('restore_session', {
      session_id: sessionId
    });
  };

  // Start chat session
  const startChat = (profile) => {
    if (!socket || !connected) {
      setError('Not connected to backend');
      return;
    }

    setSelectedProfile(profile);
    setChatHistory([]);
    
    socket.emit('start_chat', {
      user_id: 'user1',
      profile_id: profile.profile_id
    });
  };

  // Send message
  const sendMessage = (message) => {
    if (!socket || !connected || !chatSession) {
      setError('Not connected or no active session');
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

  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <Header connected={connected} />
        
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
                session={chatSession}
                connected={connected}
                loading={loading}
                processingMessage={processingMessage}
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
