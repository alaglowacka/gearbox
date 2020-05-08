from gearbox.commons import (
    DrivingMode,
    AggressiveGearChangeUpThreshold,
    GasPressure,
    GearChangeUpThreshold,
    EngineRPMS,
    AggressiveMode,
    GearChangeDownThreshold,
)
from gearbox.external_systems import ExternalSystems
from gearbox.gearbox_adapter import GearboxAdapter


class DrivingModeStrategy:
    MODE = None

    def __init__(
        self,
        gearbox: GearboxAdapter,
        external_systems: ExternalSystems,
        aggressive_mode=AggressiveMode.Mode1,
    ):
        self._gearbox = gearbox
        self._external_systems = external_systems
        self._aggressive_mode = aggressive_mode

    def handle_gas(self, pressure: GasPressure):
        raise NotImplementedError

    def change_driving_mode(self, new_mode: DrivingMode) -> 'Strategy':
        if new_mode == self.MODE:
            return self
        if new_mode == DrivingMode.SPORT:
            return SportStrategy(
                self._gearbox, self._external_systems, self._aggressive_mode
            )
        if new_mode == DrivingMode.COMFORT:
            return ComfortStrategy(
                self._gearbox, self._external_systems, self._aggressive_mode
            )
        return EcoStrategy(
            self._gearbox, self._external_systems, self._aggressive_mode
        )

    def change_aggressive_mode(self, new_aggressive_mode: AggressiveMode):
        self._aggressive_mode = new_aggressive_mode


class SportStrategy(DrivingModeStrategy):
    MODE = DrivingMode.SPORT
    CHANGE_GEAR_UP_THRESHOLD = AggressiveGearChangeUpThreshold(
        th=EngineRPMS(value=4500.0)
    )
    CHANGE_GEAR_DOWN_THRESHOLD = GearChangeDownThreshold(
        th=EngineRPMS(value=1500.0)
    )

    def handle_gas(self, pressure: GasPressure):
        if pressure.is_aggressive_kickdown():
            self._gearbox.decrease_gear()
            self._gearbox.decrease_gear()
        elif pressure.is_kickdown():
            self._gearbox.decrease_gear()
        else:
            curr_rpm = self._external_systems.get_current_rpm()
            if self.CHANGE_GEAR_UP_THRESHOLD.is_exceeded(
                curr_rpm, self._aggressive_mode
            ):
                self._gearbox.increase_gear()
            if self.CHANGE_GEAR_DOWN_THRESHOLD.is_exceeded(curr_rpm):
                self._gearbox.decrease_gear()


class ComfortStrategy(DrivingModeStrategy):
    MODE = DrivingMode.COMFORT
    CHANGE_GEAR_UP_THRESHOLD = AggressiveGearChangeUpThreshold(
        th=EngineRPMS(value=2500.0)
    )
    CHANGE_GEAR_DOWN_THRESHOLD = GearChangeDownThreshold(
        th=EngineRPMS(value=1000.0)
    )

    def handle_gas(self, pressure: GasPressure):
        if pressure.is_kickdown():
            self._gearbox.decrease_gear()
        else:
            curr_rpm = self._external_systems.get_current_rpm()
            if self.CHANGE_GEAR_UP_THRESHOLD.is_exceeded(
                curr_rpm, self._aggressive_mode
            ):
                self._gearbox.increase_gear()
            if self.CHANGE_GEAR_DOWN_THRESHOLD.is_exceeded(curr_rpm):
                self._gearbox.decrease_gear()


class EcoStrategy(DrivingModeStrategy):
    MODE = DrivingMode.ECO
    CHANGE_GEAR_UP_THRESHOLD = GearChangeUpThreshold(
        th=EngineRPMS(value=2000.0)
    )
    CHANGE_GEAR_DOWN_THRESHOLD = GearChangeDownThreshold(
        th=EngineRPMS(value=1000.0)
    )

    def handle_gas(self, pressure: GasPressure):
        curr_rpm = self._external_systems.get_current_rpm()
        if self.CHANGE_GEAR_UP_THRESHOLD.is_exceeded(curr_rpm):
            self._gearbox.increase_gear()
        if self.CHANGE_GEAR_DOWN_THRESHOLD.is_exceeded(curr_rpm):
            self._gearbox.decrease_gear()
