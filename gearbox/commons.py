from enum import Enum

from pydantic import BaseModel


class ImmutableModel(BaseModel):
    class Config:
        allow_mutation = False


class DrivingMode(str, Enum):
    ECO = "ECO"
    COMFORT = "COMFORT"
    SPORT = "SPORT"


class AggressiveMode(Enum):
    Mode1 = 1
    Mode2 = 1.2
    Mode3 = 1.3


class EngineRPMS(ImmutableModel):
    value: float

    def __mul__(self, factor: float):
        return EngineRPMS(value=self.value * factor)

    def __attrs_post_init__(self):
        if self.value < 0:
            raise ValueError()

    def is_above(self, range: "RPMSRange") -> bool:
        return range.end_lower_than(self)

    def is_below(self, range: "RPMSRange") -> bool:
        return range.start_greater_than(self)


class RPMSRange(ImmutableModel):
    left: EngineRPMS
    right: EngineRPMS

    def start_greater_than(self, rpms: EngineRPMS) -> bool:
        return self.left.value > rpms.value

    def end_lower_than(self, rpms: EngineRPMS) -> bool:
        return self.right.value < rpms.value


class GasPressure(ImmutableModel):
    pressure: int

    KICKDOWN_TH = 50
    AGGR_KICKDOWN_TH = 70

    def __attrs_post_init__(self):
        if self.pressure < 0 or self.pressure > 100:
            raise ValueError()

    def is_kickdown(self):
        return self.pressure > self.KICKDOWN_TH

    def is_aggressive_kickdown(self):
        return self.pressure > self.AGGR_KICKDOWN_TH
