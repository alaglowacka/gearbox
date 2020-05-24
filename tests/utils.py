from unittest.mock import create_autospec

from gearbox.commons import DrivingMode, EngineRPMS, GasPressure
from gearbox.gearbox import Gearbox
from gearbox.gearbox_adapter import GearboxAdapter, Gear
from gearbox.gearbox_driver import GearboxDriver, RPMProvider

GENTLE_PRESSURE = GasPressure(pressure=30)
KICKDOWN = GasPressure(pressure=60)
AGGRESIVE_KICKDOWN = GasPressure(pressure=80)
RPMS_ABOVE_SPORT_MODE_THRESHOLD = EngineRPMS(value=5000)


def create_gearbox():
    class GearBuilder:
        def __init__(self):
            self._curr_gear = Gear(gear=1)
            self._max_gear = Gear(gear=5)
            self._mode = DrivingMode.ECO

        def with_max_gear(self, max_gear: Gear):
            self._max_gear = max_gear
            return self

        def with_gear(self, gear: Gear):
            self._curr_gear = gear
            return self

        def build(self):
            gearbox = GearboxAdapter(Gearbox(), max_gear=self._max_gear)
            gearbox.change_gear(self._curr_gear)
            return gearbox

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


def assert_max_gear_is_set(gearbox, max_gear: Gear):
    assert gearbox.current_gear == max_gear


def assert_gear_was_increased(gearbox, initial_gear: Gear):
    assert gearbox.current_gear == initial_gear.next()


def assert_gear_was_reduced(gearbox, initial_gear: Gear):
    assert gearbox.current_gear == initial_gear.previous()


def assert_gear_was_reduced_twice(gearbox, initial_gear: Gear):
    assert gearbox.current_gear == initial_gear.previous().previous()


def assert_gear_was_not_changed(gearbox, initial_gear: Gear):
    assert gearbox.current_gear == initial_gear
