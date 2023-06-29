import logging
try:
    logger.debug('logger is up')
except:
# base logger setup, to standardize logging across classes
    name = 'pyelixhauser'
    formatter = logging.Formatter(fmt='%(asctime)s -  %(name)s - %(levelname)s  - %(message)s')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(logging.ERROR)
    logger.addHandler(handler)
