import logging


def get_logger():
    logger = logging.getLogger('Data Engineering Challenge')
    logger.setLevel(logging.INFO)
    log_file_handler = logging.FileHandler('../log_file.log')
    log_file_handler.setLevel(logging.INFO)
    logging_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    log_file_handler.setFormatter(logging_formatter)
    logger.addHandler(log_file_handler)
    return logger