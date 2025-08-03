#!/usr/bin/env python3
"""
Test script for the QnA Agent to verify functionality.
"""

import os
import sys
from dotenv import load_dotenv

def test_imports():
    """Test that all required modules can be imported."""
    try:
        import langgraph
        import langchain
        import langchain_openai
        import pandas as pd
        import numpy as np
        import matplotlib.pyplot as plt
        import seaborn as sns
        import plotly.express as px
        import requests
        print("✅ All imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_agent_creation():
    """Test that the agent can be created."""
    try:
        from advanced_qna_agent import AdvancedQnAAgent
        agent = AdvancedQnAAgent()
        print("✅ Agent creation successful")
        return True
    except Exception as e:
        print(f"❌ Agent creation failed: {e}")
        return False

def test_basic_functionality():
    """Test basic agent functionality."""
    try:
        from advanced_qna_agent import AdvancedQnAAgent
        
        # Initialize agent
        agent = AdvancedQnAAgent()
        
        # Test simple query
        response = agent.chat("Hello")
        print("✅ Basic functionality test passed")
        return True
    except Exception as e:
        print(f"❌ Basic functionality test failed: {e}")
        return False

def test_csv_download():
    """Test CSV download functionality."""
    try:
        import requests
        
        # Test with a simple CSV URL
        test_url = "https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv"
        response = requests.get(test_url)
        response.raise_for_status()
        
        print("✅ CSV download test passed")
        return True
    except Exception as e:
        print(f"❌ CSV download test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 Running QnA Agent Tests")
    print("=" * 40)
    
    # Load environment variables
    load_dotenv()
    
    # Check API key
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  Warning: OPENAI_API_KEY not found")
        print("Some tests may fail without API key")
    
    # Run tests
    tests = [
        ("Import Test", test_imports),
        ("Agent Creation Test", test_agent_creation),
        ("Basic Functionality Test", test_basic_functionality),
        ("CSV Download Test", test_csv_download),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Running {test_name}...")
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} failed")
    
    print("\n" + "=" * 40)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The agent is ready to use.")
        print("\nTo run the interactive demo:")
        print("uv run python demo.py")
        print("\nOr with pip:")
        print("python demo.py")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 