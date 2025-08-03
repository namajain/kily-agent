#!/usr/bin/env python3
"""
Test runner for the QnA Agent.

This script can run all tests or specific test files.
"""

import sys
import os
import subprocess
import argparse
from pathlib import Path

def run_test_file(test_file: str) -> bool:
    """Run a specific test file."""
    test_path = Path(__file__).parent / test_file
    
    if not test_path.exists():
        print(f"❌ Test file not found: {test_file}")
        return False
    
    print(f"🧪 Running test: {test_file}")
    print("-" * 50)
    
    try:
        result = subprocess.run([
            sys.executable, str(test_path)
        ], capture_output=True, text=True, cwd=Path(__file__).parent)
        
        if result.returncode == 0:
            print(f"✅ {test_file} passed")
            if result.stdout:
                print(result.stdout)
            return True
        else:
            print(f"❌ {test_file} failed")
            if result.stderr:
                print(result.stderr)
            if result.stdout:
                print(result.stdout)
            return False
            
    except Exception as e:
        print(f"❌ Error running {test_file}: {e}")
        return False

def run_all_tests():
    """Run all test files."""
    test_files = [
        "test_agent.py",
        "test_llm_analysis.py", 
        "test_load_functionality.py",
        "demo.py",
        "example_usage.py"
    ]
    
    print("🚀 Running all tests...")
    print("=" * 50)
    
    passed = 0
    failed = 0
    
    for test_file in test_files:
        if run_test_file(test_file):
            passed += 1
        else:
            failed += 1
        print()
    
    print("=" * 50)
    print(f"📊 Test Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All tests passed!")
        return True
    else:
        print("❌ Some tests failed!")
        return False

def list_tests():
    """List all available test files."""
    test_files = [
        "test_agent.py - Basic agent functionality tests",
        "test_llm_analysis.py - LLM-powered analysis demonstration",
        "test_load_functionality.py - File loading functionality tests",
        "demo.py - Interactive demo script",
        "example_usage.py - Programmatic usage examples"
    ]
    
    print("📋 Available Tests:")
    print("-" * 50)
    for test_file in test_files:
        print(f"  • {test_file}")

def main():
    parser = argparse.ArgumentParser(description="Run QnA Agent tests")
    parser.add_argument(
        "test_file", 
        nargs="?", 
        help="Specific test file to run (optional)"
    )
    parser.add_argument(
        "--list", 
        action="store_true", 
        help="List all available tests"
    )
    
    args = parser.parse_args()
    
    if args.list:
        list_tests()
        return
    
    if args.test_file:
        success = run_test_file(args.test_file)
        sys.exit(0 if success else 1)
    else:
        success = run_all_tests()
        sys.exit(0 if success else 1)

if __name__ == "__main__":
    main() 