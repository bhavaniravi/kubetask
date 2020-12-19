import enum


class State(enum.Enum):
    NOT_STARTED = "NOT_STARTED"
    STARTED = "STARTED"
    SCHEDULED = "SCHEDULED"
    DEFERRED = "DEFERRED"
