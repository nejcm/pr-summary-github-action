import unittest
from unittest.mock import patch
from main import main

class TestMainFunction(unittest.TestCase):
    
    @patch('main.linear')
    @patch('main.claude_summary')
    @patch('main.openai_summary')
    @patch('main.notion')
    @patch('os.environ', {
        "OPENAI_KEY": "mock_openai_key",
        "CLAUDE_KEY": "mock_claude_key",
        "NOTION_KEY": "mock_notion_key",
        "LINEAR_KEY": "mock_linear_key",
        "LINEAR_VIEW_ID": "mock_linear_view_id",
        "CHANGELOG": "mock_changelog",
        "VERSION": "mock_version",
        "PROMPT": "mock_prompt",
        "COMMITS": "mock_commits"
    })
    def test_main_with_claude_key(self, mock_notion, mock_openai_summary, mock_claude_summary, mock_linear):
        mock_linear.return_value = ['issue1', 'issue2']
        mock_claude_summary.return_value = 'Claude release notes'

        release_notes = main()

        mock_claude_summary.assert_called_once_with(['issue1', 'issue2'], "mock_prompt", "mock_claude_key")
        mock_notion.assert_called_once_with('Claude release notes', 'mock_commits', 'mock_notion_key', 'mock_version', 'mock_changelog')
        self.assertEqual(release_notes, 'Claude release notes')

    @patch('main.linear')
    @patch('main.claude_summary')
    @patch('main.openai_summary')
    @patch('main.notion')
    @patch('os.environ', {
        "OPENAI_KEY": "mock_openai_key",
        "CLAUDE_KEY": "",
        "NOTION_KEY": "mock_notion_key",
        "LINEAR_KEY": "mock_linear_key",
        "LINEAR_VIEW_ID": "mock_linear_view_id",
        "CHANGELOG": "mock_changelog",
        "VERSION": "mock_version",
        "PROMPT": "mock_prompt",
        "COMMITS": "mock_commits"
    })
    def test_main_with_openai_key(self, mock_notion, mock_openai_summary, mock_claude_summary, mock_linear):
        mock_linear.return_value = ['issue1', 'issue2']
        mock_openai_summary.return_value = 'OpenAI release notes'

        release_notes = main()

        mock_openai_summary.assert_called_once_with(['issue1', 'issue2'], "mock_prompt", "mock_openai_key")
        mock_notion.assert_called_once_with('OpenAI release notes', 'mock_commits', 'mock_notion_key', 'mock_version', 'mock_changelog')
        self.assertEqual(release_notes, 'OpenAI release notes')

    @patch('main.linear')
    @patch('main.claude_summary')
    @patch('main.openai_summary')
    @patch('main.notion')
    @patch('os.environ', {
        "OPENAI_KEY": "",
        "CLAUDE_KEY": "",
        "NOTION_KEY": "",
        "LINEAR_KEY": "",
        "LINEAR_VIEW_ID": "",
        "CHANGELOG": "",
        "VERSION": "",
        "PROMPT": "",
        "COMMITS": "mock_commits"
    })
    def test_main_without_keys(self, mock_notion, mock_openai_summary, mock_claude_summary, mock_linear):
        mock_linear.return_value = ''

        release_notes = main()

        mock_linear.assert_not_called()
        mock_claude_summary.assert_not_called()
        mock_openai_summary.assert_not_called()
        mock_notion.assert_not_called()
        self.assertIsNone(release_notes)

if __name__ == '__main__':
    unittest.main()