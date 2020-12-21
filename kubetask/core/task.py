from .task_instance import TaskInstance
from .constants import State, Priority
from kubetask.models.model import TaskModel
from kubetask.core.db import DB

class Task:
    def __init__(self, task_name, docker_url, command, schedule_at=None, start_at=None, priority=None, task_id=None):
        if schedule_at and start_at:
            raise TypeError("A scheduled task cannot be deferred")

        self.task_id = None
        self.task_name = task_name
        self.docker_url = docker_url
        self.command = command
        self.schedule_at = schedule_at
        self.start_at = start_at
        self.state = State.NOT_STARTED
        self.priority = priority or Priority.LOW.value

        if self.priority not in Priority:
            raise AttributeError(f"Invalid value for priority {self.priority}")
        self.model_obj = DB.create_or_get(TaskModel, self.task_id, vars(self))

        self.task_id = self.model_obj.task_id

    def update_state(func) : 
        def caller(self) : 
            func(self) 
            self.model_obj.state = self.state
        return caller 

    @update_state
    def schedule(self):
        self.state = State.SCHEDULED

    @update_state
    def defer(self):
        self.state = State.DEFERRED
        
    @update_state
    def start(self):
        self.state = State.STARTED
        task_instance = TaskInstance(self)
        return task_instance