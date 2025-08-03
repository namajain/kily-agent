#!/usr/bin/env python3
"""
Test script to demonstrate LLM-based analysis code generation.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import tempfile
import io
import sys

def create_dataset_summary(df: pd.DataFrame) -> str:
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

def execute_analysis_code(code: str, df: pd.DataFrame) -> str:
    """Execute the generated analysis code and return the result."""
    try:
        # Capture stdout to get the output
        old_stdout = sys.stdout
        new_stdout = io.StringIO()
        sys.stdout = new_stdout
        
        # Create execution environment
        local_vars = {
            'df': df,
            'pd': pd,
            'np': np,
            'plt': plt,
            'sns': sns,
            'px': px,
            'go': go
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

def main():
    """Demonstrate LLM-based analysis with mock generated code."""
    
    # Load the employees data
    df = pd.read_csv('downloads/employees.csv')
    
    # Create dataset summary
    dataset_summary = create_dataset_summary(df)
    
    print("=" * 60)
    print("LLM-BASED ANALYSIS DEMONSTRATION")
    print("=" * 60)
    
    # Example 1: Salary analysis
    print("\n1. Query: 'which employee has the highest salary and what is their job title?'")
    print("-" * 60)
    
    # Mock LLM-generated code for salary analysis
    mock_code_1 = """
# Find employee with highest salary and their job title
max_salary = df['SALARY'].max()
highest_salary_employee = df[df['SALARY'] == max_salary]

print(f"Highest salary: ${max_salary:,.2f}")
print("\\nEmployee with highest salary:")
print(highest_salary_employee[['FIRST_NAME', 'LAST_NAME', 'SALARY', 'JOB_ID']].to_string(index=False))

# Show job title details
print(f"\\nJob title: {highest_salary_employee['JOB_ID'].iloc[0]}")
"""
    
    print("Generated code:")
    print(mock_code_1)
    print("\nExecution result:")
    print(execute_analysis_code(mock_code_1, df))
    
    # Example 2: Department analysis
    print("\n2. Query: 'show me the distribution of employees by department'")
    print("-" * 60)
    
    # Mock LLM-generated code for department analysis
    mock_code_2 = """
# Department distribution analysis
dept_counts = df['DEPARTMENT_ID'].value_counts().sort_index()

print("Employees by Department:")
print("=" * 30)
for dept_id, count in dept_counts.items():
    print(f"Department {dept_id}: {count} employees")

print(f"\\nTotal departments: {len(dept_counts)}")
print(f"Total employees: {len(df)}")

# Create a visualization
plt.figure(figsize=(10, 6))
dept_counts.plot(kind='bar')
plt.title('Employees by Department')
plt.xlabel('Department ID')
plt.ylabel('Number of Employees')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('department_distribution.png')
plt.close()
print("\\nDepartment distribution plot saved as 'department_distribution.png'")
"""
    
    print("Generated code:")
    print(mock_code_2)
    print("\nExecution result:")
    print(execute_analysis_code(mock_code_2, df))
    
    # Example 3: Salary statistics
    print("\n3. Query: 'what are the salary statistics and create a histogram'")
    print("-" * 60)
    
    # Mock LLM-generated code for salary statistics
    mock_code_3 = """
# Salary statistics and visualization
print("Salary Statistics:")
print("=" * 20)
print(f"Count: {df['SALARY'].count()}")
print(f"Mean: ${df['SALARY'].mean():,.2f}")
print(f"Median: ${df['SALARY'].median():,.2f}")
print(f"Standard Deviation: ${df['SALARY'].std():,.2f}")
print(f"Minimum: ${df['SALARY'].min():,.2f}")
print(f"Maximum: ${df['SALARY'].max():,.2f}")

# Create salary histogram
plt.figure(figsize=(10, 6))
plt.hist(df['SALARY'], bins=15, edgecolor='black', alpha=0.7)
plt.title('Salary Distribution')
plt.xlabel('Salary ($)')
plt.ylabel('Number of Employees')
plt.grid(True, alpha=0.3)
plt.savefig('salary_histogram.png')
plt.close()
print("\\nSalary histogram saved as 'salary_histogram.png'")
"""
    
    print("Generated code:")
    print(mock_code_3)
    print("\nExecution result:")
    print(execute_analysis_code(mock_code_3, df))
    
    print("\n" + "=" * 60)
    print("DEMONSTRATION COMPLETE")
    print("=" * 60)
    print("\nThis shows how the LLM would generate code based on:")
    print("1. Dataset summary (columns, data types, sample data)")
    print("2. Natural language query")
    print("3. Available packages (pandas, numpy, matplotlib, etc.)")
    print("\nThe generated code is then executed to provide the answer.")

if __name__ == "__main__":
    main() 