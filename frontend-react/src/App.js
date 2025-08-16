import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import io from 'socket.io-client';
import axios from 'axios';
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import ProfileList from './components/ProfileList';
import ChatInterface from './components/ChatInterface';
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
    });

    newSocket.on('error', (data) => {
      console.error('Socket error:', data);
      setError(data.message);
    });

    setSocket(newSocket);

    return () => {
      newSocket.close();
    };
  }, []);

  // Load user profiles
  const loadProfiles = async (userId = 'user1') => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await axios.get(`${BACKEND_URL}/api/users/${userId}/profiles`);
      setUserProfiles(response.data.profiles);
    } catch (err) {
      console.error('Failed to load profiles:', err);
      setError('Failed to load profiles');
    } finally {
      setLoading(false);
    }
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
            loading={loading}
            error={error}
          />
          
          {/* Main Content */}
          <main className="flex-1 p-6">
            {selectedProfile ? (
              <ChatInterface
                profile={selectedProfile}
                chatHistory={chatHistory}
                onSendMessage={sendMessage}
                session={chatSession}
                connected={connected}
              />
            ) : (
              <div className="text-center py-12">
                <div className="max-w-md mx-auto">
                  <Brain className="w-16 h-16 text-primary-500 mx-auto mb-4" />
                  <h2 className="text-2xl font-bold text-gray-900 mb-2">
                    Welcome to Enhanced QnA Agent
                  </h2>
                  <p className="text-gray-600 mb-6">
                    Select a profile from the sidebar to start analyzing your data with AI-powered insights.
                  </p>
                  
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-left">
                    <div className="card">
                      <Database className="w-8 h-8 text-primary-500 mb-2" />
                      <h3 className="font-semibold mb-1">Multiple Data Sources</h3>
                      <p className="text-sm text-gray-600">
                        Connect and analyze multiple datasets simultaneously
                      </p>
                    </div>
                    
                    <div className="card">
                      <MessageSquare className="w-8 h-8 text-primary-500 mb-2" />
                      <h3 className="font-semibold mb-1">AI-Powered Chat</h3>
                      <p className="text-sm text-gray-600">
                        Ask questions and get intelligent responses about your data
                      </p>
                    </div>
                    
                    <div className="card">
                      <Users className="w-8 h-8 text-primary-500 mb-2" />
                      <h3 className="font-semibold mb-1">Profile Management</h3>
                      <p className="text-sm text-gray-600">
                        Organize your data analysis into focused profiles
                      </p>
                    </div>
                  </div>
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
