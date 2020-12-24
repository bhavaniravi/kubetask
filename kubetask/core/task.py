# from .task_instance import TaskInstance
from .constants import State, Priority
from kubetask.models.model import TaskModel, TaskInstanceModel
from kubetask.core.db import DB

def update_state(func) : 
    def caller(self) : 
        func(self) 
        self.model_obj.state = self.state
    return caller 

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

    @update_state
    def schedule(self):
        self.state = State.SCHEDULED

    @update_state
    def defer(self):
        self.state = State.DEFERRED

    @update_state
    def stop(self):
        self.state = State.STOPPED
        
    @update_state
    def start(self):
        self.state = State.STARTED
        task_instance = TaskInstance(self)
        return task_instance

    



class TaskInstance:
    def __init__(self, task, id=None):
        self.id = id
        self.task = task
        self.state = State.NOT_STARTED
        self.start_ts = None
        self.end_ts = None
        self.model_obj = None

    def check_start(func) : 
        def caller(self) : 
            if not self.model_obj:
                raise Exception("Task instance not started yet")
            func(self) 
        return caller 

    def create_db_object(self):
        kwargs = vars(self).copy()
        kwargs["task"] = self.task.model_obj
        kwargs.pop("model_obj")
        self.model_obj = DB.create(TaskInstanceModel, kwargs)

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
        """Update DB that the task is complete
        """
        self.state = State.COMPLETED

    


