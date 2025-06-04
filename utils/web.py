import requests
import weave
from bs4 import BeautifulSoup
from typing import List, Dict, Literal
import os
from serpapi.google_search import GoogleSearch
from pathlib import Path
from tools.content_converters import html_to_markdown
from tools.return_type import ToolResult

WEB_TOOLS = {
    "get_webpage_content": {
        "type": "function",
        "function": {
            "name": "web-get_webpage_content",
            "description": "Fetches content from a URL and returns it in markdown format, preserving links and structure while being clean and readable.",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "The URL to fetch the content from"
                    }
                },
                "required": ["url"]
            }
        }
    },
    "search_web": {
        "type": "function",
        "function": {
            "name": "web-search_web",
            "description": "Performs a DuckDuckGo web or news search with optional time filtering and returns the results",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query"
                    },
                    "search_type": {
                        "type": "string",
                        "description": "Type of search - either 'web' or 'news'",
                        "enum": ["web", "news"]
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "Maximum number of results to return (default 5)",
                        "default": 5
                    },
                    "time_period": {
                        "type": "string",
                        "description": "Filter results by time period. Can use natural language like 'last week' or specific periods like 'day', 'week', 'month', 'year', 'all'",
                        "default": "all"
                    }
                },
                "required": ["query"]
            }
        }
    },
    "get_direct_answer": {
        "type": "function", 
        "function": {
            "name": "web-get_direct_answer",
            "description": "Gets a direct answer from Google for questions about weather, calculations, unit conversions, etc.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The question to get a direct answer for (e.g. 'weather in london', '2+2', '5km to miles')"
                    }
                },
                "required": ["query"]
            }
        }
    },
    "download_file": {
        "type": "function",
        "function": {
            "name": "web-download_file",
            "description": "Downloads a file from a URL to the downloads directory",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "The URL of the file to download"
                    },
                    "filename": {
                        "type": "string",
                        "description": "Optional filename to save as. If not provided, will use the filename from the URL",
                        "default": ""
                    }
                },
                "required": ["url"]
            }
        }
    }
}

