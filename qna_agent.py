import os
import json
import requests
import pandas as pd
import numpy as np
import io
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langchain.tools import tool
from langchain.schema import BaseMessage
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import tempfile

# Load environment variables
load_dotenv()

# Initialize OpenAI client
llm = ChatOpenAI(
    model="gpt-4",
    temperature=0,
    api_key=os.getenv("OPENAI_API_KEY")
)

# State definition
class AgentState:
    messages: List[BaseMessage]
    csv_data: Optional[pd.DataFrame] = None
    csv_filename: Optional[str] = None
    analysis_results: Optional[str] = None
    error: Optional[str] = None

# Tools
@tool
def download_csv_from_url(url: str) -> str:
    """Download a CSV file from a URL and return the filename."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        # Create a temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write(response.text)
            filename = f.name
        
        return f"CSV file downloaded successfully to {filename}"
    except Exception as e:
        return f"Error downloading CSV: {str(e)}"

@tool
def load_csv_data(filename: str) -> str:
    """Load CSV data into memory for analysis."""
    try:
        df = pd.read_csv(filename)
        return f"CSV loaded successfully. Shape: {df.shape}. Columns: {list(df.columns)}"
    except Exception as e:
        return f"Error loading CSV: {str(e)}"

@tool
def analyze_csv_data(query: str, filename: str) -> str:
    """Analyze CSV data using pandas and generate insights based on the query."""
    try:
        df = pd.read_csv(filename)
        
        # Basic data info
        info = f"Dataset shape: {df.shape}\n"
        info += f"Columns: {list(df.columns)}\n"
        info += f"Data types:\n{df.dtypes}\n"
        info += f"Missing values:\n{df.isnull().sum()}\n"
        
        # Generate analysis based on query
        analysis = ""
        
        if "summary" in query.lower() or "describe" in query.lower():
            analysis += f"\nSummary statistics:\n{df.describe()}\n"
        
        if "correlation" in query.lower():
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 1:
                corr_matrix = df[numeric_cols].corr()
                analysis += f"\nCorrelation matrix:\n{corr_matrix}\n"
        
        if "plot" in query.lower() or "visualize" in query.lower():
            # Create a simple visualization
            plt.figure(figsize=(10, 6))
            if len(df.select_dtypes(include=[np.number]).columns) > 0:
                df.select_dtypes(include=[np.number]).hist(figsize=(12, 8))
                plt.tight_layout()
                plot_filename = f"analysis_plot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                plt.savefig(plot_filename)
                plt.close()
                analysis += f"\nPlot saved as: {plot_filename}\n"
        
        if "head" in query.lower():
            analysis += f"\nFirst 5 rows:\n{df.head()}\n"
        
        if "tail" in query.lower():
            analysis += f"\nLast 5 rows:\n{df.tail()}\n"
        
        return info + analysis
        
    except Exception as e:
        return f"Error analyzing CSV data: {str(e)}"

@tool
def execute_custom_analysis(code: str, filename: str) -> str:
    """Execute custom Python code for CSV analysis."""
    try:
        # Create a safe execution environment
        df = pd.read_csv(filename)
        
        # Execute the code with df available
        local_vars = {'df': df, 'pd': pd, 'plt': plt, 'sns': sns, 'px': px, 'go': go}
        
        exec(code, {}, local_vars)
        
        return "Custom analysis executed successfully."
        
    except Exception as e:
        return f"Error executing custom analysis: {str(e)}"

# Create the graph
def create_agent():
    # Define the graph
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("download_csv", download_csv_from_url)
    workflow.add_node("load_csv", load_csv_data)
    workflow.add_node("analyze_csv", analyze_csv_data)
    workflow.add_node("custom_analysis", execute_custom_analysis)
    
    # Add edges
    workflow.add_edge("download_csv", "load_csv")
    workflow.add_edge("load_csv", "analyze_csv")
    workflow.add_edge("analyze_csv", END)
    workflow.add_edge("custom_analysis", END)
    
    # Compile the graph
    app = workflow.compile()
    
    return app

# Main agent class
class QnAAgent:
    def __init__(self):
        self.app = create_agent()
        self.current_csv_file = None
    
    def process_query(self, query: str, csv_url: str = None) -> str:
        """Process a query about CSV data."""
        try:
            if csv_url:
                # Download and analyze CSV
                result = self.app.invoke({
                    "messages": [HumanMessage(content=query)],
                    "csv_url": csv_url
                })
            else:
                # Use existing CSV file
                if not self.current_csv_file:
                    return "No CSV file available. Please provide a CSV URL first."
                
                result = self.app.invoke({
                    "messages": [HumanMessage(content=query)],
                    "csv_filename": self.current_csv_file
                })
            
            return result.get("analysis_results", "Analysis completed.")
            
        except Exception as e:
            return f"Error processing query: {str(e)}"
    
    def download_csv(self, url: str) -> str:
        """Download a CSV file from URL."""
        try:
            response = requests.get(url)
            response.raise_for_status()
            
            # Save to temporary file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
                f.write(response.text)
                self.current_csv_file = f.name
            
            return f"CSV downloaded successfully to {self.current_csv_file}"
            
        except Exception as e:
            return f"Error downloading CSV: {str(e)}"
    
    def analyze_data(self, query: str) -> str:
        """Analyze the current CSV data."""
        if not self.current_csv_file:
            return "No CSV file loaded. Please download a CSV file first."
        
        try:
            df = pd.read_csv(self.current_csv_file)
            
            # Basic analysis
            analysis = f"Dataset: {df.shape[0]} rows, {df.shape[1]} columns\n"
            analysis += f"Columns: {list(df.columns)}\n\n"
            
            # Answer specific questions
            if "summary" in query.lower():
                analysis += f"Summary statistics:\n{df.describe()}\n"
            
            if "missing" in query.lower():
                analysis += f"Missing values:\n{df.isnull().sum()}\n"
            
            if "types" in query.lower():
                analysis += f"Data types:\n{df.dtypes}\n"
            
            return analysis
            
        except Exception as e:
            return f"Error analyzing data: {str(e)}"

# Example usage
if __name__ == "__main__":
    # Initialize the agent
    agent = QnAAgent()
    
    # Example: Download and analyze a CSV file
    csv_url = "https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv"
    
    print("Downloading CSV file...")
    result = agent.download_csv(csv_url)
    print(result)
    
    print("\nAnalyzing data...")
    analysis = agent.analyze_data("Show me a summary of the data")
    print(analysis) 