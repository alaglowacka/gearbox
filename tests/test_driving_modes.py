import pytest

from gearbox.commons import DrivingMode, AggressiveMode, EngineRPMS
from gearbox.driving_modes import DrivingModeStrategy
from gearbox.gearbox_adapter import Gear
from tests.utils import GENTLE_PRESSURE, KICKDOWN


@pytest.mark.parametrize(
    "mode", (DrivingMode.SPORT, DrivingMode.COMFORT, DrivingMode.ECO)
)
def test_strategy_does_not_change_gear_when_proper_rpms(mode):
    strategy = DrivingModeStrategy.create(
        driving_mode=mode, aggressive_mode=AggressiveMode.Mode1
    )
    curr_gear = Gear(gear=2)

    gear_to_set = strategy.handle_gas(
        curr_gear=curr_gear, curr_rpm=EngineRPMS(value=2000), pressure=GENTLE_PRESSURE
    )

    assert gear_to_set == curr_gear


@pytest.mark.parametrize(
    "mode", (DrivingMode.SPORT, DrivingMode.COMFORT, DrivingMode.ECO)
)
def test_strategy_sets_previous_gear_when_rpms_below_range(mode):
    strategy = DrivingModeStrategy.create(
        driving_mode=mode, aggressive_mode=AggressiveMode.Mode1
    )
    curr_gear = Gear(gear=2)

    gear_to_set = strategy.handle_gas(
        curr_gear=curr_gear, curr_rpm=EngineRPMS(value=200), pressure=GENTLE_PRESSURE
    )

    assert gear_to_set == curr_gear.previous()


@pytest.mark.parametrize(
    "mode", (DrivingMode.SPORT, DrivingMode.COMFORT, DrivingMode.ECO)
)
def test_strategy_sets_next_gear_when_rpms_above_range(mode):
    strategy = DrivingModeStrategy.create(
        driving_mode=mode, aggressive_mode=AggressiveMode.Mode1
    )
    curr_gear = Gear(gear=2)

    gear_to_set = strategy.handle_gas(
        curr_gear=curr_gear, curr_rpm=EngineRPMS(value=5000), pressure=GENTLE_PRESSURE
    )

    assert gear_to_set == curr_gear.next()


@pytest.mark.parametrize(
    "mode, curr_rpms",
    (
        (DrivingMode.SPORT, 200),
        (DrivingMode.SPORT, 1500),
        (DrivingMode.SPORT, 5000),
        (DrivingMode.COMFORT, 200),
        (DrivingMode.COMFORT, 1500),
        (DrivingMode.COMFORT, 5000),
    ),
)
def test_strategy_sets_previous_gear_on_kickdown_no_matter_what_are_current_rpms(
    mode, curr_rpms
):
    strategy = DrivingModeStrategy.create(
        driving_mode=mode, aggressive_mode=AggressiveMode.Mode1
    )
    curr_gear = Gear(gear=2)

    gear_to_set = strategy.handle_gas(
        curr_gear=curr_gear, curr_rpm=EngineRPMS(value=curr_rpms), pressure=KICKDOWN
    )

    assert gear_to_set == curr_gear.previous()
