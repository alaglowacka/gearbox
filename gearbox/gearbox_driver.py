from gearbox.commons import DrivingMode, GasPressure, EngineRPMS
from gearbox.driving_modes import ComfortStrategy
from gearbox.external_systems import ExternalSystems
from gearbox.gearbox_adapter import GearboxState, GearboxAdapter


class GearboxDriver:
    def __init__(
        self, gearbox: GearboxAdapter, external_systems: ExternalSystems
    ):
        self._gearbox = gearbox
        self._external_systems = external_systems
        self._strategy = ComfortStrategy(self._gearbox)

    def handle_gas(self, pressure: GasPressure):
        if self._gearbox.get_state() != GearboxState.DRIVE:
            return

        curr_rpm = self._external_systems.get_current_rpm()
        self._strategy.handle_gas(curr_rpm=curr_rpm, pressure=pressure)

    def change_mode(self, new_mode: DrivingMode):
        self._strategy = self._strategy.change_driving_mode(new_mode)

    def increase_gear(self):
        self._gearbox.increase_gear()

    def decrease_gear(self):
        self._gearbox.decrease_gear()


class RPMProvider:
    def __init__(self, external_systems: ExternalSystems):
        self._external_systems = external_systems

    def current_rpms(self) -> EngineRPMS:
        return self._external_systems.get_current_rpm()