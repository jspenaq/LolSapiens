import logging


class BackendLogger:
    """
    A class to create a logger object that outputs logs to the console and a log file.

    Attributes
    ----------
    logger : logging.Logger
        The logger object that logs messages at the specified level.
    level : int
        The logging level for the logger object (default: logging.INFO).

    Methods
    -------
    """

    LOG_FILE_NAME = "lolsapiens_logs.log"
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(module)s - %(funcName)s - %(message)s"

    def __init__(self, level=logging.INFO):
        # Create a logger object
        self.logger = logging.getLogger("backend")
        self.logger.setLevel(level)

        # Create a formatter object
        formatter = logging.Formatter(fmt=self.LOG_FORMAT, datefmt="%Y-%m-%d %H:%M:%S")

        # Create a console handler
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

        # Create a file handler
        fh = logging.FileHandler(self.LOG_FILE_NAME)
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)
