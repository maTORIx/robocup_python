import json
from logging import getLogger
logger = getLogger('__main__').getChild(__name__)

def write_log(message, player):
    if isinstance(message, type(None)) or len(message) < 1:
        return None
    message_head = message[0][0]
    if message_head == 'warning':
        logger.warning(json.dumps(message))
    elif message_head == 'error':
        logger.error(json.dumps(message))