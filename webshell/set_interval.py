import threading
import time

StartTime = time.time()


class SetInterval:
    """Set or cancel actions called at specified intervals"""

    def __init__(self, interval, action):
        """Execute function asynchronously in intervals

        :param interval: offset in seconds
        :param action: pointer to method which should be exeuted
        :type interval: int
        :type action: function
        """
        self.interval = interval
        self.action = action
        self.stopEvent = threading.Event()
        thread = threading.Thread(target=self.__set_interval)
        thread.start()

    def __set_interval(self):
        next_time = time.time() + self.interval
        while not self.stopEvent.wait(next_time - time.time()):
            next_time += self.interval
            self.action()

    def cancel(self):
        """Stop scheduling future intervals"""
        self.stopEvent.set()
