import os
import shutil

from sqlalchemy import create_engine
from kubetask.core.config import get_config

kubetask_config = get_config()

def reset_alembic():
    path = 'alembic/versions/'
    shutil.rmtree(path)
    os.makedirs(path)

    DB = kubetask_config.KUBETASK_DB
    engine = create_engine(DB)
    with engine.connect() as conn:
        conn.execute("TRUNCATE TABLE alembic_version")
        
if __name__ == '__main__':
    reset_alembic()