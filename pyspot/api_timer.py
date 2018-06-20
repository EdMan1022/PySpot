import time
import datetime


class ApiTimer(object):
    """
    Custom timer class for regulating API calls, and avoiding limit overruns
    """

    def __init__(self, request_limit_n, request_limit_t, buffer_n,
                 buffer_t, wait_buffer_t=1):
        super(ApiTimer, self).__init__()
        self.request_limit_n = request_limit_n
        self.buffer_n = buffer_n
        self.buffered_n = self.request_limit_n - self.buffer_n

        self.request_limit_t = request_limit_t
        self.buffer_t = buffer_t
        self.wait_buffer_t = wait_buffer_t

        self.start_time = datetime.datetime.now()
        self.request_n = 0
        self.end_time = self.get_end_time()

    def get_end_time(self):
        return self.start_time + datetime.timedelta(
            seconds=self.request_limit_t - self.buffer_t)

    @property
    def remaining_time(self):
        return (self.end_time - datetime.datetime.now()
                ).seconds + self.wait_buffer_t

    def reset_limit(self):
        self.start_time = datetime.datetime.now()
        self.request_n = 0
        self.end_time = self.get_end_time()

    def check_request(self):

        if self.request_n < self.buffered_n:
            if datetime.datetime.now() >= self.end_time:
                self.reset_limit()
        else:
            time.sleep(self.remaining_time)
            self.reset_limit()
        self.request_n += 1
