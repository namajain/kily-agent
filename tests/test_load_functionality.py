#!/usr/bin/env python3
"""
Test script to demonstrate the load existing CSV functionality.
"""

from advanced_qna_agent import AdvancedQnAAgent

def main():
    """Demonstrate loading existing CSV files."""
    
    print("=" * 60)
    print("LOAD EXISTING CSV FILES DEMONSTRATION")
    print("=" * 60)
    
    # Initialize the agent
    agent = AdvancedQnAAgent()
    
    # Test 1: List available files
    print("\n1. Listing available CSV files:")
    print("-" * 40)
    result = agent.chat("list csv files")
    print(result)
    
    # Test 2: Load a specific file
    print("\n2. Loading employees.csv:")
    print("-" * 40)
    result = agent.chat("load employees.csv")
    print(result)
    
    # Test 3: Load most recent file
    print("\n3. Loading most recent CSV file:")
    print("-" * 40)
    result = agent.chat("load csv")
    print(result)
    
    # Test 4: Try to analyze without loading (should fail)
    print("\n4. Trying to analyze without loading (should fail):")
    print("-" * 40)
    agent.current_csv_file = None  # Reset
    result = agent.chat("show me a summary")
    print(result)
    
    # Test 5: Load and analyze
    print("\n5. Loading and analyzing:")
    print("-" * 40)
    result = agent.chat("load employees.csv")
    print(result)
    
    result = agent.chat("which employee has the highest salary?")
    print(result)
    
    print("\n" + "=" * 60)
    print("DEMONSTRATION COMPLETE")
    print("=" * 60)
    print("\nKey features demonstrated:")
    print("✅ List available CSV files")
    print("✅ Load specific CSV files")
    print("✅ Load most recent CSV file")
    print("✅ Error handling for missing files")
    print("✅ Integration with analysis workflow")

if __name__ == "__main__":
    main() 