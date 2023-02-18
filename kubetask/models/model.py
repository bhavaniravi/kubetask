from typing import List
from typing import Optional
from sqlalchemy import ForeignKey, String, create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import MetaData

from sqlalchemy.types import DateTime, ARRAY, Enum
from kubetask.core.constants import State, Priority
from kubetask.core.config import config as kubetask_config
from kubetask.utils import utils


engine = create_engine(kubetask_config.KUBETASK_DB)


class Base(DeclarativeBase):
    pass


class TaskModel(Base):
    __tablename__ = "task"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    task_name: Mapped[str] = mapped_column(String)
    schedule_at: Mapped[str] = mapped_column(String, nullable=True)
    docker_url: Mapped[str] = mapped_column(String)
    command: Mapped[str] = mapped_column(ARRAY(String), nullable=True)
    start_at = mapped_column(DateTime)
    task_instances = relationship(
        "TaskInstanceModel", back_populates="task", passive_deletes=True
    )

    def __repr__(self):
        return "<Task(task_id='%s', task_name='%s', schedule='%s')>" % (
            self.task_id,
            self.task_name,
            self.schedule_at,
        )


class TaskInstanceModel(Base):
    __tablename__ = "task_instance"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    task_id: Mapped[int] = mapped_column(ForeignKey("task.id"))
    start_ts = mapped_column(DateTime, nullable=True)
    end_ts = mapped_column(DateTime, nullable=True)
    task = relationship(
        "TaskModel", back_populates="task_instances", passive_deletes=True
    )
    state = mapped_column(Enum(State), default=State.NOT_STARTED)


if __name__ == "__main__":
    Base.metadata.drop_all(engine)
    # Base.metadata.create_all(engine)
