import unittest
from unittest.mock import MagicMock, patch
from claude_summary import claude_summary

class TestClaudeSummary(unittest.TestCase):

    @patch('anthropic.Anthropic')
    def test_claude_summary(self, MockAnthropic):
        # Setup the mock instance and behavior
        mock_client = MockAnthropic.return_value
        mock_client.messages.create.return_value.content = MagicMock()

        # Test when message content is a list
        mock_client.messages.create.return_value.content = [
            MagicMock(text='Summary 1'),
            MagicMock(text='Summary 2')
        ]
        issues = "Sample issue description"
        prompt = "Summarize the following issues:"
        key = "fake-api-key"
        
        result = claude_summary(issues, prompt, key)
        self.assertEqual(result, "Summary 1\nSummary 2")

        # Test when message content has a text attribute 
        mock_client.messages.create.return_value.content = MagicMock(text='Summary 3')
        result = claude_summary(issues, prompt, key)
        self.assertEqual(result, "Summary 3")

        # Test when message content does not have a text attribute
        mock_client.messages.create.return_value.content = MagicMock()
        del mock_client.messages.create.return_value.content.text
        result = claude_summary(issues, prompt, key)
        self.assertEqual(result, "Error: Couldn't extract release notes from the API response.")

if __name__ == '__main__':
    unittest.main()