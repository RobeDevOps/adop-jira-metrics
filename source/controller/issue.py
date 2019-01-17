

class IssueController:
    def __init__(self, client):
        self.client = client

    def get_issue_status_by_key(self, issue_key):
        return self.client.get_issue_status_by_key(issue_key)
