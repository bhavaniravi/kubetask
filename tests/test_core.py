import pytest
import datetime
from kubetask.core.config import Config
from kubetask.core.task import Task
from kubetask.core.constants import State


task_list = [
    {
        "task_name": "new task",
        "docker_url": "docker_url",
        "command": [],
        "schedule": None,
        "start_at": None,
    },
    {
        "task_name": "new task 1",
        "docker_url": "docker_url 1",
        "command": ["python", "setup.py"],
        "schedule": "@daily",
        "start_at": None,
    },
    {
        "task_name": "new task 1",
        "docker_url": "docker_url 1",
        "command": ["python", "setup.py"],
        "schedule": None,
        "start_at": datetime.datetime.utcnow(),
    },
]


class TestTask:
    def test_init_type_error(self):
        arguments = {
            "task_id": "task_002",
            "task_name": "new task 1",
            "docker_url": "docker_url 1",
            "command": ["python", "setup.py"],
            "schedule": "@daily",
            "start_at": datetime.datetime.utcnow(),
        }

        with pytest.raises(TypeError):
            task = Task(**arguments)

    @pytest.mark.parametrize(
        "arguments",
        [
            (task_list[0]),
            (task_list[1]),
            (task_list[2]),
        ],
    )
    def test_task_init(self, arguments):
        task = Task(**arguments)
        for key, value in arguments.items():
            assert getattr(task, key) == value
        task.state = State.NOT_STARTED

    @pytest.mark.parametrize(
        "arguments, state",
        [
            (task_list[0], State.STARTED),
            (task_list[1], State.SCHEDULED),
            (task_list[2], State.DEFERRED),
        ],
    )
    def test_task_start(self, arguments, state):
        task = Task(**arguments)
        task.start()
        assert task.state == state
        assert task.task_id is not None