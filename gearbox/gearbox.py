from typing import List


class Gearbox:
    """ Provided API we cannot change """

    def __init__(self):
        self._max_drive: int = None
        self._current_params: List[object] = [None, None]  # state, curr_gear
        # 1 - drive, 2 - park, 3 - reverse, 4- neutral

    def get_state(self):
        return self._current_params[0]

    def get_current_gear(self):
        return self._current_params[1]

    def get_max_drive(self) -> int:
        return self._max_drive

    def set_state(self, state: int):
        self._current_params[0] = state

    def set_current_gear(self, gear: int):
        self._current_params[1] = gear

    def set_max_drive(self, max_drive: int):
        self._max_drive = max_drive
