

class IssueClient:
    ISSUE_ENDPOINT = "/rest/api/2/issue/{issue_id_or_key}"

    def __init__(self, controller_client):
        self._controller_client = controller_client

    def get_issue_status_by_key(self, issue_key):

        params = {}

        ISSUE_ENDPOINT = self.ISSUE_ENDPOINT.format(
            issue_id_or_key=issue_key)

        # query string definition
        params['fields'] = 'status'

        url = self._controller_client.build_url(ISSUE_ENDPOINT)

        res = self._controller_client.get_response_by_params(
            'get', url, **params).json()

        return {
            'status': res['fields']['status']['name']
        }
