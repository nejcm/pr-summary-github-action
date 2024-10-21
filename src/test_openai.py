import unittest
from unittest.mock import patch, MagicMock
from openai import OpenAIError
import openai

class TestOpenAISummary(unittest.TestCase):

    @patch('openai.OpenAI')
    def test_openai_summary_success(self, mock_openai):
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = {
            'choices': [{'message': {'content': 'Generated summary'}}]
        }
        mock_openai.return_value = mock_client

        summary = openai.openai_summary(
            prompt_message="Generate a summary for:",
            commit_messages="Here are commit messages.",
            key="fake_openai_api_key"
        )

        self.assertEqual(summary, "Generated summary")

    @patch('openai.OpenAI')
    def test_openai_summary_empty_commit_messages(self, mock_openai):
        with self.assertRaises(ValueError):
            openai.openai_summary(
                prompt_message="Test prompt",
                commit_messages="",
                key="fake_openai_api_key"
            )

if __name__ == '__main__':
    unittest.main()