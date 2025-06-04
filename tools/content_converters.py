import html2text
import weave
from tools.return_type import ToolResult

CONTENT_CONVERTER_TOOLS = {
    "html_to_markdown": {
        "type": "function",
        "function": {
            "name": "content_converters-html_to_markdown",
            "description": """Converts HTML content to Markdown format.  Best used for:
            - Converting HTML content to Markdown format
            - Converting HTML content to a format that is easier to read and edit 
            - Removing HTML tags to prepare content to be sent to chat completion models when the HTML is not needed for the task.
            """,
            "parameters": {
                "type": "object",
                "properties": {
                    "content": {
                        "type": "string",
                        "description": "The HTML content to convert"
                    }
                },
                "required": ["content"]
            }
        }
    }
}

@weave.op(name="content_converters-html_to_markdown")
def html_to_markdown(*, content: str) -> ToolResult[str]:
    """Convert HTML content to Markdown format."""
    try:
        h = html2text.HTML2Text()
        h.ignore_links = False
        h.ignore_images = False
        h.ignore_emphasis = False
        h.body_width = 0  # Disable line wrapping

        markdown_content = h.handle(content)
        return ToolResult.ok(markdown_content.strip())
    except Exception as e:
        return ToolResult.err(str(e))