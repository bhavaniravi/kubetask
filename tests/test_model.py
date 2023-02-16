import pytest
import datetime
from kubetask.models.model import TaskModel
from kubetask.core.constants import State
from test_core import task_list
from kubetask.core.config import UTConfig

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


class TestTaskModel:
    @classmethod
    def setup_class(cls):
        engine = create_engine(UTConfig.KUBETASK_DB)
        cls.Session = sessionmaker(bind=engine)

    @pytest.mark.parametrize(
        "arguments",
        [
            (task_list[0]),
            (task_list[1]),
            (task_list[2]),
        ],
    )
    def test_task_create(self, arguments):
        task = TaskModel(**arguments)
        session = self.Session()
        session.add(task)

        for key, value in arguments.items():
            assert getattr(task, key) == value
        
        session.commit()
