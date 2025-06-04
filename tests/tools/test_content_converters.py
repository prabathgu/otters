import unittest
from tools.content_converters import html_to_markdown

class TestContentConvertersTool(unittest.TestCase):
    def test_html_to_markdown(self):
        html_content = "<h1>Test</h1><p>This is a <strong>test</strong>.</p>"
        result = html_to_markdown(content=html_content)
        self.assertTrue(result.success)
        self.assertEqual(result.data, "# Test\n\nThis is a **test**.")
        self.assertIsNone(result.error)

    def test_html_to_markdown_error(self):
        result = html_to_markdown(content=None)
        self.assertFalse(result.success)
        self.assertIsNone(result.data)
        self.assertIsNotNone(result.error)

if __name__ == '__main__':
    unittest.main()