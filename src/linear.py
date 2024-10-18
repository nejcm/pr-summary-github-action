import requests

query = """
query CustomViewIssues($id: String!, $first: Int, $after: String) {
  customView(id: $id) {
    id
    name
    issues(first: $first, after: $after) {
      pageInfo {
        hasNextPage
        endCursor
      }
      edges {
        node {
          id
          team {
            name
          }
          title
          identifier
          description
          state {
            name
          }
          estimate
          priority
          priorityLabel
          project {
            id
            name
          }
          creator {
            email
          }
          assignee {
            email
          }
          labels {
            nodes {
              name
            }
          }
          cycle {
            number
            name
            startsAt
            endsAt
          }
          createdAt
          updatedAt
          startedAt
          startedTriageAt
          completedAt
          canceledAt
          archivedAt
          dueDate
          parent {
            id
          }
          projectMilestone {
            id
            name
          }
        }
      }
    }
  }
}
"""

# Set up headers for Linear API
headers = {
    'Authorization': LINEAR_KEY,
    'Content-Type': 'application/json',
}

def linear(custom_view_id, first=50):
    all_issues = []
    has_next_page = True
    after = None

    while has_next_page:
        variables = {
            "id": custom_view_id,
            "first": first,
            "after": after
        }
        response = requests.post('https://api.linear.app/graphql', json={'query': query, 'variables': variables}, headers=headers)

        if response.status_code == 200:
            data = response.json()['data']['customView']['issues']
            all_issues.extend(data['edges'])
            has_next_page = data['pageInfo']['hasNextPage']
            after = data['pageInfo']['endCursor']
        else:
            print(f"Error: {response.status_code}")
            raise Exception(f"Query failed with status code: {response.status_code}")

    return all_issues