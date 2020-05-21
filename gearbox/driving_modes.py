from gearbox.commons import (
    DrivingMode,
    AggressiveGearChangeUpThreshold,
    GasPressure,
    GearChangeUpThreshold,
    EngineRPMS,
    AggressiveMode,
    GearChangeDownThreshold,
)
from gearbox.gearbox_adapter import Gear


class DrivingModeStrategy:
    MODE = None

    def __init__(
        self, aggressive_mode=AggressiveMode.Mode1,
    ):
        self._aggressive_mode = aggressive_mode

    def handle_gas(
        self, curr_gear: Gear, curr_rpm: EngineRPMS, pressure: GasPressure
    ) -> Gear:
        raise NotImplementedError

    def change_driving_mode(self, new_mode: DrivingMode) -> 'DrivingModeStrategy':
        if new_mode == self.MODE:
            return self
        if new_mode == DrivingMode.SPORT:
            return SportStrategy(self._aggressive_mode)
        if new_mode == DrivingMode.COMFORT:
            return ComfortStrategy(self._aggressive_mode)
        return EcoStrategy(self._aggressive_mode)

    def change_aggressive_mode(self, new_aggressive_mode: AggressiveMode):
        self._aggressive_mode = new_aggressive_mode


class SportStrategy(DrivingModeStrategy):
    MODE = DrivingMode.SPORT
    CHANGE_GEAR_UP_THRESHOLD = AggressiveGearChangeUpThreshold(
        th=EngineRPMS(value=4500.0)
    )
    CHANGE_GEAR_DOWN_THRESHOLD = GearChangeDownThreshold(th=EngineRPMS(value=1500.0))

    def handle_gas(
        self, curr_gear: Gear, curr_rpm: EngineRPMS, pressure: GasPressure
    ) -> Gear:
        if pressure.is_aggressive_kickdown():
            return curr_gear.previous().previous()
        elif pressure.is_kickdown():
            return curr_gear.previous()
        else:
            if self.CHANGE_GEAR_UP_THRESHOLD.is_exceeded(
                curr_rpm, self._aggressive_mode
            ):
                return curr_gear.next()
            if self.CHANGE_GEAR_DOWN_THRESHOLD.is_exceeded(curr_rpm):
                return curr_gear.previous()


class ComfortStrategy(DrivingModeStrategy):
    MODE = DrivingMode.COMFORT
    CHANGE_GEAR_UP_THRESHOLD = AggressiveGearChangeUpThreshold(
        th=EngineRPMS(value=2500.0)
    )
    CHANGE_GEAR_DOWN_THRESHOLD = GearChangeDownThreshold(th=EngineRPMS(value=1000.0))

    def handle_gas(
        self, curr_gear: Gear, curr_rpm: EngineRPMS, pressure: GasPressure
    ) -> Gear:
        if pressure.is_kickdown():
            return curr_gear.previous()
        else:
            if self.CHANGE_GEAR_UP_THRESHOLD.is_exceeded(
                curr_rpm, self._aggressive_mode
            ):
                return curr_gear.next()
            if self.CHANGE_GEAR_DOWN_THRESHOLD.is_exceeded(curr_rpm):
                return curr_gear.previous()


class EcoStrategy(DrivingModeStrategy):
    MODE = DrivingMode.ECO
    CHANGE_GEAR_UP_THRESHOLD = GearChangeUpThreshold(th=EngineRPMS(value=2000.0))
    CHANGE_GEAR_DOWN_THRESHOLD = GearChangeDownThreshold(th=EngineRPMS(value=1000.0))

    def handle_gas(
        self, curr_gear: Gear, curr_rpm: EngineRPMS, pressure: GasPressure
    ) -> Gear:
        if self.CHANGE_GEAR_UP_THRESHOLD.is_exceeded(curr_rpm):
            return curr_gear.next()
        if self.CHANGE_GEAR_DOWN_THRESHOLD.is_exceeded(curr_rpm):
            return curr_gear.previous()
