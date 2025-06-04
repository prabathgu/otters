import unittest
from unittest.mock import patch, MagicMock
from utils.web import (
    search_web, 
    fetch_html, 
    parse_html, 
    extract_text, 
    get_webpage_content,
    get_direct_answer,
    download_file
)
from bs4 import BeautifulSoup
import requests
from tools.return_type import ToolResult

class TestWebTool(unittest.TestCase):
    @patch('requests.get')
    def test_search_web(self, mock_requests):
        # Mock the requests response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'organic_results': [
                {'title': 'Test Result', 'link': 'https://test.com', 'snippet': 'Test snippet'}
            ]
        }
        mock_requests.return_value = mock_response
        
        result = search_web(query="test query")
        self.assertTrue(result.success)
        self.assertEqual(len(result.data), 1)
        self.assertEqual(result.data[0]['title'], 'Test Result')
        self.assertEqual(result.data[0]['link'], 'https://test.com')
        self.assertEqual(result.data[0]['snippet'], 'Test snippet')

        # Verify the API was called with correct parameters
        mock_requests.assert_called_once()
        call_args = mock_requests.call_args[1]['params']
        self.assertEqual(call_args['q'], 'test query')
        self.assertEqual(call_args['engine'], 'duckduckgo')

    @patch('requests.get')
    def test_search_web_news(self, mock_requests):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'news_results': [
                {
                    'title': 'News Result',
                    'link': 'https://news.com',
                    'snippet': 'News snippet',
                    'date': '2024-03-20'
                }
            ]
        }
        mock_requests.return_value = mock_response
        
        result = search_web(query="test query", search_type="news")
        self.assertTrue(result.success)
        self.assertEqual(result.data[0]['date'], '2024-03-20')

    def test_fetch_html_success(self):
        with patch('requests.get') as mock_get:
            mock_response = MagicMock()
            mock_response.text = "<html><body>Test content</body></html>"
            mock_get.return_value = mock_response
            
            result = fetch_html("https://test.com")
            self.assertEqual(result, "<html><body>Test content</body></html>")

    def test_fetch_html_failure(self):
        with patch('requests.get') as mock_get:
            mock_get.side_effect = requests.RequestException("Connection error")
            
            with self.assertRaises(Exception) as context:
                fetch_html("https://test.com")
            self.assertIn("Error fetching URL", str(context.exception))

    def test_parse_html(self):
        html_content = "<html><body><p>Test content</p></body></html>"
        result = parse_html(html_content)
        self.assertIsInstance(result, BeautifulSoup)
        self.assertEqual(result.p.text, "Test content")

    def test_extract_text(self):
        soup = BeautifulSoup("<html><body><p>Test</p><p>content</p></body></html>", 'html.parser')
        result = extract_text(soup)
        self.assertEqual(result, "Test content")

    @patch('tools.web.fetch_html')
    @patch('tools.web.html_to_markdown')
    def test_get_webpage_content(self, mock_to_markdown, mock_fetch):
        mock_fetch.return_value = "<html><body>Test content</body></html>"
        mock_to_markdown.return_value = "# Test content"
        
        result = get_webpage_content(url="https://test.com")
        self.assertTrue(result.success)
        self.assertEqual(result.data, "# Test content")

    @patch('tools.web.fetch_html')
    def test_get_webpage_content_error(self, mock_fetch):
        mock_fetch.side_effect = Exception("Failed to fetch")
        result = get_webpage_content(url="https://test.com")
        self.assertFalse(result.success)
        self.assertIn("Error processing webpage: Failed to fetch", result.error)

    @patch('tools.web.GoogleSearch')
    def test_get_direct_answer(self, mock_search):
        mock_search_instance = MagicMock()
        expected_answer = {
            'type': 'calculator',
            'result': '4'
        }
        mock_search_instance.get_dict.return_value = {
            'answer_box': expected_answer
        }
        mock_search.return_value = mock_search_instance
        
        result = get_direct_answer(query="2+2")
        self.assertTrue(result.success)
        self.assertIn('answer', result.data)
        self.assertIn('type', result.data)
        self.assertEqual(result.data['answer'], expected_answer)
        self.assertEqual(result.data['type'], 'calculator')

    @patch('tools.web.GoogleSearch')
    def test_get_direct_answer_no_result(self, mock_search):
        mock_search_instance = MagicMock()
        mock_search_instance.get_dict.return_value = {}
        mock_search.return_value = mock_search_instance
        
        result = get_direct_answer(query="invalid query")
        self.assertFalse(result.success)
        self.assertEqual(result.error, "Error: No direct answer found")

    @patch('requests.get')
    def test_download_file(self, mock_requests):
        mock_response = MagicMock()
        mock_response.headers = {
            'content-type': 'text/plain',
            'content-length': '100'
        }
        mock_response.iter_content.return_value = [b'test content']
        mock_requests.return_value = mock_response

        with patch('pathlib.Path.mkdir'), \
             patch('builtins.open', unittest.mock.mock_open()):
            result = download_file(url="https://test.com/file.txt", filename="test.txt")
            
            self.assertTrue(result.success)
            self.assertEqual(result.data['status'], 'success')
            self.assertEqual(result.data['content_type'], 'text/plain')
            self.assertEqual(result.data['file_size'], 100)

    @patch('requests.get')
    def test_download_file_error(self, mock_requests):
        mock_requests.side_effect = requests.RequestException("Download failed")
        
        result = download_file(url="https://test.com/file.txt")
        self.assertFalse(result.success)
        self.assertIn('Download failed', result.error)

if __name__ == '__main__':
    unittest.main()
