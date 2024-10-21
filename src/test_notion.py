import unittest
from unittest.mock import patch, MagicMock
import notion

class TestNotion(unittest.TestCase):

    @patch('notion.requests.post')
    def test_notion(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        response = notion.notion(
            summary="Test summary",
            commit_messages="Test commit message",
            key="fake_key",
            version="1.0.0",
            changelog="Test changelog"
        )

        # Verify HTTP request was made
        mock_post.assert_called_once()
        self.assertEqual(response.status_code, 200)

    def test_split_into_chunks(self):
        text = "This is a test message."
        limit = 5
        expected_chunks = ["This ", "is a ", "test ", "messa", "ge."]
        chunks = notion.split_into_chunks(text, limit)
        self.assertEqual(chunks, expected_chunks)

if __name__ == '__main__':
    unittest.main()