

class ProjectController:

    def __init__(self, client):
        self.client = client

    def get_all_projects(self):
        return self.client.get_all_projects()
