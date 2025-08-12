from logging import LoggerAdapter

class ThreadLoggerAdapter(LoggerAdapter):
    def process(self, msg, kwargs):
        if not self.extra:
            return msg, kwargs

        return f'[{self.extra["thread_uid"]}] - {msg}', kwargs
