# from .task_instance import TaskInstance
from .constants import State, Priority
from kubetask.models.model import TaskModel, TaskInstanceModel
from kubetask.core.db import DB
from sqlalchemy.inspection import inspect

DBObject = DB()


def update_state(func):
    def caller(self):
        func(self)
        ModelClass = globals()[f"{self.__class__.__name__}Model"]
        DBObject.update(ModelClass, {"id": self.db_id}, {"state": self.state})

    return caller


class Task:
    def __init__(
        self,
        task_name,
        docker_url,
        command,
        schedule_at=None,
        start_at=None,
        priority=None,
        task_id=None,
    ):
        if schedule_at and start_at:
            raise TypeError("A scheduled task cannot be deferred")

        self.db_id = None
        self.task_name = task_name
        self.docker_url = docker_url
        self.command = command
        self.schedule_at = schedule_at
        self.start_at = start_at

        args = vars(self).copy()
        args.pop("db_id")
        model_obj = DBObject.create_or_get(TaskModel, self.db_id, args)
        self.db_id = model_obj.id

    def get_model_obj(self):
        return DBObject.get(TaskModel, self.db_id)

    def start(self):
        task_instance = TaskInstance(self)
        task_instance.start()
        return task_instance

    @property
    def model_obj(self):
        return DB.get(TaskModel, self.db_id)


class TaskInstance:
    def __init__(self, task, db_id=None):
        self.db_id = id
        self.task = task
        self.state = State.NOT_STARTED
        self.start_ts = None
        self.end_ts = None

    @property
    def model_obj(self):
        return DBObject.get(TaskInstanceModel, self.db_id)

    def check_start(func):
        def caller(self):
            if not self.db_id:
                raise Exception("Task instance not started yet")
            func(self)

        return caller

    def create_db_object(self):
        kwargs = vars(self).copy()
        kwargs.pop("db_id")
        kwargs["task"] = self.task.get_model_obj()
        model_obj = DBObject.create(TaskInstanceModel, kwargs)
        self.db_id = model_obj.id

    def start(self):
        """starts the execution of the task
        1. push the task to the queue
        2. Update DB with task instance details
        """
        self.state = State.STARTED
        self.create_db_object()

    @check_start
    @update_state
    def stop(self):
        self.state = State.STOPPED

    @check_start
    @update_state
    def complete(self):
        """Update DB that the task is complete"""
        self.state = State.COMPLETED
