from .session_task_manager import SessionTaskManager


class TaskManager:
    """
    Creates and stores all task managers per session/connection.
    """
    def __init__(self, server):
        self.server = server
        self.session_task_managers = {}

    def new_updater(self, session, connection):
        self.session_task_managers[connection] = SessionTaskManager(session)
