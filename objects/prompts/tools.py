import weave
from weave import Prompt
from utils.helpers import load_tools
from typing import List, Dict, Any

class ToolsPrompt(Prompt):
    tools: List[Dict[str, Any]] = load_tools()

    def __init__(self, tools: List[Dict[str, Any]] = None):
        super().__init__()
        self.tools = tools if tools is not None else load_tools()

    @weave.op(name="tools-generate_tool_descriptions")
    def get_tools_descriptions(self) -> str:
        tool_descriptions = []
        for i, tool in enumerate(self.tools):
            # Basic tool info
            desc = [
                f"{i+1}. **{tool['function']['name']}({', '.join(tool['function']['parameters'].get('properties', {}).keys())})**",
                f"   - {tool['function'].get('description', 'No description available.')}"
            ]
            
            # Parameters section
            if tool['function']['parameters'].get('properties'):
                desc.append("   - **Parameters:**")
                for param, properties in tool['function']['parameters'].get('properties', {}).items():
                    # Parameter name, type and description
                    param_desc = [f"     - `{param}` ({properties.get('type', 'any')}): {properties.get('description', 'No description.')}"]
                    
                    # Add enum values if they exist, converting WeaveList to regular list
                    if 'enum' in properties:
                        enum_values = list(properties['enum'])  # Convert WeaveList to regular list
                        param_desc.append(f"       - Options: {enum_values}")
                    
                    # Add default value if it exists
                    if 'default' in properties:
                        param_desc.append(f"       - Default: \"{properties['default']}\"")
                    
                    desc.append("\n".join(param_desc))
            
            tool_descriptions.append("\n".join(desc))
        
        return "\n".join(tool_descriptions)
