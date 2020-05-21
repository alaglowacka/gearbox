from unittest.mock import create_autospec

from gearbox.commons import DrivingMode, EngineRPMS
from gearbox.gearbox import Gearbox
from gearbox.gearbox_adapter import GearboxAdapter, Gear
from gearbox.gearbox_driver import GearboxDriver, RPMProvider


def create_gearbox():
    class GearBuilder:
        def __init__(self):
            self._gearbox = GearboxAdapter(Gearbox())
            self._gear = Gear(gear=1)
            self._mode = DrivingMode.ECO

        def with_gear(self, gear: Gear):
            self._gearbox.change_gear(gear)
            return self

        def build(self):
            return self._gearbox

    return GearBuilder()


def create_gearbox_driver(gearbox: GearboxAdapter):
    class GearDriverBuilder:
        def __init__(self):
            self._gearbox = gearbox
            self._rpm_provider = create_autospec(RPMProvider)
            self._mode = None

        def with_sport_mode(self):
            self._mode = DrivingMode.SPORT
            return self

        def with_engine_at(self, rpms: EngineRPMS):
            self._rpm_provider.current_rpms.return_value = rpms
            return self

        def build(self):
            driver = GearboxDriver(self._gearbox, self._rpm_provider)
            if self._mode:
                driver.change_mode(self._mode)
            return driver

    return GearDriverBuilder()
