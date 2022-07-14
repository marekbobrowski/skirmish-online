from redis import Redis
import logging

log = logging.getLogger(__name__)


class EventUser:
    """
    Inherit from this class if you want to send or listen to events.
    """
    def __init__(self, host="redis"):
        self.redis = Redis(host=host)
        self.listening_threads = []

    def stop_listening_threads(self):
        """
        Make sure to stop the listening threads.
        """
        count = len(self.listening_threads)
        for thread in self.listening_threads:
            thread.stop()
        # log.info(f"Stopped {count} threads.")

    def accept_event(self, event, handler, sleep_time=0.25):
        """
        Spawn a thread that will listen for specified event from redis.
        """
        p = self.redis.pubsub()
        p.subscribe(**{event: handler})
        thread = p.run_in_thread(sleep_time=sleep_time)
        self.listening_threads.append(thread)
        return thread

    def send_event(self, event, prepared_data):
        """
        Publish event in redis.
        """
        self.redis.publish(event, prepared_data)
