# Data Service

A Flask-based REST API server that handles all database operations for the Enhanced QnA Agent system.

## Features

- **User Management**: CRUD operations for users
- **Profile Management**: CRUD operations for user profiles
- **Database Abstraction**: All database logic centralized here
- **RESTful Endpoints**: Clean API interface for other services

## API Endpoints

### Users
- `GET /api/users/{user_id}` - Get user by ID
- `POST /api/users` - Create new user
- `PUT /api/users/{user_id}` - Update user
- `DELETE /api/users/{user_id}` - Delete user

### Profiles
- `GET /api/users/{user_id}/profiles` - Get all profiles for a user
- `GET /api/profiles/{profile_id}` - Get profile by ID
- `POST /api/profiles` - Create new profile
- `PUT /api/profiles/{profile_id}` - Update profile
- `DELETE /api/profiles/{profile_id}` - Delete profile

### Health
- `GET /health` - Health check endpoint

## Setup

1. Install dependencies:
   ```bash
   cd data_service
   uv sync
   ```

2. Set up environment variables (copy from parent project):
   ```bash
   cp ../env.example .env
   # Edit .env with your database settings
   ```

3. Run the server:
   ```bash
   uv run python3 data_service/server.py
   ```

## Usage

The server runs on `http://localhost:5002` by default and provides REST endpoints that the main backend can call instead of directly accessing the database.

## Development

- Run tests: `uv run pytest`
- Format code: `uv run black .`
- Lint code: `uv run flake8`
