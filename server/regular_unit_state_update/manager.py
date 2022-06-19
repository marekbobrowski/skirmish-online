from .unit_updater import UnitUpdater


class UnitUpdaterManager:
    """
    Creates and stores all unit updaters.
    """
    def __init__(self, server):
        self.server = server
        self.updaters = {}

    def new_updater(self, session, connection):
        self.updaters[connection] = UnitUpdater(session)
