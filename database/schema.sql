-- Enhanced QnA Agent System - MVP Database Schema
-- PostgreSQL schema for v1 implementation

-- Users table
CREATE TABLE users (
    user_id VARCHAR(255) PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    email VARCHAR(255) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User profiles table
CREATE TABLE user_profiles (
    profile_id VARCHAR(255) PRIMARY KEY,
    user_id VARCHAR(255) REFERENCES users(user_id) ON DELETE CASCADE,
    profile_name VARCHAR(255) NOT NULL,
    data_sources JSONB, -- Configuration for data sources
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Chat history table
CREATE TABLE chat_history (
    chat_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id VARCHAR(255) REFERENCES users(user_id) ON DELETE CASCADE,
    profile_id VARCHAR(255) REFERENCES user_profiles(profile_id) ON DELETE CASCADE,
    title VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Chat messages table
CREATE TABLE chat_messages (
    message_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    chat_id UUID REFERENCES chat_history(chat_id) ON DELETE CASCADE,
    message_type VARCHAR(50) NOT NULL CHECK (message_type IN ('user', 'assistant')),
    content TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Context files tracking table
CREATE TABLE context_files (
    file_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    profile_id VARCHAR(255) REFERENCES user_profiles(profile_id) ON DELETE CASCADE,
    file_path VARCHAR(500) NOT NULL,
    download_date DATE NOT NULL,
    file_size BIGINT,
    download_status VARCHAR(50) DEFAULT 'pending' CHECK (download_status IN ('pending', 'success', 'failed')),
    last_download_attempt TIMESTAMP,
    error_message TEXT,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_user_profiles_user_id ON user_profiles(user_id);
CREATE INDEX idx_user_profiles_active ON user_profiles(is_active);
CREATE INDEX idx_chat_history_user_id ON chat_history(user_id);
CREATE INDEX idx_chat_history_profile_id ON chat_history(profile_id);
CREATE INDEX idx_chat_messages_chat_id ON chat_messages(chat_id);
CREATE INDEX idx_chat_messages_timestamp ON chat_messages(timestamp);
CREATE INDEX idx_context_files_profile_date ON context_files(profile_id, download_date);
CREATE INDEX idx_context_files_status ON context_files(download_status);

-- Sample data for testing
INSERT INTO users (user_id, username, email) VALUES
('user1', 'testuser1', 'user1@example.com'),
('user2', 'testuser2', 'user2@example.com');

INSERT INTO user_profiles (profile_id, user_id, profile_name, data_sources) VALUES
('profile1', 'user1', 'Sales Data', '[
    {
        "url": "https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv",
        "filename": "covid_data.csv",
        "description": "COVID-19 aggregated data by country"
    },
    {
        "url": "https://raw.githubusercontent.com/datasets/iris/master/data/iris.csv",
        "filename": "iris_data.csv", 
        "description": "Iris flower dataset"
    }
]'),
('profile2', 'user1', 'Employee Data', '[
    {
        "url": "https://raw.githubusercontent.com/datasets/employees/master/data/employees.csv",
        "filename": "employees.csv",
        "description": "Employee salary and performance data"
    }
]'),
('profile3', 'user2', 'Financial Data', '[
    {
        "url": "https://raw.githubusercontent.com/datasets/stocks/master/data/stock_prices.csv",
        "filename": "stock_prices.csv",
        "description": "Historical stock price data"
    }
]'); 