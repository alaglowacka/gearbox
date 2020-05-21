from gearbox.commons import DrivingMode, GasPressure, EngineRPMS, AggressiveMode
from gearbox.driving_modes import DrivingModeStrategy
from gearbox.external_systems import ExternalSystems
from gearbox.gearbox_adapter import GearboxState, GearboxAdapter


class RPMProvider:
    def __init__(self, external_systems: ExternalSystems):
        self._external_systems = external_systems

    def current_rpms(self) -> EngineRPMS:
        return self._external_systems.get_current_rpm()


class GearboxDriver:
    def __init__(self, gearbox: GearboxAdapter, rpm_provider: RPMProvider):
        self._gearbox = gearbox
        self._rpm_provider = rpm_provider
        self._strategy = DrivingModeStrategy.create(DrivingMode.COMFORT)

    def handle_gas(self, pressure: GasPressure):
        if self._gearbox.get_state() != GearboxState.DRIVE:
            return

        curr_rpm = self._rpm_provider.current_rpms()
        gear = self._strategy.handle_gas(
            curr_gear=self._gearbox.current_gear,
            curr_rpm=curr_rpm,
            pressure=pressure
        )
        self._gearbox.change_gear(gear)

    def change_mode(self, new_mode: DrivingMode):
        self._strategy = DrivingModeStrategy.create(new_mode)

    def change_aggressiveness(self, new_mode: AggressiveMode):
        self._strategy = DrivingModeStrategy.create(self._strategy.MODE, new_mode)

    def increase_gear(self):
        self._gearbox.increase_gear()

    def decrease_gear(self):
        self._gearbox.decrease_gear()
