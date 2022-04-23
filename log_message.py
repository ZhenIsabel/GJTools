import logging
import config_model


logging.basicConfig(
    filename='log.txt', format='%(asctime)s  %(message)s',
    level=logging.DEBUG if config_model.config['is_testmode']==1 else logging.ERROR
)


def log_error(message):
    logging.error('ERROR: '+message)

def log_info(message):
    logging.info('Procedure: '+message)

def log_debug(message):
    logging.debug('DEBUG: '+message)