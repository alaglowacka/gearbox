from gearbox.commons import EngineRPMS


class ExternalSystems:
    def get_current_rpm(self) -> EngineRPMS:
        return EngineRPMS(rpms=1000)
