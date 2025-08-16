import React from 'react';

const ProfileList = ({ profiles, onSelectProfile }) => {
  return (
    <div className="space-y-3">
      {profiles.map((profile) => (
        <div key={profile.profile_id} className="card">
          <h4 className="font-medium text-gray-900 mb-2">
            {profile.profile_name}
          </h4>
          <p className="text-sm text-gray-500 mb-2">
            Data Sources: {profile.data_sources?.length || 0}
          </p>
          <button
            onClick={() => onSelectProfile(profile)}
            className="btn-primary w-full"
          >
            Select Profile
          </button>
        </div>
      ))}
    </div>
  );
};

export default ProfileList;
