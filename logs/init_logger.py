import logging


def init_logger(name):
    logger = logging.getLogger(name)
    FORMAT = '%(asctime)s -:- %(levelname)s -:- %(name)s -:- %(message)s'
    logger.setLevel(logging.DEBUG)
    console = logging.StreamHandler()
    console.setFormatter(logging.Formatter(FORMAT))
    console.setLevel(logging.DEBUG)
    info_debug = logging.FileHandler(filename="logs/info_debug.log")
    info_debug.setFormatter(logging.Formatter(FORMAT))
    info_debug.setLevel(logging.DEBUG)
    err_warning = logging.FileHandler(filename="logs/err_warning.log")
    err_warning.setFormatter(logging.Formatter(FORMAT))
    err_warning.setLevel(logging.WARNING)
    logger.addHandler(console)
    logger.addHandler(info_debug)
    logger.addHandler(err_warning)
    logger.debug("Логгер инициализирован")
