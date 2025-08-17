# LLM Prompts

This directory contains all the LLM prompt templates used by the QnA agent system.

## Prompt Files

### `analysis_code_generation.txt`
Template for generating Python analysis code based on user queries and available datasets.

**Variables:**
- `{context_summary}` - Summary of available datasets and their structure
- `{dataframe_names}` - List of dataframe variable names available in memory

### `conversational_response.txt`
Template for generating conversational responses that explain analysis results in simple terms.

**Variables:**
- `{context_summary}` - Summary of available datasets

### `execution_history_context.txt`
Template for providing context about previous execution attempts when retrying failed code.

**Variables:**
- `{attempt_count}` - Number of execution attempts made
- `{execution_history}` - Formatted history of previous attempts

### `conversational_query_context.txt`
Template for providing context about the user's query and analysis results to the conversational response generator.

**Variables:**
- `{query}` - User's original query
- `{analysis_result}` - Raw analysis result to be explained

## Usage

Prompts are loaded and formatted using the `PromptManager` class in `backend/utils/prompt_manager.py`:

```python
from backend.utils.prompt_manager import PromptManager

pm = PromptManager()

# Load a raw prompt
raw_prompt = pm.load_prompt('analysis_code_generation')

# Format a prompt with variables
formatted_prompt = pm.format_prompt(
    'analysis_code_generation',
    context_summary="...",
    dataframe_names=["df1", "df2"]
)

# Use convenience methods
analysis_prompt = pm.get_analysis_code_prompt(
    context_summary="...",
    dataframe_names=["df1", "df2"]
)
```

## Best Practices

1. **Keep prompts focused**: Each prompt should have a single, clear purpose
2. **Use descriptive variable names**: Make it clear what each `{variable}` represents
3. **Document variables**: Update this README when adding new variables
4. **Test prompts**: Verify that prompts work correctly with the PromptManager
5. **Version control**: Track changes to prompts as they affect system behavior

## Adding New Prompts

1. Create a new `.txt` file in this directory
2. Use `{variable_name}` syntax for dynamic content
3. Update this README with the new prompt's purpose and variables
4. Add convenience methods to `PromptManager` if needed
5. Test the prompt with the system
