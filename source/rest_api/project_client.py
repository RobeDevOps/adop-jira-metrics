import logging

logger = logging.getLogger("JIRA-LOGS")


class ProjectClient:

    PROJECT_ENDPOINT = "/rest/api/2/project"

    def __init__(self, client):
        self._controller_client = client

    def get_all_projects(self):

        url = self._controller_client.build_url(
            self.PROJECT_ENDPOINT)

        res = self._controller_client.get_response_by_params(
            'get', url).json()

        for index in range(0, len(res)):
            yield {
                'project_name': res[index]['name'].encode('utf-8'),
                'project_key': res[index]['key'].encode('utf-8')
            }
