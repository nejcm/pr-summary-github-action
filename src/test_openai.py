import unittest
from unittest.mock import patch, MagicMock
from openai_summary import openai_summary

class TestOpenAISummary(unittest.TestCase):
    @patch('openai_summary.OpenAI')
    def test_openai_success(self, mock_openai):
        # Mock response from OpenAI
        mock_response = MagicMock()
        mock_response.chat.completions.create.return_value = {
            'choices': [
                {'message': {'content': 'This is a summary of the commit messages.'}}
            ]
        }
        mock_openai.return_value = mock_response
        
        key = 'FAKE_API_KEY'
        prompt_message = "Please summarize these commit messages:"
        commit_messages = "Initial commit\nAdded feature X"
        
        summary = openai_summary(prompt_message, commit_messages, key)
        self.assertEqual(summary, 'This is a summary of the commit messages.')

    def test_openai_summary_empty_commit_messages(self):
        key = 'FAKE_API_KEY'
        prompt_message = "Please summarize these commit messages:"
        commit_messages = ""
        
        with self.assertRaises(ValueError) as context:
            openai_summary(prompt_message, commit_messages, key)
        self.assertEqual(str(context.exception), "Commit messages are empty!")

    @patch('openai_summary.OpenAI')
    def test_openai_null_summary(self, mock_openai):
        # Mock response from OpenAI with an empty summary
        mock_response = MagicMock()
        mock_response.chat.completions.create.return_value = {
            'choices': [
                {'message': {'content': ''}}
            ]
        }
        mock_openai.return_value = mock_response
        
        key = 'FAKE_API_KEY'
        prompt_message = "Please summarize these commit messages:"
        commit_messages = "Fix bug in user login"
        
        with self.assertRaises(ValueError) as context:
            openai_summary(prompt_message, commit_messages, key)
        self.assertEqual(str(context.exception), "Summary is null or empty.")

if __name__ == '__main__':
    unittest.main()