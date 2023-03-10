from pydantic import BaseModel, ValidationError, validator
from typing import Optional


class TaskModel(BaseModel):
    task_name: str
    task_type: Optional[str]
    scheduled_at: Optional[str]

    @validator("scheduled_at")
    def scheduled_at_should_have_value_if_cron_job(cls, v, values):
        if values["task_type"] == "CronJob":
            if v is None or v == "":
                raise ValueError("CronJob needs a schedule")
        return v
