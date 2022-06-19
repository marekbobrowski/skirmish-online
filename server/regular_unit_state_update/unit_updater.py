from .updaters.health_regen import HealthRegenerator


class UnitUpdater:
    """
    Creates, runs and stores all state updaters of a unit (session).
    """
    def __init__(self, session):
        self.session = session
        self.state_updaters = [
            HealthRegenerator(session),
        ]
        for state_updater in self.state_updaters:
            state_updater.start_regular_update()

