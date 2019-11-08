import os

from locust import HttpLocust
from locust.exception import LocustError

from tests import CoreUserTaskSet


class BuildlyLocust(HttpLocust):
    min_wait = 1000
    max_wait = 3000
    task_set = CoreUserTaskSet  # os.getenv('LOCUST_TASK_SET', 'CoreUserTaskSet')
    if task_set is None:
        raise LocustError('A task set was not defined!')