def fetch_html(url):
    """
    Fetches the HTML content from the given URL.
    
    Args:
    url (str): The URL to fetch the HTML from.
    
    Returns:
    str: The HTML content of the page.
    
    Raises:
    Exception: If there's an error fetching the URL or parsing the content.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.text
    except requests.RequestException as e:
        raise Exception(f"Error fetching URL: {e}")

def parse_html(html_content):
    """
    Parses the HTML content and returns a BeautifulSoup object.
    
    Args:
    html_content (str): The HTML content to parse.
    
    Returns:
    BeautifulSoup: A BeautifulSoup object representing the parsed HTML.
    """
    return BeautifulSoup(html_content, 'html.parser')

def extract_text(soup):
    """
    Extracts all visible text from the parsed HTML.
    
    Args:
    soup (BeautifulSoup): The parsed HTML.
    
    Returns:
    str: The extracted text content.
    """
    return soup.get_text(separator=' ', strip=True)

@weave.op(name="web-get_webpage_content")
def get_webpage_content(*, url: str) -> ToolResult[str]:
    """
    Retrieves content from a URL and converts it to markdown format.
    
    Args:
    url (str): The URL to fetch the content from.
    
    Returns:
    str: The webpage content converted to markdown format.
    
    Raises:
    Exception: If there's an error during the process.
    """
    try:
        html_content = fetch_html(url)
        markdown_content = html_to_markdown(content=html_content)
        return ToolResult.ok(markdown_content)
    except Exception as e:
        return ToolResult.err(f"Error processing webpage: {e}")

@weave.op(name="web-search_web")
def search_web(*, query: str, search_type: Literal['web', 'news'] = 'web', 
               max_results: int = 5, time_period: str = 'all') -> ToolResult[List[Dict]]:
    """
    Search the web using DuckDuckGo.
    
    Args:
        query: The search query
        search_type: Type of search - either "web" or "news"
        max_results: Maximum number of results to return (default 5)
        time_period: Filter results by time - can be natural language like "last week" or specific periods like "day", "week", "month", "year", "all"
        
    Returns:
        List of search results with title, link, snippet and thumbnail
    """
    try:
        # Map time periods to DuckDuckGo time filters
        time_filters = {
            "day": "d",
            "last day": "d",
            "today": "d",
            "week": "w",
            "last week": "w",
            "month": "m",
            "last month": "m",
            "year": "y",
            "last year": "y",
            "all": None
        }
        
        # Normalize time period input
        normalized_time = time_period.lower().strip()
        
        # Configure SerpAPI parameters
        params = {
            "api_key": os.getenv("SERPAPI_API_KEY"),
            "q": query,
            "engine": "duckduckgo_news" if search_type == "news" else "duckduckgo",
            "kl": "us-en"  # Region code for US English
        }
        
        # Add time filter if specified
        if normalized_time != "all" and normalized_time in time_filters:
            params["time"] = time_filters[normalized_time]
        
        # Make API request
        response = requests.get("https://serpapi.com/search", params=params)
        response.raise_for_status()
        data = response.json()
        
        # Extract results based on search type
        if search_type == "news":
            results = data.get("news_results", [])
        else:
            results = data.get("organic_results", [])
        
        # Limit results and normalize format
        formatted_results = []
        for result in results[:max_results]:
            formatted_result = {
                "title": result["title"],
                "link": result["link"],
                "snippet": result.get("snippet", ""),
                "thumbnail": result.get("thumbnail", "")  # Add thumbnail URL if available
            }
            # Add date for news results if available
            if search_type == "news":
                formatted_result["date"] = result.get("date")
            
            formatted_results.append(formatted_result)
        
        return ToolResult.ok(formatted_results)
        
    except Exception as e:
        return ToolResult.err(f"Error searching web: {str(e)}")

@weave.op(name="web-get_direct_answer")
def get_direct_answer(*, query: str) -> ToolResult[Dict]:
    """
    Gets a direct answer from Google using SerpAPI.
    
    Args:
        query: The question to get a direct answer for
        
    Returns:
        Dictionary containing the direct answer information if available
    """
    try:
        params = {
            "api_key": os.getenv("SERPAPI_API_KEY"),
            "q": query,
            "engine": "google"
        }
        
        search = GoogleSearch(params)
        results = search.get_dict()
        
        # Check if there's a direct answer box
        answer_box = results.get("answer_box")
        if not answer_box:
            return ToolResult.err("No direct answer found")
            
        # Return the answer box data
        response = {
            "type": answer_box.get("type"),
            "answer": answer_box,
            "raw_answer_box": answer_box
        }
        return ToolResult.ok(response)
        
    except Exception as e:
        return ToolResult.err(f"Error getting direct answer: {str(e)}")

@weave.op(name="web-download_file")
def download_file(*, url: str, filename: str = '') -> ToolResult[Dict]:
    """
    Downloads a file from a URL to the downloads directory.
    
    Args:
        url: The URL of the file to download
        filename: Optional filename to save as. If not provided, will use the filename from the URL
        
    Returns:
        Dictionary containing the download status and file path
    """
    try:
        # Create downloads directory if it doesn't exist
        downloads_dir = Path("downloads")
        downloads_dir.mkdir(exist_ok=True)
        
        # Get filename from URL if not provided
        if not filename:
            filename = url.split('/')[-1]
            # Remove query parameters if present
            filename = filename.split('?')[0]
        
        # Create full file path
        file_path = downloads_dir / filename
        
        # Download the file with stream=True to handle large files
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        # Get content type and size
        content_type = response.headers.get('content-type', 'unknown')
        file_size = int(response.headers.get('content-length', 0))
        
        # Write the file
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        
        result = {
            "status": "success",
            "file_path": str(file_path),
            "content_type": content_type,
            "file_size": file_size,
            "filename": filename
        }
        return ToolResult.ok(result)
        
    except Exception as e:
        return ToolResult.err(f"Error downloading file: {str(e)}")
