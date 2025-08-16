#!/usr/bin/env python3
"""
Startup script for Mock API Server
"""
import os
import sys
import subprocess
from pathlib import Path

def main():
    """Start the Mock API Server"""
    # Get the directory of this script
    script_dir = Path(__file__).parent.absolute()
    
    # Change to the mock_api directory
    os.chdir(script_dir)
    
    # Check if .env exists, if not copy from parent
    env_file = script_dir / '.env'
    if not env_file.exists():
        parent_env = script_dir.parent / 'env.example'
        if parent_env.exists():
            import shutil
            shutil.copy(parent_env, env_file)
            print(f"✅ Copied {parent_env} to {env_file}")
        else:
            print("⚠️  No .env file found and no env.example in parent directory")
    
    # Start the server
    print("🚀 Starting Mock API Server...")
    print(f"📁 Working directory: {script_dir}")
    print("🌐 Server will be available at: http://localhost:5002")
    print("📋 API Documentation:")
    print("   - GET  /health                    - Health check")
    print("   - GET  /api/users/{user_id}       - Get user")
    print("   - POST /api/users                 - Create user")
    print("   - PUT  /api/users/{user_id}       - Update user")
    print("   - DELETE /api/users/{user_id}     - Delete user")
    print("   - GET  /api/users/{user_id}/profiles - Get user profiles")
    print("   - GET  /api/profiles/{profile_id} - Get profile")
    print("   - POST /api/profiles              - Create profile")
    print("   - PUT  /api/profiles/{profile_id} - Update profile")
    print("   - DELETE /api/profiles/{profile_id} - Delete profile")
    print()
    
    try:
        # Run the server
        subprocess.run([sys.executable, 'server.py'], check=True)
    except KeyboardInterrupt:
        print("\n👋 Mock API Server stopped")
    except Exception as e:
        print(f"❌ Failed to start Mock API Server: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
