from enum import Enum

from gearbox.gearbox import Gearbox


class GearboxState(int, Enum):
    DRIVE = 1
    PARK = 2
    REVERSE = 3
    NEUTRAL = 4


class GearboxAdapter:
    """ Our wrapper for the API """

    MAX_GEAR = 8

    def __init__(self, gearbox: Gearbox):
        self._gearbox = gearbox
        self._set_current_gear(1)
        self.set_state(GearboxState.DRIVE)

    def get_state(self) -> int:
        return GearboxState(int(self._gearbox.get_state()))

    def set_state(self, state: GearboxState):
        self._gearbox.set_state(state.value)

    @property
    def current_gear(self) -> int:
        return int(self._gearbox.get_current_gear())

    def _set_current_gear(self, gear: int):
        self._gearbox.set_current_gear(gear)

    def get_max_drive(self) -> int:
        return self._gearbox.get_max_drive()

    def set_max_drive(self, max_drive: int):
        self._gearbox.set_max_drive(max_drive)

    def increase_gear(self):
        if self.current_gear < self.MAX_GEAR:
            self._set_current_gear(self.current_gear + 1)

    def decrease_gear(self):
        if self.current_gear > 1:
            self._set_current_gear(self.current_gear - 1)
