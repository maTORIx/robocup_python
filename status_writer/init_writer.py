import message_utils as msg_utils
from logging import getLogger
logger = getLogger('__main__').getChild(__name__)

def write_initial_status(message:list, player):
    if message[0][0] != 'init':
        return None
    elif len(message) < 1 or len(message[0]) != 4:
        raise ValueError()
    init_message = message[0]

    # set field side
    player.update_status('player_side', msg_utils.parse_omission('player_side', init_message[1]))

    # set player number
    if player.status['player_number'] != int(init_message[2]):
        logger.info('player {} number changed to {}'.format(player.status['player_number'], init_message[2]))
        player.update_status('player_number', int(init_message[2]))
    
    # set playmode
    player.update_status('play_mode', init_message[3])