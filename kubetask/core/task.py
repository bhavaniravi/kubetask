from .task_instance import TaskInstance
from .constants import State
from kubetask.models.model import TaskModel
from kubetask.core.db import DB

class Task:
    def __init__(self, task_name, docker_url, command, schedule=None, start_at=None, task_id=None):
        if schedule and start_at:
            raise TypeError("A scheduled task cannot be deferred")

        self.task_id = None
        self.task_name = task_name
        self.docker_url = docker_url
        self.command = command
        self.schedule = schedule
        self.start_at = start_at
        self.state = State.NOT_STARTED
         

        self.task_model_obj = DB.create_or_get(TaskModel, self.task_id, vars(self))

        self.task_id = self.task_model_obj.task_id

    def schedule_task(self):
        self.state = State.SCHEDULED

    def defer(self):
        self.state = State.DEFERRED

    def _start_task(self):
        self.state = State.STARTED
        if self.schedule: 
            self.schedule_task() # create_a_cron_and_defer_execution
        elif self.start_at:
            self.defer() # create_a_cron_and_defer_execution

    def update_state(self):
        self.task_model_obj.state = self.state
        

    def start(self):
        """
        starts the task and returns a task instance.
        make_db_entry()

        

        return task_instance       
        """


        task_instance = self._start_task()

        self.update_state()
        return task_instance