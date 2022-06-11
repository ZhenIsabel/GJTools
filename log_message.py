import logging

log_record=[]

logging.basicConfig(
    filename='log.txt', format='%(asctime)s  %(message)s',
    level=logging.WARNING
)


def log_error(message):
    logging.error('ERROR: '+message)

def log_info(message):
    # logging.info('Procedure: '+message)
    pass

def log_debug(message):
    # logging.debug('DEBUG: '+message)
    pass

def log_warning(message):
    logging.warning('WARNING:'+message)
    pass

def record(message:list, times=8):
    # print(message[0]+':'+message[1])
    if len(log_record) < times:
        log_record.append(message)
    else:
        log_record.pop(0)  # 删除队首
        log_record.append(message)

def print_record():
    message = '\nrecord:\n'
    for index in range(len(log_record)):
            if(index == (len(log_record)-1)):
                message=message+(str(log_record[index][0])+':'+str(log_record[index][1]))
            else:
                message=message+(str(log_record[index][0])+':'+str(log_record[index][1])+'\n')
    return message