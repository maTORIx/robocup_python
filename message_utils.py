import numpy as np
from functools import lru_cache
import json
import re
from logging import getLogger
import see_message_utils

logger = getLogger('__main__').getChild(__name__)

def parse_message(message: str) -> list:
    if isinstance(message, type(None)):
        return None
    message_start = message.index('(')
    message_end = len(message) - list(reversed(message)).index(')')
    result = '(' + message[message_start:message_end] + ')'
    result = re.sub(r'  +', ' ', result)
    result = re.sub(r' +\)', ')', result)
    result = result.replace(')(', ') (').replace('(', '[').replace(')', ']').replace(' ', ',')
    result = re.sub(r'([\[,])?([A-Za-z0-9\-\.%\$\!\?<>\{\}_]+)([\],])', r'\1"\2"\3', result)
    try:
        return json.loads(result)
    except ValueError:
        logger.error('Failed to parse message.\ntarget: {}'.format(result))

omissions = {
    'player_side': {
        'r': 'right',
        'l': 'left'
    }
}

def parse_omission(omission_type:str, body:str) -> str:
    if omission_type not in omissions.keys() or body not in omissions[omission_type].keys():
        return body
    return omissions[omission_type][body]

def find_by_head(message, target):
    result = []
    for item in message:
        if item[0] == target:
            result.append(item)
    return result

flags_tmp = {
    'flt30': {'x': 0, 'y': 0},
    'flt20': {'x': 0, 'y': 0},
    'flt10': {'x': 0, 'y': 0},
    'fl0'  : {'x': 0, 'y': 0},
    'flb10': {'x': 0, 'y': 0},
    'flb20': {'x': 0, 'y': 0},
    'flb30': {'x': 0, 'y': 0},
    'fbl50': {'x': 0, 'y': 0},
    'fbl40': {'x': 0, 'y': 0},
    'fbl30': {'x': 0, 'y': 0},
    'fbl20': {'x': 0, 'y': 0},
    'fbl10': {'x': 0, 'y': 0},
    'fb0'  : {'x': 0, 'y': 0},
    'fbr10': {'x': 0, 'y': 0},
    'flr20': {'x': 0, 'y': 0},
    'flr30': {'x': 0, 'y': 0},
    'flr40': {'x': 0, 'y': 0},
    'flr50': {'x': 0, 'y': 0},
    'frb30': {'x': 0, 'y': 0},
    'frb20': {'x': 0, 'y': 0},
    'frb10': {'x': 0, 'y': 0},
    'fr0'  : {'x': 0, 'y': 0},
    'frt10': {'x': 0, 'y': 0},
    'frt20': {'x': 0, 'y': 0},
    'frt30': {'x': 0, 'y': 0},
    'ftr50': {'x': 0, 'y': 0},
    'ftr40': {'x': 0, 'y': 0},
    'ftr30': {'x': 0, 'y': 0},
    'ftr20': {'x': 0, 'y': 0},
    'ftr10': {'x': 0, 'y': 0},
    'ft0'  : {'x': 0, 'y': 0},
    'ftl10': {'x': 0, 'y': 0},
    'ftl20': {'x': 0, 'y': 0},
    'ftl30': {'x': 0, 'y': 0},
    'ftl40': {'x': 0, 'y': 0},
    'ftl50': {'x': 0, 'y': 0},
    'flt'  : {'x': 0, 'y': 0},
    'flb'  : {'x': 0, 'y': 0},
    'frb'  : {'x': 0, 'y': 0},
    'frt'  : {'x': 0, 'y': 0},
    'fc'   : {'x': 0, 'y': 0},
    'fct'  : {'x': 0, 'y': 0},
    'fcb'  : {'x': 0, 'y': 0},
    'fplb' : {'x': 0, 'y': 0},
    'fplc' : {'x': 0, 'y': 0},
    'fplt' : {'x': 0, 'y': 0},
    'fprb' : {'x': 0, 'y': 0},
    'fprc' : {'x': 0, 'y': 0},
    'fprt' : {'x': 0, 'y': 0},
    'fglt' : {'x': 0, 'y': 0},
    'fglb' : {'x': 0, 'y': 0},
    'fgrt' : {'x': 0, 'y': 0},
    'fgrb' : {'x': 0, 'y': 0},
    'gl'   : {'x': 0, 'y': 0},
    'gr'   : {'x': 0, 'y': 0}
}

flags = [
    'flt30',
    'flt20',
    'flt10',
    'fl0'  ,
    'flb10',
    'flb20',
    'flb30',
    'fbl50',
    'fbl40',
    'fbl30',
    'fbl20',
    'fbl10',
    'fb0'  ,
    'fbr10',
    'fbr20',
    'fbr30',
    'fbr40',
    'fbr50',
    'flr20',
    'flr30',
    'flr40',
    'flr50',
    'frb30',
    'frb20',
    'frb10',
    'fr0'  ,
    'frt10',
    'frt20',
    'frt30',
    'ftr50',
    'ftr40',
    'ftr30',
    'ftr20',
    'ftr10',
    'ft0'  ,
    'ftl10',
    'ftl20',
    'ftl30',
    'ftl40',
    'ftl50',
    'flt'  ,
    'flb'  ,
    'frb'  ,
    'frt'  ,
    'fc'   ,
    'fct'  ,
    'fcb'  ,
    'fplb' ,
    'fplc' ,
    'fplt' ,
    'fprb' ,
    'fprc' ,
    'fprt' ,
    'fglt' ,
    'fglb' ,
    'fgrt' ,
    'fgrb' ,
    'gl'   ,
    'gr'   ,
    'lr'   ,
    'll'   ,
    'lt'   ,
    'lb'   
]

