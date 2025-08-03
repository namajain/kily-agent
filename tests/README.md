# QnA Agent Tests

This directory contains all test files and example scripts for the QnA Agent.

## Test Files

### Core Tests
- **`test_agent.py`** - Basic agent functionality tests
- **`test_llm_analysis.py`** - LLM-powered analysis demonstration
- **`test_load_functionality.py`** - File loading functionality tests

### Example Scripts
- **`demo.py`** - Interactive demo script for testing the agent
- **`example_usage.py`** - Programmatic usage examples

### Test Runner
- **`run_tests.py`** - Comprehensive test runner that can execute all tests or specific files

## Running Tests

### Run All Tests
```bash
uv run python tests/run_tests.py
```

### Run Specific Test
```bash
uv run python tests/run_tests.py test_agent.py
```

### List Available Tests
```bash
uv run python tests/run_tests.py --list
```

### Run Individual Files
```bash
# Interactive demo
uv run python tests/demo.py

# Example usage
uv run python tests/example_usage.py

# Specific tests
uv run python tests/test_agent.py
uv run python tests/test_llm_analysis.py
uv run python tests/test_load_functionality.py
```

## Test Structure

### Test Configuration
- **`conftest.py`** - Pytest configuration and shared fixtures
- **`__init__.py`** - Package initialization

### Fixtures Available
- `agent` - Fresh agent instance for each test
- `sample_csv_path` - Path to sample CSV file
- `artifacts_dir` - Path to artifacts directory
- `downloads_dir` - Path to downloads directory

## Test Categories

### Unit Tests
Tests for individual components and methods:
- Agent initialization
- CSV download functionality
- File loading operations
- Code generation and execution

### Integration Tests
Tests for complete workflows:
- End-to-end analysis workflows
- LLM-powered code generation
- File management operations

### Example Scripts
Demonstration scripts showing how to use the agent:
- Interactive chat interface
- Programmatic API usage
- Real-world usage scenarios

## Adding New Tests

1. Create a new test file in this directory
2. Import the agent: `from advanced_qna_agent import AdvancedQnAAgent`
3. Use the available fixtures if needed
4. Add the test file to the list in `run_tests.py`

## Test Environment

Tests run in the same environment as the main application:
- All dependencies are available
- Environment variables are loaded from `.env`
- File operations use the same directories (`downloads/`, `artifacts/`)

## Continuous Integration

The test runner is designed to work with CI/CD systems:
- Returns appropriate exit codes (0 for success, 1 for failure)
- Provides clear output for test results
- Can be run in headless environments 