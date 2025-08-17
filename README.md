# Enhanced QnA Agent System - MVP

## Overview

This is the MVP (Minimum Viable Product) implementation of the Enhanced QnA Agent System. It provides a real-time, profile-based data analysis platform with natural language query processing.

## Features

### ✅ MVP Features
- **Profile-based Context Management**: On-demand file downloads for specific profiles
- **Session Management**: 15-minute timeout sessions with profile context
- **Real-time Communication**: Socket.IO backend with React frontend
- **Natural Language Analysis**: LLM-powered query processing
- **Database Integration**: PostgreSQL for persistent storage
- **File Organization**: Date-based file structure (`downloads/YYYY-MM-DD/profile_id/`)

### 🔄 Workflow
1. User selects a profile from the frontend
2. Backend creates session and downloads context files (if needed)
3. User asks questions in natural language
4. QnA agent analyzes data using profile context
5. Results are streamed back in real-time

## Architecture Vision

```┌─────────────────────────────────────────────────────────────────────────────┐
│                              CLIENT LAYER                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────────────┐  │
│  │   React         │    │   Web Client    │    │     Mobile Client       │  │
│  │   Frontend      │    │   (Vue/Angular) │    │                         │  │
│  └─────────────────┘    └─────────────────┘    └─────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ WebSocket/Socket.IO
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           COMMUNICATION LAYER                               │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │                    Socket.IO Server (Backend)                          │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │ │
│  │  │   Auth      │  │   Cache     │  │   Chat      │  │   File      │    │ │
│  │  │  Manager    │  │  Manager    │  │  Manager    │  │  Manager    │    │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘    │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ Internal API Calls
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                            BUSINESS LOGIC LAYER                             │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────────────┐  │
│  │   Context       │    │   Session       │    │      QnA Agent          │  │
│  │   Manager       │    │   Manager       │    │                         │  │
│  └─────────────────┘    └─────────────────┘    └─────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ Data Access
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                             DATA LAYER                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────────────┐  │
│  │   File System   │    │   Database      │    │     Cache (Redis)       │  │
│  │   (Downloads)   │    │   (PostgreSQL)  │    │                         │  │
│  └─────────────────┘    └─────────────────┘    └─────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Architecture

The system is now split into three main components:

1. **Data Service** (`data_service/`) - Handles all database operations via REST endpoints
2. **Backend Server** (`backend/`) - Flask Socket.IO server that communicates with Mock API
3. **Frontend** (`frontend-react/`) - React application that connects to the backend

This separation provides:
- **Clean separation of concerns** - Database logic is isolated
- **Scalability** - Each component can be scaled independently
- **Testability** - Each component can be tested in isolation
- **Flexibility** - Easy to swap out database layer or add new APIs

## Quick Start

### Prerequisites
- Python 3.9+
- PostgreSQL 13+ (see installation steps below)
- OpenAI API key
- uv (Python package manager)

### PostgreSQL Installation

**On macOS (using Homebrew):**
```bash
# Install PostgreSQL
brew install postgresql@15

# Start PostgreSQL service
brew services start postgresql@15

# Add to PATH (add to ~/.zshrc or ~/.bash_profile)
echo 'export PATH="/opt/homebrew/opt/postgresql@15/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# Create database
createdb qna_agent
```

**On other systems:**
- Download from: https://www.postgresql.org/download/
- Follow the installation wizard
- Create a database named `qna_agent`

### Install uv

If you don't have uv installed, install it first:

```bash
# On macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Or with pip
pip install uv
```

### 1. Setup Environment

**Option 1: Automated Setup (Recommended)**
```bash
# Clone and navigate to v1 directory
cd v1

# Run the automated setup script
python3 scripts/setup_uv.py
```

**Option 2: Manual Setup**
```bash
# Clone and navigate to v1 directory
cd v1

# Create virtual environment and install dependencies
uv sync

# Activate the virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
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
uv run python3 -c "from database.config import init_database; init_database()"
```

### 4. Start the System

**Option 1: Start All Services (Recommended)**
```bash
make run-all
```

**Option 2: Start Services Individually**

**Terminal 1 - Data Service (Database Layer):**
```bash
make run-data-service
```

**Terminal 2 - Backend (Socket.IO Server):**
```bash
make run-backend
```

**Terminal 3 - React Frontend (Modern Web App):**
```bash
make run-react
```



### 5. Access the Application

- **React Frontend**: http://localhost:3000
- **Backend Health**: http://localhost:5001/health
- **Data Service Health**: http://localhost:5002/health

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
├── backend/
│   ├── agents/
│   │   └── qna_agent.py          # QnA analysis engine
│   ├── managers/
│   │   ├── context_manager.py    # File download and caching
│   │   └── session_manager.py    # Session lifecycle management
│   ├── utils/
│   │   └── prompt_manager.py     # LLM prompt management
│   ├── core/
│   └── server.py                 # Socket.IO backend server
├── prompts/                      # LLM prompt templates
│   ├── analysis_code_generation.txt
│   ├── conversational_response.txt
│   ├── execution_history_context.txt
│   ├── conversational_query_context.txt
│   └── README.md                 # Prompt documentation

├── frontend-react/               # Modern React frontend
│   ├── src/
│   │   ├── components/           # React components
│   │   ├── App.js               # Main React app
│   │   └── index.js             # React entry point
│   ├── package.json             # Node.js dependencies
│   └── README.md                # React frontend docs
├── data_service/                # Data service layer
│   ├── server.py                # REST API server
│   ├── models.py                # Data models
│   └── database.py              # Database connection
├── database/
│   ├── config.py                # Database configuration
│   └── schema.sql               # Database schema
├── scripts/
│   ├── start_backend.py         # Backend startup script
│   ├── setup_uv.py              # Python setup script
│   └── setup_react_frontend.py  # React setup script
├── tests/                       # Test files
├── pyproject.toml               # Python project configuration
├── Makefile                     # Development convenience commands
├── .gitignore                   # Git ignore patterns
├── env.example                  # Environment variables template
└── README.md                    # This file
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

### uv Commands

The project uses `uv` for dependency management. Here are some useful commands:

```bash
# Install dependencies
uv sync

# Add a new dependency
uv add package-name

# Add a development dependency
uv add --dev package-name

# Remove a dependency
uv remove package-name

# Update dependencies
uv lock --upgrade

# Run a command in the virtual environment
uv run python script.py

# Activate the virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### Makefile Commands

For convenience, you can also use the provided Makefile:

```bash
# Show all available commands
make help

# Setup the project
make setup

# Install dependencies
make install

# Run tests
make test

# Start backend
make run-backend

# Start frontend
make run-frontend

# Format code
make format

# Run linting
make lint

# Clean up generated files
make clean
```

### Running Tests
```bash
# Run all tests
uv run pytest tests/

# Run specific test file
uv run pytest tests/test_qna_agent.py

# Run with coverage
uv run pytest tests/ --cov=backend --cov=frontend
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