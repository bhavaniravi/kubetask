from sqlalchemy import Column, Integer, String
from sqlalchemy.types import DateTime, ARRAY, Enum
from sqlalchemy.ext.declarative import declarative_base


from kubetask.core.constants import State, Priority
from kubetask.utils import utils

Base = declarative_base()

class TaskModel(Base):
    __tablename__ = "task"

    task_id = Column(Integer, primary_key=True, autoincrement=True)
    task_name = Column(String)
    schedule = Column(String)
    docker_url = Column(String)
    command = Column(ARRAY(String))
    start_at = Column(DateTime)
    state = Column(Enum(State))
    priority = Column(Enum(Priority))

    def __repr__(self):
        return "<Task(task_id='%s', task_name='%s', schedule='%s')>" % (
            self.task_id,
            self.task_name,
            self.schedule,
        )