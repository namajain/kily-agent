#!/usr/bin/env python3
"""
Interactive demo for the QnA Agent with CSV download and code interpreter capabilities.
"""

import os
from dotenv import load_dotenv
from advanced_qna_agent import AdvancedQnAAgent

def main():
    # Load environment variables
    load_dotenv()
    
    # Check for OpenAI API key
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  Warning: OPENAI_API_KEY not found in environment variables.")
        print("Please set your OpenAI API key in a .env file or environment variable.")
        print("Example .env file:")
        print("OPENAI_API_KEY=your-api-key-here")
        return
    
    # Initialize the agent
    print("🤖 Initializing QnA Agent...")
    agent = AdvancedQnAAgent()
    
    print("\n" + "="*60)
    print("🎯 QnA Agent with CSV Download & Code Interpreter")
    print("="*60)
    print("\nAvailable commands:")
    print("- Download CSV: 'download https://example.com/data.csv'")
    print("- List files: 'list csv files'")
    print("- Load existing: 'load employees.csv' or 'load csv'")
    print("- Analyze data: 'show me a summary'")
    print("- Run code: 'run code: ```python\nprint(df.head())\n```'")
    print("- Visualize: 'create a plot'")
    print("- Quit: 'quit' or 'exit'")
    print("\nNote: CSV files are saved to the 'downloads/' folder")
    print("\n" + "="*60)
    
    # Interactive loop
    while True:
        try:
            # Get user input
            user_input = input("\n💬 You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            
            if not user_input:
                continue
            
            # Process the input
            print("🤖 Agent: Processing...")
            response = agent.chat(user_input)
            
            print(f"🤖 Agent: {response}")
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    main() 