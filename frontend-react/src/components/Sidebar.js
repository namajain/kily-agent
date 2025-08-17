import React, { useState } from 'react';
import { FolderOpen, Loader, AlertCircle, ChevronDown, ChevronRight, MessageSquare } from 'lucide-react';
import ProfileList from './ProfileList';

const Sidebar = ({ 
  userProfiles, 
  selectedProfile, 
  onLoadProfiles, 
  onSelectProfile, 
  onShowChatHistory,
  loading, 
  error 
}) => {
  const [userId, setUserId] = useState('user1');
  const [showDataSources, setShowDataSources] = useState({});

  const handleLoadProfiles = () => {
    onLoadProfiles(userId);
  };

  const toggleDataSources = (profileId) => {
    setShowDataSources(prev => ({
      ...prev,
      [profileId]: !prev[profileId]
    }));
  };

  return (
    <aside className="w-80 bg-white shadow-lg border-r border-gray-200 h-screen overflow-y-auto">
      <div className="p-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">
          🔐 Authentication
        </h2>
        
        {/* User ID Input */}
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            User ID
          </label>
          <input
            type="text"
            value={userId}
            onChange={(e) => setUserId(e.target.value)}
            className="input-field"
            placeholder="Enter user ID"
          />
        </div>

        {/* Load Profiles Button */}
        <button
          onClick={handleLoadProfiles}
          disabled={loading}
          className="btn-primary w-full mb-4 flex items-center justify-center"
        >
          {loading ? (
            <>
              <Loader className="w-4 h-4 mr-2 animate-spin" />
              Loading...
            </>
          ) : (
            'Load Profiles'
          )}
        </button>

        {/* Error Display */}
        {error && (
          <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-md">
            <div className="flex items-center">
              <AlertCircle className="w-4 h-4 text-red-500 mr-2" />
              <span className="text-sm text-red-700">{error}</span>
            </div>
          </div>
        )}

        {/* Profiles Section */}
        {userProfiles.length > 0 && (
          <div className="mt-6">
            <h3 className="text-md font-semibold text-gray-900 mb-3 flex items-center">
              <FolderOpen className="w-4 h-4 mr-2" />
              Available Profiles ({userProfiles.length})
            </h3>
            
            <div className="space-y-3">
              {userProfiles.map((profile) => (
                <div key={profile.profile_id} className="card">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <h4 className="font-medium text-gray-900 mb-1">
                        {profile.profile_name}
                      </h4>
                      <p className="text-sm text-gray-500 mb-2">
                        ID: {profile.profile_id}
                      </p>
                      <p className="text-sm text-gray-500 mb-2">
                        Data Sources: {profile.data_sources?.length || 0}
                      </p>
                      <div className="flex items-center mb-3">
                        <span className="text-sm text-gray-500 mr-2">Status:</span>
                        <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${
                          profile.is_active 
                            ? 'bg-green-100 text-green-800' 
                            : 'bg-red-100 text-red-800'
                        }`}>
                          {profile.is_active ? '🟢 Active' : '🔴 Inactive'}
                        </span>
                      </div>
                    </div>
                  </div>

                  {/* Data Sources Expandable Section */}
                  {profile.data_sources && profile.data_sources.length > 0 && (
                    <div className="mt-3">
                      <button
                        onClick={() => toggleDataSources(profile.profile_id)}
                        className="flex items-center text-sm text-primary-600 hover:text-primary-700"
                      >
                        {showDataSources[profile.profile_id] ? (
                          <ChevronDown className="w-4 h-4 mr-1" />
                        ) : (
                          <ChevronRight className="w-4 h-4 mr-1" />
                        )}
                        📊 View {profile.data_sources.length} Data Sources
                      </button>
                      
                      {showDataSources[profile.profile_id] && (
                        <div className="mt-2 space-y-2">
                          {profile.data_sources.map((source, index) => (
                            <div key={index} className="p-2 bg-gray-50 rounded text-xs">
                              <div className="font-medium">{source.filename}</div>
                              <div className="text-gray-600">{source.description}</div>
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                  )}

                  {/* Select Profile Button */}
                  <button
                    onClick={() => onSelectProfile(profile)}
                    disabled={!profile.is_active}
                    className={`w-full mt-3 py-2 px-3 rounded-md text-sm font-medium transition-colors ${
                      profile.is_active
                        ? 'bg-primary-600 hover:bg-primary-700 text-white'
                        : 'bg-gray-200 text-gray-500 cursor-not-allowed'
                    }`}
                  >
                    Select {profile.profile_name}
                  </button>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Chat History Section */}
        {userProfiles.length > 0 && (
          <div className="mt-6 pt-6 border-t border-gray-200">
            <h3 className="text-md font-semibold text-gray-900 mb-3 flex items-center">
              <MessageSquare className="w-4 h-4 mr-2" />
              Chat History
            </h3>
            <button
              onClick={() => onShowChatHistory && onShowChatHistory(userId)}
              className="w-full py-2 px-3 rounded-md text-sm font-medium bg-gray-100 hover:bg-gray-200 text-gray-700 transition-colors flex items-center justify-center"
            >
              <MessageSquare className="w-4 h-4 mr-2" />
              View Chat History
            </button>
          </div>
        )}

        {/* Empty State */}
        {userProfiles.length === 0 && !loading && (
          <div className="text-center py-8 text-gray-500">
            <FolderOpen className="w-12 h-12 mx-auto mb-3 text-gray-300" />
            <p>No profiles loaded</p>
            <p className="text-sm">Click "Load Profiles" to get started</p>
          </div>
        )}
      </div>
    </aside>
  );
};

export default Sidebar;
