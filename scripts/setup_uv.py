#!/usr/bin/env python3
"""
Setup script for uv-based project initialization
"""
import os
import sys
import subprocess
import platform
import shutil

def check_uv_installed():
    """Check if uv is installed"""
    try:
        subprocess.run(['uv', '--version'], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def get_python_command():
    """Get the appropriate python command"""
    # Try python3 first
    if shutil.which('python3'):
        return 'python3'
    # Then try python
    elif shutil.which('python'):
        return 'python'
    else:
        print("❌ Python not found. Please install Python 3.9+")
        return None

def install_uv():
    """Install uv if not already installed"""
    print("uv is not installed. Installing...")
    
    system = platform.system().lower()
    
    if system == "darwin" or system == "linux":
        # macOS/Linux
        install_cmd = "curl -LsSf https://astral.sh/uv/install.sh | sh"
        print(f"Running: {install_cmd}")
        os.system(install_cmd)
    elif system == "windows":
        # Windows
        install_cmd = "powershell -c \"irm https://astral.sh/uv/install.ps1 | iex\""
        print(f"Running: {install_cmd}")
        os.system(install_cmd)
    else:
        print("Unsupported operating system. Please install uv manually:")
        print("https://docs.astral.sh/uv/getting-started/installation/")
        return False
    
    return True

def setup_project():
    """Setup the project with uv"""
    print("Setting up Enhanced QnA Agent System with uv...")
    
    # Get Python command
    python_cmd = get_python_command()
    if not python_cmd:
        return False
    
    # Check if uv is installed
    if not check_uv_installed():
        if not install_uv():
            return False
    
    # Sync dependencies
    print("Installing dependencies...")
    try:
        subprocess.run(['uv', 'sync'], check=True)
        print("✅ Dependencies installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False
    
    # Copy environment file if it doesn't exist
    if not os.path.exists('.env'):
        if os.path.exists('env.example'):
            print("Creating .env file from env.example...")
            subprocess.run(['cp', 'env.example', '.env'])
            print("✅ .env file created. Please edit it with your configuration.")
        else:
            print("⚠️  env.example not found. Please create .env file manually.")
    
    print("\n🎉 Setup complete!")
    print("\nNext steps:")
    print("1. Install PostgreSQL if not already installed:")
    print("   brew install postgresql@15")
    print("   brew services start postgresql@15")
    print("   createdb qna_agent")
    print("2. Edit .env file with your database credentials and OpenAI API key")
    print(f"3. Initialize the database: uv run {python_cmd} -c \"from database.config import init_database; init_database()\"")
    print(f"4. Start the backend: uv run {python_cmd} scripts/start_backend.py")
    print(f"5. Start the frontend: uv run {python_cmd} scripts/start_frontend.py")
    
    return True

if __name__ == "__main__":
    setup_project()
