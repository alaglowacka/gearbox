from unittest.mock import create_autospec

from gearbox.commons import DrivingMode, EngineRPMS
from gearbox.external_systems import ExternalSystems
from gearbox.gearbox import Gearbox
from gearbox.gearbox_adapter import GearboxAdapter
from gearbox.gearbox_driver import GearboxDriver


def create_gearbox():
    class GearBuilder:
        def __init__(self):
            self._gearbox = GearboxAdapter(Gearbox())
            self._gear = 1
            self._mode = DrivingMode.ECO

        def with_gear(self, gear: int):
            for _ in range(1, gear):
                self._gearbox.increase_gear()
            return self

        def build(self):
            return self._gearbox

    return GearBuilder()


def create_gearbox_driver(gearbox: GearboxAdapter):
    class GearDriverBuilder:
        def __init__(self):
            self._gearbox = gearbox
            self._external_systems = create_autospec(ExternalSystems())
            self._mode = None

        def with_sport_mode(self):
            self._mode = DrivingMode.SPORT
            return self

        def with_engine_at(self, rpms: EngineRPMS):
            self._external_systems.get_current_rpm.return_value = rpms
            return self

        def build(self):
            driver = GearboxDriver(self._gearbox, self._external_systems)
            if self._mode:
                driver.change_mode(self._mode)
            return driver

    return GearDriverBuilder()