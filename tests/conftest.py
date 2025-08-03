"""
Pytest configuration for QnA Agent tests.

This file contains shared fixtures and configuration for all tests.
"""

import pytest
import os
import sys
from pathlib import Path

# Add the parent directory to the Python path so we can import the agent
sys.path.insert(0, str(Path(__file__).parent.parent))

@pytest.fixture
def agent():
    """Create a fresh agent instance for each test."""
    from advanced_qna_agent import AdvancedQnAAgent
    return AdvancedQnAAgent()

@pytest.fixture
def sample_csv_path():
    """Path to a sample CSV file for testing."""
    return Path(__file__).parent.parent / "downloads" / "employees.csv"

@pytest.fixture
def artifacts_dir():
    """Path to the artifacts directory."""
    artifacts_path = Path(__file__).parent.parent / "artifacts"
    artifacts_path.mkdir(exist_ok=True)
    return artifacts_path

@pytest.fixture
def downloads_dir():
    """Path to the downloads directory."""
    downloads_path = Path(__file__).parent.parent / "downloads"
    downloads_path.mkdir(exist_ok=True)
    return downloads_path 