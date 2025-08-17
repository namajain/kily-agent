#!/bin/bash

# Enhanced QnA Agent System - Start All Services Script

echo "🚀 Starting Enhanced QnA Agent System..."
echo "========================================"

# Function to check if a port is in use
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null ; then
        echo "⚠️  Port $port is already in use"
        return 1
    else
        return 0
    fi
}

# Function to wait for a service to be ready
wait_for_service() {
    local url=$1
    local service_name=$2
    local max_attempts=30
    local attempt=1
    
    echo "⏳ Waiting for $service_name to be ready..."
    while [ $attempt -le $max_attempts ]; do
        if curl -s "$url" >/dev/null 2>&1; then
            echo "✅ $service_name is ready!"
            return 0
        fi
        echo "   Attempt $attempt/$max_attempts..."
        sleep 2
        ((attempt++))
    done
    echo "❌ $service_name failed to start after $max_attempts attempts"
    return 1
}

# Stop any existing services
echo "🛑 Stopping any existing services..."
pkill -f "python.*server.py" 2>/dev/null || true
pkill -f "python.*start_backend.py" 2>/dev/null || true
pkill -f "react-scripts" 2>/dev/null || true
pkill -f "node.*react-scripts" 2>/dev/null || true
sleep 2

# Check if ports are available
echo "🔍 Checking port availability..."
check_port 5002 || exit 1
check_port 5001 || exit 1
check_port 3000 || exit 1

# Start Data Service
echo "📊 Starting Data Service..."
cd data_service
DB_PASSWORD=password uv run python3 server.py &
DATA_SERVICE_PID=$!
cd ..

# Wait for Data Service to be ready
if wait_for_service "http://localhost:5002/health" "Data Service"; then
    echo "✅ Data Service started successfully (PID: $DATA_SERVICE_PID)"
else
    echo "❌ Failed to start Data Service"
    kill $DATA_SERVICE_PID 2>/dev/null || true
    exit 1
fi

# Start Backend Service
echo "🔧 Starting Backend Service..."
uv run python3 scripts/start_backend.py &
BACKEND_PID=$!

# Wait for Backend to be ready
if wait_for_service "http://localhost:5001/health" "Backend Service"; then
    echo "✅ Backend Service started successfully (PID: $BACKEND_PID)"
else
    echo "❌ Failed to start Backend Service"
    kill $DATA_SERVICE_PID $BACKEND_PID 2>/dev/null || true
    exit 1
fi

# Start React Frontend
echo "🌐 Starting React Frontend..."
cd frontend-react
npm start &
FRONTEND_PID=$!
cd ..

# Wait for React Frontend to be ready
if wait_for_service "http://localhost:3000" "React Frontend"; then
    echo "✅ React Frontend started successfully (PID: $FRONTEND_PID)"
else
    echo "❌ Failed to start React Frontend"
    kill $DATA_SERVICE_PID $BACKEND_PID $FRONTEND_PID 2>/dev/null || true
    exit 1
fi

echo ""
echo "🎉 All services started successfully!"
echo "========================================"
echo "📊 Data Service:    http://localhost:5002/health"
echo "🔧 Backend Service: http://localhost:5001/health"
echo "🌐 React Frontend:  http://localhost:3000"
echo ""
echo "📝 Service PIDs:"
echo "   Data Service: $DATA_SERVICE_PID"
echo "   Backend:      $BACKEND_PID"
echo "   Frontend:     $FRONTEND_PID"
echo ""
echo "🛑 To stop all services, run: ./stop-all.sh"
echo "   Or press Ctrl+C to stop this script"
echo ""

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping all services..."
    kill $DATA_SERVICE_PID $BACKEND_PID $FRONTEND_PID 2>/dev/null || true
    pkill -f "python.*server.py" 2>/dev/null || true
    pkill -f "python.*start_backend.py" 2>/dev/null || true
    pkill -f "react-scripts" 2>/dev/null || true
    echo "✅ All services stopped"
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Keep the script running
echo "🔄 Services are running. Press Ctrl+C to stop all services..."
while true; do
    sleep 10
    # Check if all services are still running
    if ! kill -0 $DATA_SERVICE_PID 2>/dev/null; then
        echo "❌ Data Service stopped unexpectedly"
        cleanup
    fi
    if ! kill -0 $BACKEND_PID 2>/dev/null; then
        echo "❌ Backend Service stopped unexpectedly"
        cleanup
    fi
    if ! kill -0 $FRONTEND_PID 2>/dev/null; then
        echo "❌ React Frontend stopped unexpectedly"
        cleanup
    fi
done
