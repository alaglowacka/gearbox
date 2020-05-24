from gearbox.commons import (
    DrivingMode,
    EngineRPMS,
    AggressiveMode,
    RPMSRange, GasPressure)
from gearbox.gearbox_adapter import Gear


class GearChangeThresholdProvider:
    THRESHOLDS = {
        DrivingMode.SPORT: (EngineRPMS(value=1500), EngineRPMS(value=4500)),
        DrivingMode.COMFORT: (EngineRPMS(value=1000), EngineRPMS(value=2500)),
        DrivingMode.ECO: (EngineRPMS(value=1000), EngineRPMS(value=2000)),
    }

    @classmethod
    def for_mode(cls, driving_mode: DrivingMode, aggressive_mode: AggressiveMode = None) -> RPMSRange:
        left, right = cls.THRESHOLDS[driving_mode]
        if aggressive_mode:
            right *= aggressive_mode.value
        return RPMSRange(left=left, right=right)


class DrivingModeStrategy:
    MODE = None

    def handle_gas(
            self, curr_gear: Gear, curr_rpm: EngineRPMS, pressure: GasPressure
    ) -> Gear:
        raise NotImplementedError

    @classmethod
    def create(
            cls,
            driving_mode: DrivingMode,
            aggressive_mode: AggressiveMode = AggressiveMode.Mode1
    ) -> "DrivingModeStrategy":
        if driving_mode == DrivingMode.SPORT:
            return SportStrategy(aggressive_mode)
        if driving_mode == DrivingMode.COMFORT:
            return ComfortStrategy(aggressive_mode)
        return EcoStrategy()


class SportStrategy(DrivingModeStrategy):
    MODE = DrivingMode.SPORT

    def __init__(
            self, aggressive_mode=AggressiveMode.Mode1,
    ):
        self._rpsm_range = GearChangeThresholdProvider.for_mode(self.MODE, aggressive_mode)

    def handle_gas(
            self, curr_gear: Gear, curr_rpm: EngineRPMS, pressure: GasPressure
    ) -> Gear:
        if pressure.is_aggressive_kickdown():
            return curr_gear.previous().previous()
        elif pressure.is_kickdown():
            return curr_gear.previous()
        else:
            if curr_rpm.is_above(self._rpsm_range):
                return curr_gear.next()
            if curr_rpm.is_below(self._rpsm_range):
                return curr_gear.previous()


class ComfortStrategy(DrivingModeStrategy):
    MODE = DrivingMode.COMFORT

    def __init__(
            self, aggressive_mode=AggressiveMode.Mode1,
    ):
        self._rpsm_range = GearChangeThresholdProvider.for_mode(self.MODE, aggressive_mode)

    def handle_gas(
            self, curr_gear: Gear, curr_rpm: EngineRPMS, pressure: GasPressure
    ) -> Gear:
        if pressure.is_kickdown():
            return curr_gear.previous()
        else:
            if curr_rpm.is_above(self._rpsm_range):
                return curr_gear.next()
            if curr_rpm.is_below(self._rpsm_range):
                return curr_gear.previous()


class EcoStrategy(DrivingModeStrategy):
    MODE = DrivingMode.ECO

    def __init__(self):
        self._rpsm_range = GearChangeThresholdProvider.for_mode(self.MODE)

    def handle_gas(
            self, curr_gear: Gear, curr_rpm: EngineRPMS, pressure: GasPressure
    ) -> Gear:
        if curr_rpm.is_above(self._rpsm_range):
            return curr_gear.next()
        if curr_rpm.is_below(self._rpsm_range):
            return curr_gear.previous()
