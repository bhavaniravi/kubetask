import pytest
import datetime
from kubetask.core.config import Config
from kubetask.core.task import Task, TaskInstance, DBObject
from kubetask.core.constants import State

from kubetask.models.model import TaskModel, TaskInstanceModel


task_list = [
    {
        "task_name": "new task",
        "docker_url": "docker_url",
        "command": [],
        "start_at": None,
    },
    {
        "task_name": "new task 1",
        "docker_url": "docker_url 1",
        "command": ["python", "setup.py"],
        "schedule_at": "@daily",
        "start_at": None,
    },
    {
        "task_name": "new task 1",
        "docker_url": "docker_url 1",
        "command": ["python", "setup.py"],
        "start_at": datetime.datetime.utcnow(),
    },
    {
        "task_name": "new task 1",
        "docker_url": "docker_url 1",
        "command": ["python", "setup.py"],
        "start_at": datetime.datetime.utcnow(),
    },
]


class TestTask:
    @pytest.mark.parametrize(
        "arguments",
        [
            (task_list[0]),
            (task_list[1]),
            (task_list[2]),
        ],
    )
    def test_task_init(self, arguments):
        print(arguments)
        task = Task(**arguments)
        for key, value in arguments.items():
            assert getattr(task, key) == value

    def test_task_start(self):
        task = Task(**task_list[0])
        task_instance = task.start()
        assert task_instance.state == State.STARTED
        assert task.db_id is not None


class TestTaskInstance:
    def test_task_instance_obj(self):
        task_args = {
            "task_name": "new task",
            "docker_url": "docker_url",
            "command": [],
            "start_at": None,
        }
        task = Task(**task_args)
        ti = TaskInstance(task)
        ti.start()
        assert ti.state == State.STARTED
        assert ti.model_obj is not None
        assert ti.model_obj.state == State.STARTED

        ti.complete()
        ti_model_obj = DBObject.get(TaskInstanceModel, ti.db_id)
        assert ti_model_obj.state == State.COMPLETED
        assert ti.model_obj.state == State.COMPLETED

    def test_task_complete_before_start(self):
        task_args = {
            "task_name": "new task",
            "docker_url": "docker_url",
            "command": [],
            "start_at": None,
        }
        task = Task(**task_args)
        ti = TaskInstance(task)

        with pytest.raises(Exception):
            ti.complete()
            ti.stop()
