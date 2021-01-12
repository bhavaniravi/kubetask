from kubetask.core.constants import State

class TaskInstance:
    def __init__(self, task):
        self.task = task
        self.state = None
        self.start_ts = None
        self.end_ts = None