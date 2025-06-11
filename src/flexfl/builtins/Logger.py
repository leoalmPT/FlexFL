import logging
import json
import time

class Logger:

    SEND = "send"
    RECV = "recv"
    JOIN = "join"
    NEW_WORKER = "new_worker"
    LEAVE = "leave"
    ENCODE = "encode"
    DECODE = "decode"
    EPOCH = "epoch"
    START = "start"
    END = "end"
    WORKING_START = "working_start"
    WORKING_END = "working_end"
    VALIDATION_START = "validation_start"
    VALIDATION_END = "validation_end"
    FAILURE = "failure"

    _logger = logging.getLogger("flexfl")

    @staticmethod
    def setup(file_path: str):
        Logger._logger.setLevel(logging.INFO)
        handler = logging.FileHandler(file_path, mode='w')
        formatter = logging.Formatter('%(message)s')
        handler.setFormatter(formatter)
        Logger._logger.handlers = []
        Logger._logger.addHandler(handler)
        Logger._logger.propagate = False

    
    @staticmethod
    def end():
        for handler in Logger._logger.handlers:
            handler.flush()
            handler.close()
        Logger._logger.handlers = []


    @staticmethod
    def log(event: str, **kwargs) -> dict:
        timestamp = time.time()
        data = {
            'event': event,
            'timestamp': timestamp,
            **kwargs
        }
        Logger._logger.info(json.dumps(data))
        return data
    

    @staticmethod
    def time(event: str):
        def decorator(func):
            def wrapper(*args, **kwargs):
                start = time.time()
                res = func(*args, **kwargs)
                end = time.time()
                Logger.log(event, time=end-start)
                return res
            return wrapper
        return decorator