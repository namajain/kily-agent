import os
import json
import requests
import pandas as pd
import numpy as np
from typing import Optional
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import tempfile

# Load environment variables
load_dotenv()

# Initialize OpenAI client
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    llm = None
else:
    llm = ChatOpenAI(
        model="gpt-4",
        temperature=0,
        api_key=api_key
    )

# Main agent class
class AdvancedQnAAgent:
    def __init__(self):
        self.current_csv_file = None
    
    def download_csv(self, url: str) -> str:
        """Download a CSV file from URL."""
        try:
            response = requests.get(url)
            response.raise_for_status()
            
            # Create downloads directory if it doesn't exist
            downloads_dir = "downloads"
            os.makedirs(downloads_dir, exist_ok=True)
            
            # Extract filename from URL or use timestamp
            if "/" in url:
                filename = url.split("/")[-1]
                if not filename.endswith('.csv'):
                    filename = f"{filename}.csv"
            else:
                filename = f"data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            
            # Save to downloads folder
            filepath = os.path.join(downloads_dir, filename)
            with open(filepath, 'w') as f:
                f.write(response.text)
            
            self.current_csv_file = filepath
            
            return f"CSV downloaded successfully to {filepath}"
            
        except Exception as e:
            return f"Error downloading CSV: {str(e)}"
    
    def load_existing_csv(self, message: str) -> str:
        """Load an existing CSV file from the downloads folder."""
        try:
            import os
            import glob
            
            # Check if downloads folder exists
            downloads_dir = "downloads"
            if not os.path.exists(downloads_dir):
                return "No downloads folder found. Please download a CSV file first."
            
            # Get all CSV files in downloads folder
            csv_files = glob.glob(os.path.join(downloads_dir, "*.csv"))
            
            if not csv_files:
                return "No CSV files found in downloads folder. Please download a CSV file first."
            
            # Extract filename from message if provided
            message_lower = message.lower()
            filename = None
            
            # Look for specific filename in the message
            for file in csv_files:
                file_basename = os.path.basename(file)
                if file_basename.lower() in message_lower:
                    filename = file
                    break
            
            # If no specific file mentioned, use the most recent one
            if not filename:
                # Sort by modification time (most recent first)
                csv_files.sort(key=os.path.getmtime, reverse=True)
                filename = csv_files[0]
            
            # Load the CSV file
            self.current_csv_file = filename
            df = pd.read_csv(filename)
            
            return f"Loaded CSV file: {os.path.basename(filename)}\nDataset: {df.shape[0]} rows, {df.shape[1]} columns\nColumns: {list(df.columns)}"
            
        except Exception as e:
            return f"Error loading CSV file: {str(e)}"
    
    def list_available_csv_files(self) -> str:
        """List all available CSV files in the downloads folder."""
        try:
            import os
            import glob
            
            # Check if downloads folder exists
            downloads_dir = "downloads"
            if not os.path.exists(downloads_dir):
                return "No downloads folder found."
            
            # Get all CSV files in downloads folder
            csv_files = glob.glob(os.path.join(downloads_dir, "*.csv"))
            
            if not csv_files:
                return "No CSV files found in downloads folder."
            
            # Sort by modification time (most recent first)
            csv_files.sort(key=os.path.getmtime, reverse=True)
            
            result = "Available CSV files:\n"
            for i, file in enumerate(csv_files, 1):
                filename = os.path.basename(file)
                size = os.path.getsize(file)
                modified = datetime.fromtimestamp(os.path.getmtime(file))
                result += f"{i}. {filename} ({size:,} bytes, modified {modified.strftime('%Y-%m-%d %H:%M')})\n"
            
            return result
            
        except Exception as e:
            return f"Error listing CSV files: {str(e)}"
    
    def analyze_data(self, query: str) -> str:
        """Analyze the current CSV data using dynamically generated code."""
        if not self.current_csv_file:
            return "No CSV file loaded. Please download a CSV file first."
        
        try:
            df = pd.read_csv(self.current_csv_file)
            
            # Generate code based on the query
            code = self._generate_analysis_code(query, df)
            
            # Execute the generated code
            result = self._execute_analysis_code(code, df)
            
            return result
            
        except Exception as e:
            return f"Error analyzing data: {str(e)}"
    
    def _generate_analysis_code(self, query: str, df: pd.DataFrame) -> str:
        """Generate Python code using LLM based on the natural language query and dataset summary."""
        
        # Create dataset summary
        dataset_summary = self._create_dataset_summary(df)
        
        # Create system prompt
        system_prompt = f"""You are a data analysis expert. Given a dataset summary and a natural language query, generate Python code to analyze the data.

Available packages: pandas (pd), numpy (np), matplotlib.pyplot (plt), seaborn (sns), plotly.express (px), plotly.graph_objects (go)

Dataset Summary:
{dataset_summary}

Requirements:
1. The dataframe is already loaded as 'df'
2. Generate only the analysis code, not the data loading
3. Use print() statements to output results
4. For visualizations, ALWAYS save plots to the artifacts folder using: plt.savefig(f'{{artifacts_dir}}/plot_name.png')
5. Handle missing values appropriately
6. Provide clear, informative output
7. Use proper formatting for currency, percentages, etc.
8. Include error handling where appropriate
9. Focus on answering the specific query asked
10. Generate complete, executable Python code
11. The artifacts_dir variable is available in the execution environment

Generate clean, efficient Python code that directly answers the user's query."""

        # Create user message
        user_message = f"Query: {query}\n\nGenerate Python code to analyze the data based on this query."

        try:
            # Check if LLM is available
            if llm is None:
                return "LLM not available. Please check your OpenAI API key in the .env file."
            
            # Generate code using LLM
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_message)
            ]
            
            response = llm.invoke(messages)
            generated_code = response.content
            
            # Clean up the generated code
            code = self._clean_generated_code(generated_code)
            
            return code
            
        except Exception as e:
            # If LLM fails, return error message
            return f"Error generating analysis code: {str(e)}"
    
    def _create_dataset_summary(self, df: pd.DataFrame) -> str:
        """Create a comprehensive summary of the dataset for the LLM."""
        summary = f"""
Dataset Shape: {df.shape[0]} rows, {df.shape[1]} columns

Columns and Data Types:
"""
        
        for col in df.columns:
            dtype = str(df[col].dtype)
            unique_count = df[col].nunique()
            missing_count = df[col].isnull().sum()
            
            if df[col].dtype in ['int64', 'float64']:
                min_val = df[col].min()
                max_val = df[col].max()
                mean_val = df[col].mean()
                summary += f"- {col} ({dtype}): {unique_count} unique values, {missing_count} missing\n"
                summary += f"  Range: {min_val} to {max_val}, Mean: {mean_val:.2f}\n"
            else:
                summary += f"- {col} ({dtype}): {unique_count} unique values, {missing_count} missing\n"
                # Show sample values for categorical columns
                sample_values = df[col].value_counts().head(5).to_dict()
                summary += f"  Sample values: {sample_values}\n"
        
        summary += f"\nMissing Values Summary:\n{df.isnull().sum().to_string()}\n"
        
        # Add sample data
        summary += f"\nFirst 3 rows:\n{df.head(3).to_string()}\n"
        
        # Add column descriptions based on common patterns
        summary += "\nColumn Descriptions:\n"
        for col in df.columns:
            if 'salary' in col.lower() or 'income' in col.lower():
                summary += f"- {col}: Contains salary/income information\n"
            elif 'name' in col.lower():
                summary += f"- {col}: Contains name information\n"
            elif 'id' in col.lower():
                summary += f"- {col}: Contains ID/identifier information\n"
            elif 'date' in col.lower():
                summary += f"- {col}: Contains date information\n"
            elif 'email' in col.lower():
                summary += f"- {col}: Contains email addresses\n"
            elif 'phone' in col.lower():
                summary += f"- {col}: Contains phone numbers\n"
            else:
                summary += f"- {col}: Data column\n"
        
        return summary
    
    def _clean_generated_code(self, code: str) -> str:
        """Clean and format the generated code."""
        # Remove markdown code blocks if present
        if "```python" in code:
            start = code.find("```python") + 9
            end = code.find("```", start)
            if end != -1:
                code = code[start:end].strip()
        elif "```" in code:
            start = code.find("```") + 3
            end = code.find("```", start)
            if end != -1:
                code = code[start:end].strip()
        
        # Add basic info if not present
        if "print(f\"Dataset:" not in code:
            code = f"""
# Basic dataset info
print(f"Dataset: {{df.shape[0]}} rows, {{df.shape[1]}} columns")
print(f"Columns: {{list(df.columns)}}")
print()

{code}
"""
        
        return code
    

    
    def _execute_analysis_code(self, code: str, df: pd.DataFrame) -> str:
        """Execute the generated analysis code and return the result."""
        try:
            # Create artifacts folder
            artifacts_dir = "artifacts"
            os.makedirs(artifacts_dir, exist_ok=True)
            
            # Capture stdout to get the output
            import io
            import sys
            
            # Redirect stdout to capture output
            old_stdout = sys.stdout
            new_stdout = io.StringIO()
            sys.stdout = new_stdout
            
            # Create execution environment with artifacts directory
            local_vars = {
                'df': df,
                'pd': pd,
                'np': np,
                'plt': plt,
                'sns': sns,
                'px': px,
                'go': go,
                'artifacts_dir': artifacts_dir
            }
            
            # Execute the code
            exec(code, {}, local_vars)
            
            # Get the output
            output = new_stdout.getvalue()
            
            # Restore stdout
            sys.stdout = old_stdout
            
            return output
            
        except Exception as e:
            return f"Error executing analysis: {str(e)}"
    
    def run_code(self, code: str) -> str:
        """Run custom Python code on the CSV data."""
        if not self.current_csv_file:
            return "No CSV file loaded. Please download a CSV file first."
        
        try:
            df = pd.read_csv(self.current_csv_file)
            
            # Create a safe execution environment
            local_vars = {
                'df': df,
                'pd': pd,
                'plt': plt,
                'sns': sns,
                'px': px,
                'go': go,
                'np': np,
                'requests': requests,
                'json': json,
                'datetime': datetime,
                'tempfile': tempfile
            }
            
            # Execute the code
            exec(code, {}, local_vars)
            
            return "Code executed successfully."
            
        except Exception as e:
            return f"Error executing code: {str(e)}"
    
    def chat(self, message: str) -> str:
        """Chat interface for the agent."""
        try:
            # Check if it's a download request
            if "download" in message.lower() and "http" in message:
                # Extract URL
                words = message.split()
                url = next((word for word in words if word.startswith("http")), None)
                if url:
                    return self.download_csv(url)
                else:
                    return "Please provide a valid URL for downloading CSV."
            
            # Check if it's a load request
            elif "load" in message.lower() and ("csv" in message.lower() or "file" in message.lower()):
                return self.load_existing_csv(message)
            
            # Check if it's a list request
            elif "list" in message.lower() and ("csv" in message.lower() or "files" in message.lower()):
                return self.list_available_csv_files()
            
            # Check if it's a code execution request
            elif "```python" in message:
                # Extract code
                code_start = message.find("```python") + 9
                code_end = message.find("```", code_start)
                if code_start > 8 and code_end > code_start:
                    code = message[code_start:code_end].strip()
                    return self.run_code(code)
                else:
                    return "Please provide valid Python code in ```python blocks."
            
            # Otherwise, treat as analysis request
            else:
                return self.analyze_data(message)
                
        except Exception as e:
            return f"Error: {str(e)}"

# Example usage
if __name__ == "__main__":
    # Initialize the agent
    agent = AdvancedQnAAgent()
    
    # Example conversation
    queries = [
        "Download a CSV file from https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv",
        "Show me a summary of the data",
        "Create a visualization of the data",
        "Run this code: ```python\nimport pandas as pd\nprint(df.head())\nprint(df.describe())\n```"
    ]
    
    for query in queries:
        print(f"\nUser: {query}")
        response = agent.chat(query)
        print(f"Agent: {response}") 