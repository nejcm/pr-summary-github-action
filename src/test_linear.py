import unittest
from unittest.mock import patch, MagicMock
import linear

class TestLinear(unittest.TestCase):

    @patch('linear.requests.post')
    def test_linear_success(self, mock_post):
        # Simulate a successful response from the Linear API
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'data': {
                'customView': {
                    'issues': {
                        'pageInfo': {
                            'hasNextPage': False,
                            'endCursor': None
                        },
                        'edges': [{'node': {'id': '1', 'title': 'Issue 1'}}]
                    }
                }
            }
        }
        mock_post.return_value = mock_response

        issues = linear.linear(custom_view_id="fake_id", key="fake_key")

        # Verify linear returns expected result
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0]['node']['title'], 'Issue 1')

        # Verify the request was made with correct headers
        mock_post.assert_called_once_with(
            'https://api.linear.app/graphql',
            json={'query': linear.query, 'variables': {'id': 'fake_id', 'first': 50, 'after': None}},
            headers={'Authorization': 'fake_key', 'Content-Type': 'application/json'}
        )

    @patch('linear.requests.post')
    def test_linear_pagination(self, mock_post):
        # Simulate two responses to test pagination
        mock_response_page_1 = MagicMock()
        mock_response_page_1.status_code = 200
        mock_response_page_1.json.return_value = {
            'data': {
                'customView': {
                    'issues': {
                        'pageInfo': {
                            'hasNextPage': True,
                            'endCursor': 'page2_cursor'
                        },
                        'edges': [{'node': {'id': '1', 'title': 'Issue 1'}}]
                    }
                }
            }
        }
        
        mock_response_page_2 = MagicMock()
        mock_response_page_2.status_code = 200
        mock_response_page_2.json.return_value = {
            'data': {
                'customView': {
                    'issues': {
                        'pageInfo': {
                            'hasNextPage': False,
                            'endCursor': None
                        },
                        'edges': [{'node': {'id': '2', 'title': 'Issue 2'}}]
                    }
                }
            }
        }
        
        # Set a side_effect to simulate the paginator getting two pages
        mock_post.side_effect = [mock_response_page_1, mock_response_page_2]

        issues = linear.linear(custom_view_id="fake_id", key="fake_key")

        # Verify it fetched two pages
        self.assertEqual(len(issues), 2)
        self.assertEqual(issues[0]['node']['title'], 'Issue 1')
        self.assertEqual(issues[1]['node']['title'], 'Issue 2')

    @patch('linear.requests.post')
    def test_linear_failed_request(self, mock_post):
        # Simulate a failed response from the Linear API
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_post.return_value = mock_response

        with self.assertRaises(Exception) as context:
            linear.linear(custom_view_id="fake_id", key="fake_key")

        self.assertTrue('Query failed with status code: 404' in str(context.exception))

if __name__ == '__main__':
    unittest.main()