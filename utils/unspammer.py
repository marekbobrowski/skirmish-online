from datetime import datetime, timedelta


class RequestUnspammer:
    INTERVAL = timedelta(milliseconds=500)

    def __init__(self):
        self.last_spammed = datetime.now()

    def clean(self):
        if datetime.now() - self.last_spammed < self.INTERVAL:
            return False

        self.last_spammed = datetime.now()
        return True
