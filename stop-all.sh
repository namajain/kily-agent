#!/bin/bash

# Enhanced QnA Agent System - Stop All Services Script

echo "🛑 Stopping Enhanced QnA Agent System..."
echo "========================================"

# Stop all Python services
echo "📊 Stopping Data Service..."
pkill -f "python.*server.py" 2>/dev/null || echo "   No Data Service processes found"

echo "🔧 Stopping Backend Service..."
pkill -f "python.*start_backend.py" 2>/dev/null || echo "   No Backend Service processes found"

# Stop React frontend
echo "🌐 Stopping React Frontend..."
pkill -f "react-scripts" 2>/dev/null || echo "   No React Frontend processes found"
pkill -f "node.*react-scripts" 2>/dev/null || echo "   No React Frontend node processes found"

# Wait a moment for processes to stop
sleep 2

# Check if any processes are still running
echo "🔍 Checking for remaining processes..."
if pgrep -f "python.*server.py" >/dev/null; then
    echo "⚠️  Data Service processes still running, force killing..."
    pkill -9 -f "python.*server.py" 2>/dev/null || true
fi

if pgrep -f "python.*start_backend.py" >/dev/null; then
    echo "⚠️  Backend Service processes still running, force killing..."
    pkill -9 -f "python.*start_backend.py" 2>/dev/null || true
fi

if pgrep -f "react-scripts" >/dev/null; then
    echo "⚠️  React Frontend processes still running, force killing..."
    pkill -9 -f "react-scripts" 2>/dev/null || true
fi

echo ""
echo "✅ All services stopped successfully!"
echo "========================================"
echo "📊 Data Service:    http://localhost:5002/health (stopped)"
echo "🔧 Backend Service: http://localhost:5001/health (stopped)"
echo "🌐 React Frontend:  http://localhost:3000 (stopped)"
echo ""
echo "🚀 To start all services again, run: ./start-all.sh"
