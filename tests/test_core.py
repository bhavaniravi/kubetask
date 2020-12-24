import pytest
import datetime
from kubetask.core.config import Config
from kubetask.core.task import Task, TaskInstance
from kubetask.core.constants import State


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
        "priority": "HIGH",
        "start_at": datetime.datetime.utcnow(),
    },
    
]

error_tasks = [
    {
            "task_id": "task_002",
            "task_name": "new task 1",
            "docker_url": "docker_url 1",
            "command": ["python", "setup.py"],
            "schedule_at": "@daily",
            "start_at": datetime.datetime.utcnow(),
        },
    {
        "task_name": "new task 1",
        "docker_url": "docker_url 1",
        "command": ["python", "setup.py"],
        "priority": "BLAH",
        "start_at": datetime.datetime.utcnow(),
    },

]


class TestTask:
    @pytest.mark.parametrize(
        "arguments, error", 
        [
            (error_tasks[0], TypeError),
            (error_tasks[1], AttributeError),
        ],
    )
    def test_init_type_error(self, arguments, error):
        with pytest.raises(error):
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
        "arguments, func, state",
        [
            (task_list[0], "start", State.STARTED),
            (task_list[1], "schedule", State.SCHEDULED),
            (task_list[2], "defer", State.DEFERRED),
        ],
    )
    def test_task_start(self, arguments, func, state):
        task = Task(**arguments)
        getattr(Task, func)(task)
        assert task.state == state
        assert task.task_id is not None


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


        