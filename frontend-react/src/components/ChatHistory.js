import React, { useState, useEffect } from 'react';
import { MessageSquare, Clock, User, Calendar } from 'lucide-react';

const ChatHistory = ({ userId, onSelectSession }) => {
  const [sessions, setSessions] = useState([]);
  const [selectedSession, setSelectedSession] = useState(null);
  const [sessionMessages, setSessionMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (userId) {
      loadUserSessions();
    }
  }, [userId]);

  const loadUserSessions = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(`http://localhost:5001/api/users/${userId}/sessions`);
      if (response.ok) {
        const data = await response.json();
        setSessions(data.sessions || []);
      } else {
        setError('Failed to load sessions');
      }
    } catch (err) {
      setError('Error loading sessions');
      console.error('Error loading sessions:', err);
    } finally {
      setLoading(false);
    }
  };

  const loadSessionMessages = async (sessionId) => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(`http://localhost:5001/api/sessions/${sessionId}/messages`);
      if (response.ok) {
        const data = await response.json();
        setSessionMessages(data.messages || []);
        setSelectedSession(sessionId);
      } else {
        setError('Failed to load session messages');
      }
    } catch (err) {
      setError('Error loading session messages');
      console.error('Error loading session messages:', err);
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  const getProfileName = (profileId) => {
    // Map profile IDs to names (you can make this dynamic)
    const profileNames = {
      'profile1': 'Sales Analytics',
      'profile2': 'Customer Analytics'
    };
    return profileNames[profileId] || profileId;
  };

  const getMessageCount = (session) => {
    // This would ideally come from the session data
    return session.message_count || 0;
  };

  if (loading && sessions.length === 0) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-4">
        <div className="bg-red-50 border border-red-200 rounded-md p-4">
          <p className="text-red-800">{error}</p>
          <button
            onClick={loadUserSessions}
            className="mt-2 text-sm text-red-600 hover:text-red-800 underline"
          >
            Try again
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="h-full flex flex-col">
      {/* Header */}
      <div className="border-b border-gray-200 p-4">
        <h2 className="text-lg font-semibold text-gray-900 flex items-center gap-2">
          <MessageSquare className="h-5 w-5" />
          Chat History
        </h2>
        <p className="text-sm text-gray-600 mt-1">
          View your previous chat sessions and conversations
        </p>
      </div>

      <div className="flex-1 flex overflow-hidden">
        {/* Sessions List */}
        <div className="w-1/3 border-r border-gray-200 overflow-y-auto">
          <div className="p-4">
            <h3 className="text-sm font-medium text-gray-700 mb-3">Recent Sessions</h3>
            {sessions.length === 0 ? (
              <div className="text-center py-8">
                <MessageSquare className="h-8 w-8 text-gray-400 mx-auto mb-2" />
                <p className="text-sm text-gray-500">No chat sessions found</p>
              </div>
            ) : (
              <div className="space-y-2">
                {sessions.map((session) => (
                  <div
                    key={session.session_id}
                    onClick={() => loadSessionMessages(session.session_id)}
                    className={`p-3 rounded-lg border cursor-pointer transition-colors ${
                      selectedSession === session.session_id
                        ? 'border-blue-500 bg-blue-50'
                        : 'border-gray-200 hover:border-gray-300 hover:bg-gray-50'
                    }`}
                  >
                    <div className="flex items-start justify-between">
                      <div className="flex-1 min-w-0">
                        <p className="text-sm font-medium text-gray-900 truncate">
                          {getProfileName(session.profile_id)}
                        </p>
                        <p className="text-xs text-gray-500 mt-1">
                          {formatDate(session.created_at)}
                        </p>
                        <div className="flex items-center gap-2 mt-1">
                          <span className="text-xs text-gray-400">
                            {getMessageCount(session)} messages
                          </span>
                          {session.is_active && (
                            <span className="inline-flex items-center px-1.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                              Active
                            </span>
                          )}
                        </div>
                      </div>
                      <Clock className="h-4 w-4 text-gray-400 flex-shrink-0" />
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Messages View */}
        <div className="flex-1 flex flex-col">
          {selectedSession ? (
            <>
              {/* Session Header */}
              <div className="border-b border-gray-200 p-4">
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="text-sm font-medium text-gray-900">
                      {getProfileName(sessions.find(s => s.session_id === selectedSession)?.profile_id)}
                    </h3>
                    <p className="text-xs text-gray-500">
                      Session started {formatDate(sessions.find(s => s.session_id === selectedSession)?.created_at)}
                    </p>
                  </div>
                  <button
                    onClick={() => onSelectSession && onSelectSession(selectedSession)}
                    className="text-sm text-blue-600 hover:text-blue-800 underline"
                  >
                    Continue Chat
                  </button>
                </div>
              </div>

              {/* Messages */}
              <div className="flex-1 overflow-y-auto p-4">
                {loading ? (
                  <div className="flex items-center justify-center h-32">
                    <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-500"></div>
                  </div>
                ) : sessionMessages.length === 0 ? (
                  <div className="text-center py-8">
                    <MessageSquare className="h-8 w-8 text-gray-400 mx-auto mb-2" />
                    <p className="text-sm text-gray-500">No messages in this session</p>
                  </div>
                ) : (
                  <div className="space-y-4">
                    {sessionMessages.map((message, index) => (
                      <div
                        key={index}
                        className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
                      >
                        <div
                          className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                            message.type === 'user'
                              ? 'bg-blue-500 text-white'
                              : 'bg-gray-100 text-gray-900'
                          }`}
                        >
                          <div className="flex items-start gap-2">
                            {message.type === 'assistant' && (
                              <User className="h-4 w-4 text-gray-500 flex-shrink-0 mt-0.5" />
                            )}
                            <div className="flex-1">
                              <p className="text-sm whitespace-pre-wrap">{message.content}</p>
                              <p className="text-xs opacity-70 mt-1">
                                {formatDate(message.timestamp)}
                              </p>
                            </div>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </>
          ) : (
            <div className="flex-1 flex items-center justify-center">
              <div className="text-center">
                <MessageSquare className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                <p className="text-gray-500">Select a session to view messages</p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ChatHistory;