flag_length = len(flags)
team_player_length = 6
enemy_player_length = 6
unknown_player_length = 6
unknown_goal_length = 2
ball_length = 1

object_length = team_player_length + enemy_player_length + unknown_player_length + unknown_goal_length + ball_length

# dataset structure
# | visible | direction | distance | direction_change | distance_change |
# -----------------------------------------------------------------------
# | boolean |  number   |  number  |      number      |      number     |

def parse_see_message_to_data(message:list, player) -> np.array:
    objects_data = np.zeros((object_length, 5), dtype='float32')
    flags_data = np.zeros((len(flags), 3), dtype='float32')
    team_player_start = 0
    team_player_count = 0
    enemy_player_start = team_player_start + team_player_length
    enemy_player_count = 0
    unknown_player_start = enemy_player_start + enemy_player_length
    unknown_player_count = 0
    unknown_goal_start = unknown_player_start + unknown_player_length
    unknown_goal_count = 0
    ball_start = unknown_goal_start + unknown_goal_length

    for item in message[0][2:]:
        target_index = None
        flag = False
        item_name = ''.join(item[0])

        # when item is flag
        if item_name in flags:
            flag = True
            target_index = flags.index(''.join(item[0]))
        elif item_name.startswith('p' + player.status['team_name']):
        # elif item_name.startswith('p' + 'left'):
            target_index = team_player_start + team_player_count
            team_player_count += 1
        elif item_name.startswith('p'):
            target_index = enemy_player_start + enemy_player_count
            enemy_player_count += 1
        elif item_name.startswith('b') or item_name.startswith('B'):
            target_index = ball_start
        elif item_name.startswith('G'):
            target_index = unknown_goal_start
            unknown_goal_count += unknown_goal_count
        elif item_name.startswith('P'):
            target_index = unknown_player_start + unknown_player_count
            unknown_player_count += 1
        else:
            logger.warning("Unknown object found: {}".format(json.dumps(item)))
        
        # input data
        if flag:
            flags_data[target_index, 0] = 1.0
            flags_data[target_index, 1] = float(item[1]) / 200
            flags_data[target_index, 2] = (float(item[2]) + 180.0) / 360
            continue
        
        objects_data[target_index,0] = 1.0
        objects_data[target_index,1] = float(item[1]) / 200
        objects_data[target_index,2] = (float(item[2]) + 180.0) / 360
        if len(item) > 4:
            objects_data[target_index,3] = float(item[3]) / 200
            objects_data[target_index,4] = (float(item[4]) + 180.0) / 360
        
    return np.concatenate((np.reshape(flags_data, (len(flags) * 3,)), np.reshape(objects_data, (object_length * 5))))

def calc_reward_from_see_message(message:list, player:int) -> int:
    ball_visible, ball_location = see_message_utils.ball_is_visible(message)
    ball_kickable = ball_visible and float(ball_location[1]) < 1.0
    goal_visible, goal_location = see_message_utils.enemy_goal_is_visible(message, player)
    players = list(filter(see_message_utils.filter_players(), message[0][2:]))

    reward = 0
    if ball_visible:
        reward += 1.0 - float(ball_location[1]) / 50
    else:
        reward -= 100.0
    if ball_kickable:
        reward += 50
    if goal_visible:
        reward += 20
    if ball_visible and goal_visible and float(goal_location[1]) < 30:
        reward += 70
    # if len(players) > 1:
    #     reward += 0.3

    return reward

def calc_next_reward(command, message, last_command=None):
    next_reward = 0.0
    parsed_command = parse_message(command)[0]
    ball_visible, ball_location = see_message_utils.ball_is_visible(message)
    ball_kickable = ball_visible and float(ball_location[1]) < 1.0
    if parsed_command[0] == 'kick':
        if not ball_kickable:
            next_reward -= 100
    elif parsed_command[0] == 'change_view':
        next_reward -= 20
        if last_command == command:
            next_reward -= 100
    elif parsed_command[0] == 'dash':
        if float(parsed_command[1]) < 1.0:
            next_reward -= 100
        else:
            next_reward += 20
        if float(parsed_command[2]) < 40.0 and float(parsed_command[2]) > -40.0:
            next_reward += 20
    if parsed_command[0] == 'turn':
        next_reward += 20
    return next_reward

if __name__ == '__main__':
    message = '(int aaa test aa gai (ew te isa)(egr (rgao)) (t) (aa aa (a 1.52 2) ) a)'
    print(parse_message(message))
    print(parse_message('(te tes test)'))