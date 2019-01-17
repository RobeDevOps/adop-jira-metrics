

class SearchController:
    def __init__(self, client):
        self.client = client

    def get_issues_key_by_project(self, project_key):
        return self.client.get_issues_key_by_project(project_key)
