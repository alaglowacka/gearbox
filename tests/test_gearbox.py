from gearbox.commons import GasPressure, EngineRPMS
from tests.utils import create_gearbox, create_gearbox_driver

GENTLE_PRESSURE = GasPressure(pressure=30)
KICKDOWN = GasPressure(pressure=60)
AGGRESIVE_KICKDOWN = GasPressure(pressure=80)
RPMS_ABOVE_SPORT_MODE_THRESHOLD = EngineRPMS(value=5000)


def test_gear_cannot_exceed_range():
    gearbox = create_gearbox().with_gear(1).build()
    gearbox_driver = create_gearbox_driver(gearbox).build()

    for x in range(10):
        gearbox_driver.increase_gear()
    assert_max_gear_is_set(gearbox)


def test_gear_is_changed_when_threshold_is_exceeded():
    initial_gear = 1
    gearbox = create_gearbox().with_gear(initial_gear).build()
    gearbox_driver = (
        create_gearbox_driver(gearbox)
        .with_engine_at(RPMS_ABOVE_SPORT_MODE_THRESHOLD)
        .build()
    )

    gearbox_driver.handle_gas(pressure=GENTLE_PRESSURE)

    assert_gear_was_increased(gearbox, initial_gear)


def test_gear_is_reduced_when_kickdown():
    initial_gear = 4
    gearbox = create_gearbox().with_gear(initial_gear).build()
    gearbox_driver = create_gearbox_driver(gearbox).with_sport_mode().build()

    gearbox_driver.handle_gas(pressure=KICKDOWN)

    assert_gear_was_reduced(gearbox, initial_gear)


def test_gear_is_not_reduced_when_kickdown_on_lowest_gear():
    initial_gear = 1
    gearbox = create_gearbox().with_gear(initial_gear).build()
    gearbox_driver = create_gearbox_driver(gearbox).with_sport_mode().build()

    gearbox_driver.handle_gas(pressure=KICKDOWN)

    assert_gear_was_not_changed(gearbox, initial_gear)


def test_gear_is_reduced_twice_when_aggressive_kickdown():
    initial_gear = 4
    gearbox = create_gearbox().with_gear(initial_gear).build()
    gearbox_driver = create_gearbox_driver(gearbox).with_sport_mode().build()

    gearbox_driver.handle_gas(pressure=AGGRESIVE_KICKDOWN)

    assert_gear_was_reduced_twice(gearbox, initial_gear)


def assert_max_gear_is_set(gearbox):
    assert gearbox.current_gear == gearbox.MAX_GEAR


def assert_gear_was_increased(gearbox, initial_gear):
    assert gearbox.current_gear == initial_gear + 1


def assert_gear_was_reduced(gearbox, initial_gear):
    assert gearbox.current_gear == initial_gear - 1


def assert_gear_was_reduced_twice(gearbox, initial_gear):
    assert gearbox.current_gear == initial_gear - 2


def assert_gear_was_not_changed(gearbox, initial_gear):
    assert gearbox.current_gear == initial_gear
