#!/usr/bin/env python3
"""
Example usage of the QnA Agent with CSV download and code interpreter.
"""

import os
from dotenv import load_dotenv
from advanced_qna_agent import AdvancedQnAAgent

def main():
    """Demonstrate the agent's capabilities."""
    
    # Load environment variables
    load_dotenv()
    
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY not found in environment variables.")
        print("Please set your OpenAI API key in a .env file:")
        print("OPENAI_API_KEY=your-api-key-here")
        return
    
    print("🚀 Starting QnA Agent Demo")
    print("=" * 50)
    
    # Initialize the agent
    agent = AdvancedQnAAgent()
    
    # Example 1: Download and analyze COVID-19 data
    print("\n📊 Example 1: Downloading and analyzing COVID-19 data")
    print("-" * 50)
    
    covid_url = "https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv"
    
    print(f"Downloading CSV from: {covid_url}")
    response = agent.chat(f"Download {covid_url}")
    print(f"Response: {response}")
    
    print("\nAnalyzing the data...")
    response = agent.chat("Show me a summary of the data")
    print(f"Response: {response}")
    
    # Example 2: Run custom code analysis
    print("\n💻 Example 2: Running custom code analysis")
    print("-" * 50)
    
    custom_code = """
```python
import pandas as pd
import matplotlib.pyplot as plt

# Basic info
print("Dataset shape:", df.shape)
print("Columns:", list(df.columns))

# Show first few rows
print("\\nFirst 5 rows:")
print(df.head())

# Summary statistics
print("\\nSummary statistics:")
print(df.describe())

# Check for missing values
print("\\nMissing values:")
print(df.isnull().sum())

# If there are numeric columns, create a simple plot
numeric_cols = df.select_dtypes(include=['number']).columns
if len(numeric_cols) > 0:
    print(f"\\nNumeric columns: {list(numeric_cols)}")
    # Create a simple histogram for the first numeric column
    if len(numeric_cols) > 0:
        plt.figure(figsize=(10, 6))
        df[numeric_cols[0]].hist(bins=20)
        plt.title(f'Distribution of {numeric_cols[0]}')
        plt.xlabel(numeric_cols[0])
        plt.ylabel('Frequency')
        plt.savefig('example_analysis.png')
        plt.close()
        print("\\nPlot saved as 'example_analysis.png'")
```
"""
    
    print("Running custom code analysis...")
    response = agent.chat(f"Run this code: {custom_code}")
    print(f"Response: {response}")
    
    # Example 3: Ask specific questions
    print("\n❓ Example 3: Asking specific questions")
    print("-" * 50)
    
    questions = [
        "What are the data types of each column?",
        "Show me the first 10 rows",
        "Are there any missing values?",
        "Create a correlation matrix if possible"
    ]
    
    for question in questions:
        print(f"\nQ: {question}")
        response = agent.chat(question)
        print(f"A: {response}")
    
    print("\n" + "=" * 50)
    print("✅ Demo completed successfully!")
    print("\nTo try the interactive version, run:")
    print("uv run python demo.py")
    print("\nOr with pip:")
    print("python demo.py")

if __name__ == "__main__":
    main() 