import logging
import logging.handlers
import time
from functools import wraps

log = logging.getLogger(__name__)


def api_logger(func):
    api_log = logging.getLogger("api_log")

    @wraps(func)
    def wrapper(*args, **kwargs):
        request = kwargs.get('request')
        api_info = "{url} - {method} - {data}".format(url=request.url, method=request.method, data=request.json())
        api_log.info(api_info)
        return func(*args, **kwargs)

    return wrapper


def log_setup(filename):
    log_handler = logging.handlers.TimedRotatingFileHandler(filename=filename, when='midnight', interval=1)
    formatter = logging.Formatter('%(asctime)s LoveallAPI [%(process)d]: %(message)s', '%b %d %H:%M:%S:%ms')
    formatter.converter = time.localtime
    log_handler.setFormatter(formatter)
    logger = logging.getLogger()
    logger.addHandler(log_handler)
    logger.setLevel(logging.INFO)
