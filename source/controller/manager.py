import requests
from errors.http import *
from errors.status_codes import *
from errors.params import InvalidAuthentication
import logging

logger = logging.getLogger('JIRA-LOGS')


class JiraManager:

    def __init__(self, host=None, username=None, password=None):

        self._host = host
        self._session = requests.Session()

        logger.info("Create client controller for server: {}".format(
            self._host))

        if username != None:
            # password is empty when username works as token id.
            # So credentials works like:
            #       self._session.auth = token, '' where token is username
            self._session.auth = username, password
            logger.info(
                "Creating credentials with username/password")
        else:
            raise InvalidAuthentication()

    def build_url(self, endpoint):
        return '{base_path}{endpoint}'.format(base_path=self._host, endpoint=endpoint)

    def get_response_by_params(self, method, url, **params):
        # Get method and make the call
        call = getattr(self._session, method.lower())
        self._session.params = params

        if params:
            logger.info("Calling endpoint: {url} with params {params}" .format(
                url=url, params=params))
        else:
            logger.info("Calling endpoint: {url}" .format(url=url))

        res = call(url)

        if res.status_code < HTTP_300:
            # OK, return http response
            return res
        elif res.status_code in (HTTP_401, HTTP_403):
            # Authentication error. Need to verify username/password or token
            raise AuthenticationError(res.reason)
        elif res.status_code == HTTP_404:
            # Need to check the endpoint provided
            raise NotFoundError(res.reason)
        elif res.status_code < HTTP_500:
            # Any other 4xx, it is reported as a generic client error
            print(res.status_code)
            raise ClientError(res.reason)
        else:
            # 5xx is server error
            raise ServerError(res.reason)
