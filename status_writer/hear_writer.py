from logging import getLogger
logger = getLogger('__main__').getChild(__name__)

def write_heared_status(message, player):
    if message[0][0] != 'hear':
        return
    if message[0][2] == 'referee':
        logger.info('write game mode: {}'.format(message[0][3]))
        player.update_status('play_mode', message[0][3])
