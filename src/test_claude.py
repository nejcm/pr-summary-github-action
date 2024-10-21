import unittest
from unittest.mock import patch, MagicMock
import claude

class TestClaudeSummary(unittest.TestCase):

    @patch('claude.anthropic.Anthropic')
    def test_claude_summary(self, mock_anthropic):
        mock_client = MagicMock()
        mock_client.messages.create.return_value = MagicMock(content={"text": "Generated Claude summary"})
        mock_anthropic.return_value = mock_client

        summary = claude.claude_summary(
            issues="List of issues",
            prompt="Generate a summary for issues:",
            key="fake_claude_api_key"
        )

        self.assertEqual(summary, "Generated Claude summary")

if __name__ == '__main__':
    unittest.main()