from kubetask.core.constants import State
from kubetask.models.model import TaskInstanceModel
from kubetask.core.db import DB

class TaskInstance:
    def __init__(self, task, id=None):
        self.id = id
        self.task = task
        self.state = State.NOT_STARTED
        self.start_ts = None
        self.end_ts = None
        self.model_obj = None

    def update_state(func) : 
        def caller(self) : 
            func(self) 
            self.model_obj.state = self.state
        return caller 

    def push_to_queue(self):
        pass

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
        

    @update_state
    def complete(self):
        """Update DB that the task is complete
        """
        self.state = State.COMPLETED

