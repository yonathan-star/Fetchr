from enum import Enum, auto


class RoverState(Enum):
    IDLE = auto()
    FOLLOW_OWNER = auto()
    WASTE_SCAN = auto()
    APPROACH_TARGET = auto()
    COLLECT_SEQUENCE = auto()
    RETURN_TO_DOCK = auto()
    DOCKED_ANALYZE = auto()
    FAULT = auto()
