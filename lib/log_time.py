import logging
import time
from contextlib import contextmanager


@contextmanager
def log_time(logname, name, log_begin=False):
    logger = logging.getLogger(logname)
    #logger.addHandler(logging.StreamHandler())
    if(log_begin):
        logger.info(f"{name} started")
    start = time.perf_counter()
    yield
    stop = time.perf_counter()
    logger.warning(f"{name} took {stop - start}s")
