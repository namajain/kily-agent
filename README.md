# QnA Agent with CSV Download & Code Interpreter

A powerful QnA agent built with LangGraph that can download CSV files via API calls and run code interpreter to answer questions about the data.

## Features

- 🔗 **CSV Download**: Download CSV files from URLs via API calls
- 🤖 **LLM-Powered Analysis**: Uses GPT-4 to generate Python code based on natural language queries
- 📊 **Dynamic Code Generation**: Creates analysis code on-the-fly using dataset summary and available packages
- 💻 **Code Interpreter**: Execute custom Python code for advanced data analysis
- 📈 **Visualization**: Generate plots and charts using matplotlib, seaborn, and plotly
- 🔄 **Interactive Chat**: Real-time conversation interface

## Installation

### Using uv (Recommended)

1. **Install uv** (if not already installed):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd kily-agent
   ```

3. **Install dependencies with uv**:
   ```bash
   uv sync
   ```

4. **Set up environment variables**:
   Create a `.env` file in the project root:
   ```bash
   # .env
   OPENAI_API_KEY=your-openai-api-key-here
   ```

### Using pip (Alternative)

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd kily-agent
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   Create a `.env` file in the project root:
   ```bash
   # .env
   OPENAI_API_KEY=your-openai-api-key-here
   ```

## Usage

### Web Interface (Recommended)

Launch the Streamlit web application:
```bash
# Using uv
uv run streamlit run app.py

# Or using pip
streamlit run app.py
```

The web interface will open at `http://localhost:8501` and provides:
- 📤 **File Upload**: Upload CSV files directly
- 🌐 **URL Download**: Download CSV files from URLs  
- 📂 **File Management**: Load existing files from the downloads folder
- 💬 **Natural Language Queries**: Ask questions about your data
- 📊 **Visual Results**: View generated visualizations and analysis results
- 📁 **Artifacts**: All generated plots and files are saved to the `artifacts/` folder

### Interactive Demo

Run the interactive demo:
```bash
# Using uv
uv run python demo.py

# Or using pip
python demo.py
```

### Programmatic Usage

```python
from advanced_qna_agent import AdvancedQnAAgent

# Initialize the agent
agent = AdvancedQnAAgent()

# Download and analyze a CSV file
response = agent.chat("Download https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv")
print(response)

# Ask questions about the data
response = agent.chat("Show me a summary of the data")
print(response)

# Run custom code
response = agent.chat("""
Run this code:
```python
import pandas as pd
print("Dataset shape:", df.shape)
print("Columns:", list(df.columns))
print(df.head())
```
""")
print(response)
```

### Running Tests

```bash
# Run all tests
uv run python tests/run_tests.py

# Run a specific test
uv run python tests/run_tests.py test_agent.py

# List all available tests
uv run python tests/run_tests.py --list

# Run individual test files
uv run python tests/demo.py
uv run python tests/example_usage.py
uv run python tests/test_agent.py
uv run python tests/test_llm_analysis.py
uv run python tests/test_load_functionality.py

# Or with pip
python tests/run_tests.py
python tests/demo.py
python tests/example_usage.py
```

## Available Commands

### Download CSV Files
- `download https://example.com/data.csv`
- `Download CSV from https://example.com/data.csv`

### Load Existing Files
- `load employees.csv` - Load a specific CSV file
- `load csv` - Load the most recent CSV file
- `list csv files` - List all available CSV files

**Note**: CSV files are automatically saved to the `downloads/` folder in the workspace.

### Data Analysis
- `Show me a summary`
- `Analyze the data`
- `What are the data types?`
- `Show missing values`
- `Create a correlation matrix`

### Visualization
- `Create a plot`
- `Visualize the data`
- `Generate charts`

### Code Interpreter
- `Run this code: ```python\nprint(df.head())\n````
- `Execute: ```python\nimport matplotlib.pyplot as plt\nplt.hist(df['column'])\nplt.show()\n````

## Architecture

The agent uses LLM-powered code generation with the following components:

### Core Components
- **Dataset Summary Generator**: Creates comprehensive dataset summaries for the LLM
- **LLM Code Generator**: Uses GPT-4 to generate Python analysis code
- **Code Executor**: Safely executes generated code with proper environment
- **CSV Downloader**: Downloads CSV files from URLs

### Workflow
1. **Download CSV**: Downloads CSV file from URL to `downloads/` folder
2. **Create Summary**: Generates comprehensive dataset summary (columns, data types, sample data)
3. **LLM Analysis**: Sends dataset summary + natural language query to GPT-4
4. **Code Generation**: LLM generates Python code to answer the query
5. **Code Execution**: Executes generated code with pandas, numpy, matplotlib, etc.
6. **Result Output**: Returns formatted analysis results

### Available Packages
- `pandas` (pd): Data manipulation and analysis
- `numpy` (np): Numerical computing
- `matplotlib.pyplot` (plt): Basic plotting
- `seaborn` (sns): Statistical plotting
- `plotly.express` (px): Interactive plotting
- `plotly.graph_objects` (go): Advanced plotting

## Example Workflows

### Basic Analysis
1. Download CSV from URL
2. Load data into memory
3. Generate summary statistics
4. Create visualizations

### Advanced Analysis
1. Download CSV from URL
2. Load data into memory
3. Execute custom Python code
4. Generate custom visualizations
5. Export results

## Project Structure

```
kily-agent/
├── advanced_qna_agent.py    # Main agent implementation
├── app.py                  # Streamlit web application
├── run_app.py              # Streamlit app launcher
├── requirements.txt        # Python dependencies
├── pyproject.toml         # Project configuration
├── uv.lock               # Lock file for uv
├── .env                  # Environment variables (create this)
├── downloads/            # Downloaded CSV files
├── artifacts/            # Generated plots and files
├── tests/                # Test suite
│   ├── __init__.py       # Test package initialization
│   ├── conftest.py       # Pytest configuration
│   ├── run_tests.py      # Test runner
│   ├── README.md         # Test documentation
│   ├── demo.py           # Interactive demo script
│   ├── example_usage.py  # Programmatic usage examples
│   ├── test_agent.py     # Basic agent tests
│   ├── test_llm_analysis.py # LLM analysis tests
│   └── test_load_functionality.py # File loading tests
└── README.md            # This file
```

## Dependencies

### Core Dependencies
- `langgraph`: Workflow management
- `langchain`: LLM integration
- `langchain-openai`: OpenAI integration
- `pandas`: Data manipulation
- `numpy`: Numerical computing
- `matplotlib`: Basic plotting
- `seaborn`: Statistical plotting
- `plotly`: Interactive plotting
- `requests`: HTTP requests
- `python-dotenv`: Environment management
- `streamlit`: Web application framework

### Development Dependencies
- `pytest`: Testing framework
- `black`: Code formatting
- `flake8`: Linting
- `mypy`: Type checking

### Package Management
This project uses `uv` for fast, reliable Python package management. The dependencies are defined in `pyproject.toml` and locked in `uv.lock`.

## Security Considerations

- The code interpreter runs in a controlled environment
- Only safe libraries are available in the execution context
- File operations are limited to temporary files
- Network requests are restricted to CSV downloads

## Error Handling

The agent includes comprehensive error handling for:
- Network errors during CSV download
- File format errors
- Code execution errors
- Memory issues with large datasets

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License. 