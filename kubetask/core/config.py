from dotenv import load_dotenv
import os

load_dotenv()

class BaseConfig:
    pass

class LocalConfig:
    pass

class Config(BaseConfig):
    pass

class UTConfig(BaseConfig):
    KUBETASK_DB = "postgresql://bhavaniravi:admin@localhost:5432/kubetask"


def get_config():
    env = os.environ["ENV"]
    
    load_dotenv(f"{env}.env")
    return globals()[f"{env}Config"]

config = get_config()