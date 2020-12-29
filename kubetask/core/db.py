from kubetask.core.config import get_config

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


Config = get_config()
engine = create_engine(Config.KUBETASK_DB)
Session = sessionmaker(bind=engine, expire_on_commit = False)

from contextlib import contextmanager

@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.flush()
        session.expunge_all()
        session.close()

def for_all_methods(decorator):
    def decorate(cls):
        for attr in cls.__dict__: # there's propably a better way to do this
            if callable(getattr(cls, attr)):
                setattr(cls, attr, decorator(getattr(cls, attr)))
        return cls
    return decorate



class DB:
    def create(self, ModelClass, kwargs):
        with session_scope() as session:
            model_obj = ModelClass(**kwargs)
            session.add(model_obj)
            return model_obj

    def get(self, ModelClass, primary_key):
        with session_scope() as session:
            return session.query(ModelClass).get(primary_key)

    def create_or_get(self, ModelClass, primary_key, params):
        if not primary_key:
            return self.create(ModelClass, params)
        return self.get(ModelClass, primary_key)

    def filter(self, ModelClass, filter_dict):
        with session_scope() as session:
            session.query(ModelClass).filter_by(**filter_dict)

    def update(self, ModelClass, filter_dict, update_dict):
        with session_scope() as session:
            rs = session.query(ModelClass).filter_by(**filter_dict).update(update_dict)


