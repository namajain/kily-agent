"""
QnA Agent for MVP - Handles natural language analysis with profile context
"""
import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List, Optional
import logging
from datetime import datetime
import tempfile
import re
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from ..utils.prompt_manager import PromptManager

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class QnAAgent:
    """
    Enhanced QnA agent that works with profile context and real-time analysis.
    """
    
    def __init__(self, context_manager, llm_model: str = "gpt-4o-mini"):
        self.context_manager = context_manager
        self.llm = ChatOpenAI(
            model=llm_model,
            temperature=0,
            api_key=os.getenv("OPENAI_API_KEY")
        )
        self.artifacts_dir = "artifacts"
        self._ensure_artifacts_directory()
        
        # Initialize prompt manager
        self.prompt_manager = PromptManager()
    
    def _ensure_artifacts_directory(self):
        """Ensure artifacts directory exists"""
        os.makedirs(self.artifacts_dir, exist_ok=True)
    
    def analyze_with_context(self, query: str, context_data: Dict[str, pd.DataFrame], chat_history: List[Dict] = None) -> str:
        """
        Analyze data using profile context and loaded dataframes.
        
        Args:
            query: User's question
            context_data: Available dataframes
            chat_history: List of previous messages in format [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]
        """
        try:
            logger.info(f"Starting analysis for query: {query}")
            
            if not context_data:
                return "No context data available for analysis."
            
            # Generate analysis code
            analysis_code = self._generate_analysis_code(query, context_data, chat_history)
            
            # Execute analysis
            result = self._execute_analysis(analysis_code, context_data)
            
            # Generate conversational response
            conversational_response = self._generate_conversational_response(query, result, context_data, chat_history)
            
            logger.info("Analysis completed successfully")
            return conversational_response
            
        except Exception as e:
            logger.error(f"Analysis failed: {e}")
            return f"Analysis failed: {str(e)}"
    
    def _generate_analysis_code(self, query: str, context_data: Dict[str, pd.DataFrame], chat_history: List[Dict] = None, execution_history: List[Dict] = None) -> str:
        """Generate Python code for analysis based on query and available data"""
        try:
            # Create context summary
            context_summary = self._create_context_summary(context_data)
            
            # Get dataframe names for the prompt
            dataframe_names = [filename.replace('.csv', '_df') for filename in context_data.keys()]
            
            # Get system prompt from prompt manager
            system_prompt = self.prompt_manager.get_analysis_code_prompt(
                context_summary=context_summary,
                dataframe_names=dataframe_names
            )
            
            # Build messages list with chat history and execution history
            messages = [SystemMessage(content=system_prompt)]
            
            # Add execution history if available
            if execution_history:
                # Format execution history
                history_text = ""
                for i, attempt in enumerate(execution_history[-3:], 1):  # Keep last 3 attempts
                    history_text += f"""
                Attempt {attempt['iteration']}:
                Code: {attempt['code'][:200]}...
                Result: {attempt['result'][:200]}...
                Status: {attempt['status']}
                """
                
                history_context = self.prompt_manager.get_execution_history_context(
                    attempt_count=len(execution_history),
                    execution_history=history_text
                )
                messages.append(HumanMessage(content=history_context))
            
            # Add chat history if available
            if chat_history:
                for message in chat_history[-6:]:  # Keep last 6 messages for context
                    if message.get('role') == 'user':
                        messages.append(HumanMessage(content=message.get('content', '')))
                    elif message.get('role') == 'assistant':
                        messages.append(AIMessage(content=message.get('content', '')))
            
            # Add current query
            messages.append(HumanMessage(content=query))
            
            # Generate code using LLM
            response = self.llm.invoke(messages)
            
            code = self._extract_code(response.content)
            logger.info(f"Generated code: {code}")
            
            return code
            
        except Exception as e:
            logger.error(f"Failed to generate analysis code: {e}")
            raise
    
    def _create_context_summary(self, context_data: Dict[str, pd.DataFrame]) -> str:
        """Create a summary of available context data"""
        summary = []
        
        for filename, df in context_data.items():
            df_summary = f"""
            Variable name: {filename}
            Dataset: {filename}
            - Shape: {df.shape[0]} rows, {df.shape[1]} columns
            - Columns: {list(df.columns)}
            - Data types: {dict(df.dtypes)}
            - Sample data:
            {df.head(3).to_string()}
            """
            summary.append(df_summary)
        
        return "\n".join(summary)
    
    def _extract_code(self, content: str) -> str:
        """Extract Python code from LLM response"""
        # Look for code blocks
        code_pattern = r'```python\s*(.*?)\s*```'
        matches = re.findall(code_pattern, content, re.DOTALL)
        
        if matches:
            return matches[0].strip()
        
        # If no code blocks, try to extract code lines
        lines = content.split('\n')
        code_lines = []
        in_code = False
        
        for line in lines:
            if line.strip().startswith('import ') or line.strip().startswith('from '):
                in_code = True
            elif in_code and (line.strip().startswith('#') or line.strip() == '' or line.strip().startswith('print')):
                code_lines.append(line)
            elif in_code and line.strip():
                code_lines.append(line)
            elif in_code and not line.strip():
                break
        
        return '\n'.join(code_lines)
    
    def _execute_analysis(self, code: str, context_data: Dict[str, pd.DataFrame]) -> str:
        """Execute analysis code safely with context data available"""
        try:
            # Create safe execution environment with clean variable names
            local_vars = {
                'pd': pd,
                'np': np,
                'plt': plt,
                'sns': sns,
                'px': px,
                'go': go,
                'artifacts_dir': self.artifacts_dir,
            }
            
            # Add dataframes with clean variable names
            for filename, df in context_data.items():
                # Create clean variable name (remove .csv extension and replace with underscore)
                clean_name = filename.replace('.csv', '_df')
                local_vars[clean_name] = df
                logger.info(f"Added dataframe: {clean_name} = {filename}")
            
            logger.info(f"Available variables: {list(local_vars.keys())}")
            logger.info(f"Context data keys: {list(context_data.keys())}")
            
            # Capture output
            output_buffer = []
            
            def custom_print(*args, **kwargs):
                output_buffer.append(' '.join(str(arg) for arg in args))
            
            local_vars['print'] = custom_print
            
            # Execute code
            exec(code, {}, local_vars)
            
            # Save any plots that were created
            self._save_plots()
            
            # Return captured output
            result = '\n'.join(output_buffer)
            
            if not result.strip():
                result = "Analysis completed. Check the artifacts directory for any generated visualizations."
            
            return result
            
        except Exception as e:
            logger.error(f"Code execution failed: {e}")
            raise
    
    def _save_plots(self):
        """Save any plots that were created during analysis"""
        try:
            # Save matplotlib plots
            if plt.get_fignums():
                for fig_num in plt.get_fignums():
                    fig = plt.figure(fig_num)
                    filename = f"analysis_plot_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{fig_num}.png"
                    filepath = os.path.join(self.artifacts_dir, filename)
                    fig.savefig(filepath, dpi=300, bbox_inches='tight')
                    plt.close(fig)
                    logger.info(f"Saved plot: {filepath}")
            
        except Exception as e:
            logger.error(f"Failed to save plots: {e}")
    
    def get_basic_summary(self, context_data: Dict[str, pd.DataFrame]) -> str:
        """Generate a basic summary of the context data"""
        try:
            summary = []
            
            for filename, df in context_data.items():
                df_summary = f"""
                **{filename}**
                - Rows: {df.shape[0]:,}
                - Columns: {df.shape[1]}
                - Memory usage: {df.memory_usage(deep=True).sum() / 1024:.2f} KB
                
                **Columns:**
                {', '.join(df.columns)}
                
                **Data Types:**
                {df.dtypes.to_string()}
                
                **Missing Values:**
                {df.isnull().sum().to_string()}
                
                **Sample Data:**
                {df.head(3).to_string()}
                """
                summary.append(df_summary)
            
            return "\n".join(summary)
            
        except Exception as e:
            logger.error(f"Failed to generate basic summary: {e}")
            return f"Failed to generate summary: {str(e)}"
    
    def run_custom_code(self, code: str, context_data: Dict[str, pd.DataFrame]) -> str:
        """Run custom Python code with context data"""
        try:
            return self._execute_analysis(code, context_data)
        except Exception as e:
            logger.error(f"Custom code execution failed: {e}")
            return f"Code execution failed: {str(e)}"
    
    def get_available_datasets(self, context_data: Dict[str, pd.DataFrame]) -> List[Dict]:
        """Get information about available datasets"""
        datasets = []
        
        for filename, df in context_data.items():
            dataset_info = {
                'filename': filename,
                'rows': df.shape[0],
                'columns': df.shape[1],
                'column_names': list(df.columns),
                'data_types': dict(df.dtypes),
                'missing_values': dict(df.isnull().sum()),
                'memory_usage_kb': df.memory_usage(deep=True).sum() / 1024
            }
            datasets.append(dataset_info)
        
        return datasets
    
    def validate_query(self, query: str) -> bool:
        """Basic query validation"""
        if not query or not query.strip():
            return False
        
        # Check for potentially dangerous keywords
        dangerous_keywords = ['exec', 'eval', 'import', 'open', 'file', 'system', 'subprocess']
        query_lower = query.lower()
        
        for keyword in dangerous_keywords:
            if keyword in query_lower:
                logger.warning(f"Query contains potentially dangerous keyword: {keyword}")
                return False
        
        return True
    
    def _generate_conversational_response(self, query: str, analysis_result: str, context_data: Dict[str, pd.DataFrame], chat_history: List[Dict] = None) -> str:
        """Generate a conversational response based on the analysis result"""
        try:
            # Create context summary for the LLM
            context_summary = self._create_context_summary(context_data)
            
            # Get system prompt from prompt manager
            system_prompt = self.prompt_manager.get_conversational_response_prompt(
                context_summary=context_summary
            )
            
            # Build messages list with chat history
            messages = [SystemMessage(content=system_prompt)]
            
            # Add chat history if available (keep last 4 messages for context)
            if chat_history:
                for message in chat_history[-4:]:
                    if message.get('role') == 'user':
                        messages.append(HumanMessage(content=message.get('content', '')))
                    elif message.get('role') == 'assistant':
                        messages.append(AIMessage(content=message.get('content', '')))
            
            # Add current query and analysis result
            current_prompt = self.prompt_manager.get_conversational_query_context(
                query=query,
                analysis_result=analysis_result
            )
            messages.append(HumanMessage(content=current_prompt))
            
            # Generate conversational response using LLM
            response = self.llm.invoke(messages)
            
            return response.content.strip()
            
        except Exception as e:
            logger.error(f"Failed to generate conversational response: {e}")
            # Fallback to original result if conversational generation fails
            return f"Here's what I found:\n\n{analysis_result}"
    
    def _execute_analysis_iterative(self, query: str, context_data: Dict[str, pd.DataFrame], chat_history: List[Dict] = None) -> str:
        """Execute analysis with iterative refinement up to 5 attempts"""
        max_iterations = 5
        iteration = 0
        execution_history = []
        
        while iteration < max_iterations:
            iteration += 1
            logger.info(f"Starting iteration {iteration}/{max_iterations}")
            
            try:
                # Generate analysis code
                analysis_code = self._generate_analysis_code(query, context_data, chat_history, execution_history)
                
                # Execute the code
                result = self._execute_analysis(analysis_code, context_data)
                
                # Check if we have a complete answer
                is_complete = self._check_completion(query, result, execution_history)
                
                if is_complete:
                    logger.info(f"Analysis completed successfully in iteration {iteration}")
                    return result
                else:
                    logger.info(f"Iteration {iteration} incomplete, continuing...")
                    execution_history.append({
                        'iteration': iteration,
                        'code': analysis_code,
                        'result': result,
                        'status': 'incomplete'
                    })
                    
            except Exception as e:
                logger.warning(f"Error in iteration {iteration}: {e}")
                execution_history.append({
                    'iteration': iteration,
                    'code': analysis_code if 'analysis_code' in locals() else 'N/A',
                    'result': f"Error: {str(e)}",
                    'status': 'error'
                })
        
        # If we reach here, return the best result we have
        logger.warning(f"Reached maximum iterations ({max_iterations}), returning best available result")
        if execution_history:
            return execution_history[-1]['result']
        else:
            return "Analysis failed after maximum iterations"
    
    def _check_completion(self, query: str, result: str, execution_history: List[Dict]) -> bool:
        """Check if the analysis result is complete and answers the query"""
        try:
            # Create a simple prompt to check completion
            check_prompt = f"""
            You are an expert data analyst. Check if the following analysis result completely answers the user's query.
            
            User Query: {query}
            
            Analysis Result:
            {result}
            
            Execution History: {len(execution_history)} previous attempts
            
            Determine if this result:
            1. Provides a direct answer to the query
            2. Contains meaningful data/insights
            3. Is not just an error message
            4. Would satisfy the user's question
            
            Respond with ONLY "COMPLETE" or "INCOMPLETE" followed by a brief reason.
            """
            
            response = self.llm.invoke([
                SystemMessage(content="You are a completion checker. Respond with only 'COMPLETE' or 'INCOMPLETE' followed by a brief reason."),
                HumanMessage(content=check_prompt)
            ])
            
            response_text = response.content.strip().upper()
            logger.info(f"Completion check result: {response_text}")
            
            return response_text.startswith("COMPLETE")
            
        except Exception as e:
            logger.error(f"Error in completion check: {e}")
            # Default to incomplete if we can't check
            return False 