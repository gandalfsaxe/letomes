"""All logging setup related functions.
"""


import logging


def logging_setup(level="debug"):
    """Setup logging at specified level.

    Keyword Arguments:
        level {str} -- debug level (default: {debug})
    """

    if level == "debug":
        level = logging.DEBUG
    elif level == "info":
        level = logging.INFO
    elif level == "warning":
        level = logging.WARNING
    elif level == "error":
        level = logging.ERROR
    elif level == "critical":
        level = logging.CRITICAL
    else:
        raise ValueError(
            "Not valid debug level. Options: debug, info, warning, error, critical"
        )

    logger = logging.getLogger()
    logger.setLevel(level)

    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s (%(funcName)s): %(message)s"
    )

    fh = logging.FileHandler("code/logs/log.txt")
    fh.setLevel(level)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    ch = logging.StreamHandler()
    ch.setLevel(level)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
