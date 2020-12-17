from .task_instance import TaskInstance
from .constants import State
class Task:
    def __init__(self, task_id, task_name, docker_url, command, schedule=None, start_at=None):
        if schedule and start_at:
            raise TypeError("A scheduled task cannot be deferred")

        self.task_id = task_id
        self.task_name = task_name
        self.docker_url = docker_url
        self.command = command
        self.schedule = schedule
        self.start_at = start_at
        self.state = State.NOT_STARTED

    def _schedule(self):
        self.state = State.SCHEDULED

    def _defer(self):
        self.state = State.DEFERRED

    def _start_task(self):
        self.state = State.STARTED


    def start(self):
        """
        starts the task and returns a task instance.
        make_db_entry()

        

        return task_instance       
        """
        if self.schedule: 
            task_instance = self._schedule() # create_a_cron_and_defer_execution
        elif self.start_at:
            task_instance = self._defer() # create_a_cron_and_defer_execution
        else:
            task_instance = self._start_task()
        return TaskInstance()