
class SearchClient:

    SEARCH_ENDPOINT = '/rest/api/2/search'

    def __init__(self, controller_client):
        self._controller_client = controller_client

    def get_issues_key_by_project(self, project_key):

        params = {}
        # query string definition
        params['jql'] = "project={}".format(project_key)
        params['fields'] = '*'

        start_at = 0
        max_result = 1
        total = 1

        params['startAt'] = start_at
        params['maxResults'] = max_result

        url = self._controller_client.build_url(
            self.SEARCH_ENDPOINT)

        # Looping all the pages looking for components
        while start_at * max_result <= total - 1:
            # Update paging information for calculation
            res = self._controller_client.get_response_by_params(
                'get', url, **params).json()

            start_at = res['startAt'] + 1
            max_result = res['maxResults']
            total = res['total']

            # Update page number (next) in queryset
            params['startAt'] = start_at

            # Yield rules
            if len(res['issues']) > 0:
                yield {
                    'issue_key': res['issues'][0]['key']
                }
