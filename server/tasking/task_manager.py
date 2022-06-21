from .session_task_manager import SessionTaskManager
from server.connection_dependant.connection_dependant_mgr import ConnectionDependantManager


class TaskManager(ConnectionDependantManager):
    """
    Creates and stores all task managers per session/connection.
    """
    def __init__(self, server):
        self.server = server
        self.session_task_managers = {}
        super().__init__(self.session_task_managers)

    def new_session_task_manager(self, session, connection):
        self.session_task_managers[connection] = SessionTaskManager(session, connection, self.server)



