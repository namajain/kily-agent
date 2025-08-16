# React Frontend for Enhanced QnA Agent

A modern, responsive React frontend for the Enhanced QnA Agent System.

## Features

- 🎨 **Modern UI**: Clean, responsive design with Tailwind CSS
- 🔄 **Real-time Chat**: Socket.IO integration for live chat functionality
- 📊 **Profile Management**: View and select data profiles with multiple data sources
- 📱 **Responsive Design**: Works on desktop, tablet, and mobile devices
- ⚡ **Fast Performance**: Optimized React components with hooks
- 🔌 **Easy Integration**: REST API and Socket.IO communication with backend

## Tech Stack

- **React 18** - Modern React with hooks
- **Tailwind CSS** - Utility-first CSS framework
- **Socket.IO Client** - Real-time communication
- **Axios** - HTTP client for API calls
- **React Router** - Client-side routing
- **Lucide React** - Beautiful icons
- **PostCSS** - CSS processing

## Getting Started

### Prerequisites

- Node.js 16+ 
- npm or yarn
- Backend services running (Mock API, Backend, Database)

### Installation

1. Navigate to the frontend directory:
```bash
cd frontend-react
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

The app will open at `http://localhost:3000`

### Environment Variables

Create a `.env` file in the `frontend-react` directory:

```env
REACT_APP_BACKEND_URL=http://localhost:5001
```

## Project Structure

```
frontend-react/
├── public/
│   └── index.html
├── src/
│   ├── components/
│   │   ├── Header.js          # App header with connection status
│   │   ├── Sidebar.js         # Profile management sidebar
│   │   ├── ChatInterface.js   # Real-time chat interface
│   │   └── ProfileList.js     # Profile list component
│   ├── App.js                 # Main app component
│   ├── index.js              # React entry point
│   └── index.css             # Global styles with Tailwind
├── package.json
├── tailwind.config.js
└── postcss.config.js
```

## Usage

1. **Load Profiles**: Enter a user ID and click "Load Profiles" to fetch available data profiles
2. **View Data Sources**: Expand profile cards to see associated data sources
3. **Start Chat**: Select a profile to begin a chat session
4. **Ask Questions**: Use the chat interface to ask questions about your data
5. **Real-time Responses**: Get instant AI-powered responses via Socket.IO

## Development

### Available Scripts

- `npm start` - Start development server
- `npm build` - Build for production
- `npm test` - Run tests
- `npm eject` - Eject from Create React App

### Styling

The app uses Tailwind CSS for styling. Custom styles are defined in `src/index.css` using Tailwind's `@layer` directive.

### Component Architecture

- **App.js**: Main container with state management and Socket.IO setup
- **Header.js**: Displays app title and connection status
- **Sidebar.js**: Handles profile loading and selection
- **ChatInterface.js**: Manages chat functionality and message display

## API Integration

### REST Endpoints

- `GET /api/users/{userId}/profiles` - Fetch user profiles
- `GET /health` - Health check

### Socket.IO Events

- `connect` - Connection established
- `disconnect` - Connection lost
- `chat_started` - Chat session started
- `message_response` - Received message response
- `error` - Error events

## Building for Production

```bash
npm run build
```

This creates a `build` folder with optimized production files.

## Troubleshooting

### Connection Issues

- Ensure backend services are running
- Check `REACT_APP_BACKEND_URL` environment variable
- Verify CORS settings on backend

### Profile Loading Issues

- Check Mock API is running on port 5002
- Verify database has sample data
- Check browser console for errors

## Contributing

1. Follow React best practices
2. Use functional components with hooks
3. Maintain consistent styling with Tailwind
4. Add proper error handling
5. Test Socket.IO functionality
