from enum import Enum

from gearbox.commons import ImmutableModel
from gearbox.gearbox import Gearbox


class GearboxState(int, Enum):
    DRIVE = 1
    PARK = 2
    REVERSE = 3
    NEUTRAL = 4


class Gear(ImmutableModel):
    gear: int

    def __attrs_post_init__(self):
        if self.gear < 1:
            raise ValueError()

    def next(self) -> "Gear":
        return Gear(gear=self.gear + 1)

    def previous(self) -> "Gear":
        return Gear(gear=self.gear - 1 if self.gear > 1 else 1)

    def is_greater_than(self, other: 'Gear') -> bool:
        return self.gear > other.gear


class GearboxAdapter:
    """ Our wrapper for the API """

    MAX_GEAR = Gear(gear=8)

    def __init__(self, gearbox: Gearbox):
        self._gearbox = gearbox
        self.change_gear(Gear(gear=1))
        self.set_state(GearboxState.DRIVE)

    def get_state(self) -> GearboxState:
        return GearboxState(int(self._gearbox.get_state()))

    def set_state(self, state: GearboxState):
        self._gearbox.set_state(state.value)

    def change_gear(self, gear_to_set: Gear):
        gear = self.MAX_GEAR if gear_to_set.is_greater_than(self.MAX_GEAR) else gear_to_set
        self._gearbox.set_current_gear(gear.gear)

    @property
    def current_gear(self) -> Gear:
        return Gear(gear=self._gearbox.get_current_gear())

    def get_max_drive(self) -> Gear:
        return Gear(gear=self._gearbox.get_max_drive())  # TODO ogarnac max drive

    def set_max_drive(self, max_drive: Gear):
        self._gearbox.set_max_drive(max_drive.gear)

    def increase_gear(self):
        self.change_gear(self.current_gear.next())

    def decrease_gear(self):
        self.change_gear(self.current_gear.previous())
