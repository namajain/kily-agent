#!/usr/bin/env python3
"""
Prompt Manager for loading and formatting LLM prompts from files
"""
import os
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class PromptManager:
    """Manages loading and formatting of LLM prompts from files"""
    
    def __init__(self, prompts_dir: str = "prompts"):
        """
        Initialize PromptManager
        
        Args:
            prompts_dir: Directory containing prompt template files
        """
        self.prompts_dir = prompts_dir
        self._prompt_cache = {}
        
    def load_prompt(self, prompt_name: str) -> str:
        """
        Load a prompt template from file
        
        Args:
            prompt_name: Name of the prompt file (without extension)
            
        Returns:
            Prompt template content
        """
        if prompt_name in self._prompt_cache:
            return self._prompt_cache[prompt_name]
        
        prompt_file = os.path.join(self.prompts_dir, f"{prompt_name}.txt")
        
        try:
            with open(prompt_file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                self._prompt_cache[prompt_name] = content
                logger.debug(f"Loaded prompt: {prompt_name}")
                return content
        except FileNotFoundError:
            logger.error(f"Prompt file not found: {prompt_file}")
            raise FileNotFoundError(f"Prompt file not found: {prompt_file}")
        except Exception as e:
            logger.error(f"Error loading prompt {prompt_name}: {e}")
            raise
    
    def format_prompt(self, prompt_name: str, **kwargs) -> str:
        """
        Load and format a prompt template with provided variables
        
        Args:
            prompt_name: Name of the prompt file (without extension)
            **kwargs: Variables to format into the prompt template
            
        Returns:
            Formatted prompt content
        """
        template = self.load_prompt(prompt_name)
        
        try:
            formatted = template.format(**kwargs)
            return formatted
        except KeyError as e:
            logger.error(f"Missing required variable in prompt {prompt_name}: {e}")
            raise KeyError(f"Missing required variable in prompt {prompt_name}: {e}")
        except Exception as e:
            logger.error(f"Error formatting prompt {prompt_name}: {e}")
            raise
    
    def get_analysis_code_prompt(self, context_summary: str, dataframe_names: list) -> str:
        """
        Get formatted analysis code generation prompt
        
        Args:
            context_summary: Summary of available datasets
            dataframe_names: List of dataframe variable names
            
        Returns:
            Formatted analysis code prompt
        """
        return self.format_prompt(
            "analysis_code_generation",
            context_summary=context_summary,
            dataframe_names=dataframe_names
        )
    
    def get_conversational_response_prompt(self, context_summary: str) -> str:
        """
        Get formatted conversational response prompt
        
        Args:
            context_summary: Summary of available datasets
            
        Returns:
            Formatted conversational response prompt
        """
        return self.format_prompt(
            "conversational_response",
            context_summary=context_summary
        )
    
    def get_execution_history_context(self, attempt_count: int, execution_history: str) -> str:
        """
        Get formatted execution history context
        
        Args:
            attempt_count: Number of execution attempts
            execution_history: Formatted execution history
            
        Returns:
            Formatted execution history context
        """
        return self.format_prompt(
            "execution_history_context",
            attempt_count=attempt_count,
            execution_history=execution_history
        )
    
    def get_conversational_query_context(self, query: str, analysis_result: str) -> str:
        """
        Get formatted conversational query context
        
        Args:
            query: User's original query
            analysis_result: Analysis result to explain
            
        Returns:
            Formatted conversational query context
        """
        return self.format_prompt(
            "conversational_query_context",
            query=query,
            analysis_result=analysis_result
        )
