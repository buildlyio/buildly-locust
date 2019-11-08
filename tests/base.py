import os
import json

from locust import TaskSet
from .urls import LOGIN_URL_PATH, USER_DATA_PATH

OAUTH_CREDENTIALS = os.environ['OAUTH_CREDENTIALS']


class BaseTaskSet(TaskSet):
    def setup(self):
        """ on_start is called when a Locust start before any task is scheduled """
        self._login()
        self._get_user()

    def _login(self):
        # create payload and headers to request token from the server
        payload = "username=admin&password=admin&grant_type=password"
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': f'Basic {OAUTH_CREDENTIALS}',
            'cache-control': 'no-cache'
        }
        self.client.headers = headers
        response = self.client.post(LOGIN_URL_PATH, data=payload)
        data = json.loads(response.content.decode('utf-8'))

        # set JSON Web Token for the upcoming requests
        os.environ['USER_JWT'] = data['access_token_jwt']
        self.client.headers = {'Authorization': f'JWT {data["access_token_jwt"]}'}

    def _get_user(self):
        response = self.client.get(USER_DATA_PATH)
        data = json.loads(response.content.decode('utf-8'))
        os.environ['USER_DATA'] = json.dumps(data['core_user'])
