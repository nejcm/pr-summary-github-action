import unittest
from unittest.mock import Mock, patch, MagicMock
from openai_summary import openai_summary

def create_mock_response(content):
    mock = Mock()
    mock.choices = [
        Mock(
            message = Mock(
                content = content
            )
        )
    ]
    return mock

class TestOpenAISummary(unittest.TestCase):
    @patch('openai_summary.OpenAI')
    def test_openai_success(self, mock_openai):
        # Mock response from OpenAI
        mock_response = MagicMock()
        mock_response.chat.completions.create.return_value = create_mock_response('This is a summary of the commit messages.')
        mock_openai.return_value = mock_response
        
        key = 'FAKE_API_KEY'
        prompt_message = "Please summarize these commit messages:"
        commit_messages = "Initial commit\nAdded feature X"
        org = "test_org"
        
        summary = openai_summary(commit_messages, prompt_message, key, org)
        self.assertEqual(summary, 'This is a summary of the commit messages.')

    def test_openai_summary_empty_commit_messages(self):
        key = 'FAKE_API_KEY'
        prompt_message = "Please summarize these commit messages:"
        commit_messages = ""
        org = "test_org"
        
        with self.assertRaises(ValueError) as context:
            openai_summary(commit_messages, prompt_message, key, org)
        self.assertEqual(str(context.exception), "Commit messages are empty!")

    @patch('openai_summary.OpenAI')
    def test_openai_null_summary(self, mock_openai):
        # Mock response from OpenAI with an empty summary
        mock_response = MagicMock()
        mock_response.chat.completions.create.return_value = create_mock_response('')
        mock_openai.return_value = mock_response
        
        key = 'FAKE_API_KEY'
        prompt_message = "Please summarize these commit messages:"
        commit_messages = "Fix bug in user login"
        org = "test_org"
        
        with self.assertRaises(ValueError) as context:
            openai_summary(commit_messages, prompt_message, key, org)
        self.assertEqual(str(context.exception), "Summary is null or empty.")

if __name__ == '__main__':
    unittest.main()