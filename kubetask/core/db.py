from kubetask.core.config import get_config

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


Config = get_config()
engine = create_engine(Config.KUBETASK_DB)
Session = sessionmaker(bind=engine)

from contextlib import contextmanager

@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    session.expire_on_commit = False
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.expunge_all()
        session.close()


class DB:

    @classmethod
    def create(cls, ModelClass, kwargs):
        with session_scope() as session:
            model_obj = ModelClass(**kwargs)
            session.add(model_obj)
        return model_obj

    @classmethod
    def get(cls, ModelClass, primary_key, session=None):
        session = session or session_scope()
        return session.query(ModelClass).get(primary_key)

    @classmethod
    def create_or_get(cls, ModelClass, primary_key, params):
        if not primary_key:
            return cls.create(ModelClass, params)
        return cls.get(ModelClass, primary_key)


    def filter(cls, ModelClass, filter_dict):
        with session_scope() as session:
            return session.query(ModelClass).filter_by(**filter_dict)

