from .task_performers.health_regen import HealthRegenerator


class SessionTaskManager:
    """
    Creates, runs and stores all task performers for the specified session.
    """
    def __init__(self, session):
        self.session = session
        self.task_performers = [
            HealthRegenerator(session),
        ]
        for task_performer in self.task_performers:
            task_performer.start_task()

