#!/usr/bin/env python3
"""
Setup script for React frontend
"""
import os
import subprocess
import sys
from pathlib import Path

def check_node_installed():
    """Check if Node.js is installed"""
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Node.js found: {result.stdout.strip()}")
            return True
        else:
            print("❌ Node.js not found")
            return False
    except FileNotFoundError:
        print("❌ Node.js not found")
        return False

def check_npm_installed():
    """Check if npm is installed"""
    try:
        result = subprocess.run(['npm', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ npm found: {result.stdout.strip()}")
            return True
        else:
            print("❌ npm not found")
            return False
    except FileNotFoundError:
        print("❌ npm not found")
        return False

def install_dependencies():
    """Install React frontend dependencies"""
    frontend_dir = Path("frontend-react")
    
    if not frontend_dir.exists():
        print("❌ frontend-react directory not found")
        return False
    
    print("📦 Installing React frontend dependencies...")
    
    try:
        # Change to frontend directory
        os.chdir(frontend_dir)
        
        # Install dependencies
        result = subprocess.run(['npm', 'install'], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ React frontend dependencies installed successfully")
            return True
        else:
            print(f"❌ Failed to install dependencies: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error installing dependencies: {e}")
        return False
    finally:
        # Change back to root directory
        os.chdir("..")

def create_env_file():
    """Create .env file for React frontend"""
    frontend_dir = Path("frontend-react")
    env_file = frontend_dir / ".env"
    
    if env_file.exists():
        print("✅ .env file already exists")
        return True
    
    try:
        env_content = """# React Frontend Environment Variables
REACT_APP_BACKEND_URL=http://localhost:5001
"""
        
        with open(env_file, 'w') as f:
            f.write(env_content)
        
        print("✅ Created .env file")
        return True
        
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 Setting up React Frontend for Enhanced QnA Agent")
    print("=" * 50)
    
    # Check prerequisites
    print("\n📋 Checking prerequisites...")
    if not check_node_installed():
        print("\n❌ Please install Node.js first:")
        print("   Visit: https://nodejs.org/")
        print("   Or use: brew install node (macOS)")
        return False
    
    if not check_npm_installed():
        print("\n❌ Please install npm first")
        return False
    
    # Install dependencies
    print("\n📦 Installing dependencies...")
    if not install_dependencies():
        return False
    
    # Create environment file
    print("\n⚙️  Setting up environment...")
    if not create_env_file():
        return False
    
    print("\n🎉 React frontend setup completed!")
    print("\n📝 Next steps:")
    print("   1. Start the backend services: make run-all")
    print("   2. Start the React frontend: make run-react")
    print("   3. Open http://localhost:3000 in your browser")
    print("\n📚 For more information, see: frontend-react/README.md")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
