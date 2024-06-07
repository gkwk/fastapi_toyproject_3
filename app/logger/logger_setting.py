import logging
from logger.custom_logger import CustomTimedRotatingFileHandler
from logging.handlers import TimedRotatingFileHandler


logger = logging.getLogger("main_looger")
logger.setLevel(logging.INFO)

log_formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")
log_handler = CustomTimedRotatingFileHandler(
    filename="../logger/app/app.log",
    # when='midnight',
    when="S",
    interval=5,
    backupCount=5,
)
log_handler.setFormatter(log_formatter)
log_handler.setLevel(logging.INFO)
logger.addHandler(log_handler)
