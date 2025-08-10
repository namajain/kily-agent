# Enhanced QnA Agent System - MVP

## Overview

This is the MVP (Minimum Viable Product) implementation of the Enhanced QnA Agent System. It provides a real-time, profile-based data analysis platform with natural language query processing.

## Features

### ✅ MVP Features
- **Profile-based Context Management**: On-demand file downloads for specific profiles
- **Session Management**: 15-minute timeout sessions with profile context
- **Real-time Communication**: Socket.IO backend with Streamlit frontend
- **Natural Language Analysis**: LLM-powered query processing
- **Database Integration**: PostgreSQL for persistent storage
- **File Organization**: Date-based file structure (`downloads/YYYY-MM-DD/profile_id/`)

### 🔄 Workflow
1. User selects a profile from the frontend
2. Backend creates session and downloads context files (if needed)
3. User asks questions in natural language
4. QnA agent analyzes data using profile context
5. Results are streamed back in real-time

## Architecture

```
┌─────────────────┐    WebSocket    ┌─────────────────┐
│   Streamlit     │ ◄─────────────► │   Socket.IO     │
│   Frontend      │                 │   Backend       │
└─────────────────┘                 └─────────────────┘
                                              │
                                              ▼
                                    ┌─────────────────┐
                                    │   PostgreSQL    │
                                    │   Database      │
                                    └─────────────────┘
                                              │
                                              ▼
                                    ┌─────────────────┐
                                    │   File System   │
                                    │  (Downloads)    │
                                    └─────────────────┘
```

## Quick Start

### Prerequisites
- Python 3.9+
- PostgreSQL 13+
- OpenAI API key

### 1. Setup Environment

```bash
# Clone and navigate to v1 directory
cd v1

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Database Setup

```bash
# Create PostgreSQL database
createdb qna_agent

# Copy environment file
cp env.example .env

# Edit .env with your database credentials and OpenAI API key
```

### 3. Initialize Database

```bash
# Run database initialization
python -c "from database.config import init_database; init_database()"
```

### 4. Start the System

**Terminal 1 - Backend:**
```bash
python scripts/start_backend.py
```

**Terminal 2 - Frontend:**
```bash
python scripts/start_frontend.py
```

### 5. Access the Application

- **Frontend**: http://localhost:8501
- **Backend Health**: http://localhost:5000/health

## Usage

### 1. Authentication
- Enter your User ID (e.g., "user1")
- Click "Load Profiles" to see available profiles

### 2. Profile Selection
- Select a profile from the sidebar
- The system will automatically download context files for that profile

### 3. Chat Interface
- Ask questions about your data in natural language
- View real-time responses and visualizations
- Check context information in the right panel

### 4. Example Queries
```
- "Show me a summary of the data"
- "What are the data types?"
- "Create a histogram of the values"
- "Find correlations between variables"
- "Show me the trends over time"
```

## Project Structure

```
v1/
├── backend/
│   ├── agents/
│   │   └── qna_agent.py          # QnA analysis engine
│   ├── managers/
│   │   ├── context_manager.py    # File download and caching
│   │   └── session_manager.py    # Session lifecycle management
│   ├── core/
│   └── server.py                 # Socket.IO backend server
├── frontend/
│   └── app.py                    # Streamlit frontend
├── database/
│   ├── config.py                 # Database configuration
│   └── schema.sql                # Database schema
├── scripts/
│   ├── start_backend.py          # Backend startup script
│   └── start_frontend.py         # Frontend startup script
├── tests/                        # Test files
├── docs/                         # Documentation
├── requirements.txt              # Python dependencies
├── env.example                   # Environment variables template
└── README.md                     # This file
```

## Configuration

### Environment Variables

Create a `.env` file based on `env.example`:

```bash
# Database Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=qna_agent
DB_USER=postgres
DB_PASSWORD=your_password

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key

# Server Configuration
SECRET_KEY=your_secret_key
FLASK_ENV=development
```

### Database Schema

The system uses the following main tables:
- `users`: User accounts
- `user_profiles`: Profile configurations with data sources
- `chat_history`: Chat sessions
- `chat_messages`: Individual messages
- `context_files`: Download tracking

## API Reference

### Socket.IO Events

#### Client → Server
- `authenticate`: User authentication
- `start_chat`: Start chat session for profile
- `send_message`: Send chat message
- `get_chat_history`: Get session chat history
- `get_user_profiles`: Get user's profiles
- `get_context_summary`: Get data context summary
- `end_session`: End chat session

#### Server → Client
- `connected`: Connection confirmation
- `authenticated`: Authentication success
- `auth_error`: Authentication failure
- `chat_started`: Chat session created
- `message_response`: Analysis response
- `chat_history`: Chat history data
- `user_profiles`: User profile list
- `context_summary`: Context data summary
- `error`: Error messages

## Development

### Running Tests
```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_qna_agent.py
```

### Code Structure

#### Context Manager
- Handles profile-based file downloads
- Organizes files by date and profile
- Tracks download status in database

#### Session Manager
- Manages 15-minute session timeouts
- Stores chat history in memory and database
- Handles session creation and cleanup

#### QnA Agent
- Generates Python code using LLM
- Executes analysis in sandboxed environment
- Creates visualizations and saves to artifacts

#### Socket.IO Server
- Handles real-time communication
- Routes events to appropriate handlers
- Manages authentication and sessions

## Troubleshooting

### Common Issues

1. **Database Connection Failed**
   - Check PostgreSQL is running
   - Verify database credentials in `.env`
   - Ensure database `qna_agent` exists

2. **OpenAI API Errors**
   - Verify API key in `.env`
   - Check API quota and billing
   - Ensure internet connectivity

3. **Socket.IO Connection Issues**
   - Check backend is running on port 5000
   - Verify CORS settings
   - Check firewall settings

4. **File Download Failures**
   - Check internet connectivity
   - Verify data source URLs in database
   - Check file permissions in downloads directory

### Logs

Backend logs are available in the terminal where you started the backend server. Look for:
- Connection events
- Download progress
- Analysis execution
- Error messages

## Next Steps (v2)

The MVP will be enhanced in v2 with:
- Scheduled daily downloads at 1 AM
- Redis-based session persistence
- Enhanced caching and performance
- Advanced error handling
- Multi-profile support per user

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the logs for error messages
3. Verify all prerequisites are met
4. Check the database schema and sample data

## License

This project is part of the Enhanced QnA Agent System. 