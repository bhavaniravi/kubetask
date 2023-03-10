import yaml

from kubetask.logger import logging
from kubetask.api.validators import TaskModel

import asyncio


async def parse_files(file):
    """Extract kubernetes jobspec details such as jobname to accomodate TaskModel
    taskname, tasktype, scheduled_at

    Args:
        file (_type_): _description_
    """
    data = yaml.full_load(file)
    try:
        new_data = {
            "task_name": data["metadata"]["name"],
            "task_type": data["kind"],
            "scheduled_at": data["spec"].get("schedule"),
        }

    except KeyError as e:
        raise KeyError(f"Invalid yaml file uploded \n {e}")
    model = TaskModel(**new_data)
    return model


def parse_cronjob_spec(file):
    pass


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    data = loop.run_until_complete(parse_files(open("k8_sample/sample_cronjob.yaml")))
    print(loop.run_until_complete(parse_files(open("k8_sample/sample_job.yaml"))))
