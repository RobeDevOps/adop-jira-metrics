import logging
import os

from controller.manager import JiraManager
from controller.project import ProjectController
from controller.search import SearchController
from controller.issue import IssueController

from rest_api.project_client import ProjectClient
from rest_api.search_client import SearchClient
from rest_api.issue_client import IssueClient

import watcher.logger


class AgilePortfolio:

    def __init__(self):
        self.logger = logging.getLogger('JIRA-LOGS')

        self._prepare_clients()

    '''
    Create all the clients and controllers required for this manager class.
    E.g: Project, Issues, Search
    '''

    def _prepare_clients(self):

        HOST = os.environ.get('JIRA_HOST')
        USERNAME = os.environ.get('JIRA_USERNAME')
        PASSWORD = os.environ.get('JIRA_PASSWORD')

        self.jira_controller = JiraManager(HOST, USERNAME, PASSWORD)

        project_client = ProjectClient(self.jira_controller)
        self.project_controller = ProjectController(project_client)

        search_client = SearchClient(self.jira_controller)
        self.search_controller = SearchController(search_client)

        issue_client = IssueClient(self.jira_controller)
        self.issue_controller = IssueController(issue_client)

    '''
    Return all the project metrics as a collection of 
    WIP: number of tasks In Progress
    TO-DO: number of tasks in To Do
    DONE: number of tasks in Done
    project_name: Project name used as Jira name
    '''

    def collect_agile_metrics(self):
        self.logger.info("Collecting agile portfolio metrics")

        try:
            all_projects = self.project_controller.get_all_projects()

            for project in all_projects:
                wip = 0
                todo = 0
                done = 0

                issues = self.search_controller.get_issues_key_by_project(
                    project_key=project['project_key'])
                for issue in issues:
                    self.logger.info("**** Issue details ****")
                    self.logger.info("Issue: {}".format(issue['issue_key']))
                    issue_status = self.issue_controller.get_issue_status_by_key(
                        issue['issue_key'])
                    self.logger.info("Issue status: {}".format(issue_status))
                    if issue_status['status'] in "To Do":
                        todo = todo + 1
                    elif issue_status['status'] in "Done":
                        done = done + 1
                    elif issue_status['status'] in "In Progress":
                        wip = wip + 1

                yield {
                    "project_name": project['project_name'],
                    "TODO": todo,
                    "WIP": wip,
                    "DONE": done
                }
        except Exception as error:
            self.logger.info("Error in get_agile_metrics".format(
                str(error)), exc_info=True)
