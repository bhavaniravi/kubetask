import enum

class BaseEnumMeta(enum.EnumMeta): 
    def __contains__(cls, item): 
        return item in [v.value for v in cls.__members__.values()] 


class State(enum.Enum, metaclass=BaseEnumMeta):
    NOT_STARTED = "NOT_STARTED"
    STARTED = "STARTED"
    SCHEDULED = "SCHEDULED"
    DEFERRED = "DEFERRED"
    COMPLETED = "COMPLETED"
    STOPPED = 'STOPPED'


class Priority(enum.Enum, metaclass=BaseEnumMeta):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    HIGHEST = "HIGHEST"
