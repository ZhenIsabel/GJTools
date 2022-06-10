import logging


logging.basicConfig(
    filename='log.txt', format='%(asctime)s  %(message)s',
    level=logging.ERROR
)


def log_error(message):
    logging.error('ERROR: '+message)

def log_info(message):
    # logging.info('Procedure: '+message)
    pass

def log_debug(message):
    # logging.debug('DEBUG: '+message)
    pass