import json
import os
import random

from locust import task

from .base import BaseTaskSet


class CoreUserTaskSet(BaseTaskSet):
    def on_start(self):
        self.client.headers = {'Authorization': f'JWT {os.environ["USER_JWT"]}'}

    @task
    def test_change_user(self):
        first_names = ['John', 'Bruno', 'Leon', 'Karla', 'Joana', 'Anna']
        last_names = ['Muller', 'Silva', 'Santos', 'Smith', 'Brown', 'Taylor']
        payload = {
            'first_name': first_names[random.randrange(5)],
            'last_name': last_names[random.randrange(5)]
        }
        user_id = json.loads(os.environ['USER_DATA'])['id']
        self.client.patch(f'/coreuser/{user_id}/?partial=true', payload)
