from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.types import DateTime, ARRAY, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


from kubetask.core.constants import State, Priority
from kubetask.utils import utils

Base = declarative_base()

ENUM_TYPE = Enum(State)

class TaskModel(Base):
    __tablename__ = "task"

    task_id = Column(Integer, primary_key=True, autoincrement=True)
    task_name = Column(String)
    schedule_at = Column(String)
    docker_url = Column(String)
    command = Column(ARRAY(String))
    start_at = Column(DateTime)
    state = Column(ENUM_TYPE)
    priority = Column(Enum(Priority))
    task_instances = relationship("TaskInstanceModel", back_populates="task")

    def __repr__(self):
        return "<Task(task_id='%s', task_name='%s', schedule='%s')>" % (
            self.task_id,
            self.task_name,
            self.schedule_at,
        )

class TaskInstanceModel(Base):
    __tablename__ = "task_instance"

    id = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(Integer, ForeignKey('task.task_id'))
    start_ts = Column(DateTime)
    end_ts = Column(DateTime)
    task = relationship("TaskModel", back_populates="task_instances")
    state = Column(ENUM_TYPE)