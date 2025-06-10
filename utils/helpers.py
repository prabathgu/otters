import os
import importlib
from typing import List

def load_tools() -> List:
    """
    Dynamically loads all tools from the tools directory.
    Returns a list of all available tools with complete parameter specifications.
    """
    all_tools = {}
    tools_dir = 'tools'
    for filename in sorted(os.listdir(tools_dir)):
        if filename.endswith('.py') and not filename.startswith('__'):
            module_name = f'tools.{filename[:-3]}'
            module = importlib.import_module(module_name)
            for attr_name in dir(module):
                if attr_name.endswith('_TOOLS'):
                    tool_dict = getattr(module, attr_name)
                    # Keep all properties of parameters as they are defined in the tool
                    all_tools.update(tool_dict)
    return list(all_tools.values())

def clean_claude_json(content: str) -> str:
    """
    Clean JSON content by removing markdown code block markers that Claude sometimes adds.
    Also handles cases where Claude includes explanatory text before the JSON.
    Handles cases like:
    "Some explanatory text\n\n```json\n{"result": {...}}\n```"
    "Some explanatory text\n\n{"result": {...}}"  (no code blocks)
    or 
    ```json
    {"result": {...}}
    ```
    or 
    ```
    {"result": {...}}
    ```
    """
    content = content.strip()
    
    # First try to find ```json block
    json_start_marker = '```json'
    json_end_marker = '```'
    
    json_start = content.find(json_start_marker)
    if json_start != -1:
        # Found ```json, extract content between markers
        content_after_start = content[json_start + len(json_start_marker):]
        json_end = content_after_start.find(json_end_marker)
        if json_end != -1:
            return content_after_start[:json_end].strip()
        else:
            # Found start marker but no end marker, take everything after start
            return content_after_start.strip()
    
    # If no ```json found, try to find generic ``` block
    generic_start_marker = '```'
    generic_start = content.find(generic_start_marker)
    if generic_start != -1:
        content_after_start = content[generic_start + len(generic_start_marker):]
        generic_end = content_after_start.find(generic_start_marker)
        if generic_end != -1:
            return content_after_start[:generic_end].strip()
        else:
            # Found start marker but no end marker, take everything after start
            return content_after_start.strip()
    
    # No code blocks found, look for raw JSON starting with {
    json_object_start = content.find('{')
    if json_object_start != -1:
        # Found start of JSON object, extract from there to end
        return content[json_object_start:].strip()
    
    # No code blocks or JSON objects found, return as is (maybe it's already clean JSON)
    return content
